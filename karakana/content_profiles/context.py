"""Explicit source selections, governing coverage, reference edges and evidence.

Only locators and source-derived identities enter results; source facts are not
copied into configuration or treated as authenticated approvals.
"""
from dataclasses import dataclass
from datetime import datetime
from pathlib import PurePosixPath
import re
from urllib.parse import urlsplit, unquote

from .reader import read_source, plain, SUBSTITUTION
from .schemas import ContentError, Section


@dataclass
class Selection:
    source: object
    start: int
    end: int
    prose: list
    tables: list
    row: object = None
    spec: object = None
    field: str = None

    @property
    def value(self):
        if self.field: return self.row.values[self.field]
        if self.row: return '\n'.join(self.row.values.values())
        return '\n'.join([v for _,v in self.prose]+[v for _,rows in self.tables for row in rows for v in row.values.values()])

    @property
    def location(self):
        result={'path':self.source.path,'line':self.row.line if self.row else self.prose[0][0] if self.prose else self.start}
        if self.field:result['field']=self.field
        if self.row and self.spec and self.spec['identity']:result['record_id']=self.row.values[self.spec['identity']]
        return result

    @property
    def identity(self):
        return self.source.key,self.row.line if self.row else self.start,self.field


class Context:
    def __init__(self, inputs, narratives, context, md):
        self.inputs,self.context,self.md=inputs,context,md
        self.docs={d.key:d for d in narratives}
        self.sources={d.key:d.source for d in narratives}
        self.specs={d['key']:d for d in context['documents']}
        self.table_specs=[]
        for doc in narratives:
            for spec in doc.profile['tables']:
                if spec not in self.table_specs:self.table_specs.append(spec)
        paths={inputs.root/d.path for d in narratives}
        for ref in sorted(context.get('references',[]),key=lambda r:r['key']):
            raw,path=inputs.read(ref['path'],'reference:'+ref['key'])
            physical=inputs.root/path
            if physical in paths:raise ContentError('A document/reference source was declared more than once.',rule='CP-ID-001')
            paths.add(physical)
            if ref.get('format')=='narrative-0.1':self.sources[ref['key']]=read_source(raw,ref['key'],path,md)
        self.links={}
        self.claims=[]
        self.claim_sources=[]
        self.mapped_items=[]
        self.findings=[]

    def select(self, locator, *, nonempty=True):
        source=self.sources.get(locator['document'])
        if source is None:raise ContentError('Select a declared, successfully read narrative source; opaque files have no locators.',rule='CP-LOCATOR-001')
        start,end=source.bounds(locator)
        tables=[];matches=[]
        specs=self.docs[source.key].profile['tables'] if source.key in self.docs else self.table_specs
        for table in source.tables:
            rows=[r for r in table.rows if start<=r.line<=end]
            if not rows and not start<=table.line<=end:continue
            tables.append((table,rows))
            for spec in specs:
                if table.headers not in spec['headers']:continue
                for row in rows:
                    if 'record_id' in locator and (not spec['identity'] or row.values[spec['identity']]!=locator['record_id']):continue
                    if 'field' in locator and locator['field'] not in row.values:continue
                    matches.append((row,spec))
        # Shared metadata/standards specs across profiles do not make one physical row ambiguous.
        unique={ (row.line,spec['record_type'],spec['identity']):(row,spec) for row,spec in matches }
        row=spec=None
        if 'field' in locator or 'record_id' in locator:
            if len(unique)!=1:raise ContentError('The row or cell is absent, unregistered or ambiguous. Use its actual ID or unique row/cell anchor.',rule='CP-LOCATOR-001',location={'path':source.path,'line':start})
            row,spec=next(iter(unique.values()))
            tables=[(table,[row]) for table,rows in tables if row in rows]
            start=end=row.line
        selection=Selection(source,start,end,[(line,v) for line,v in source.prose if start<=line<=end],tables,row,spec,locator.get('field'))
        if nonempty and (not plain(self.md,selection.value).strip() or SUBSTITUTION.search(plain(self.md,selection.value))):
            raise ContentError('Complete the selected source content before using this mapping.',rule='CP-CONTENT-001',location=selection.location)
        return selection

    def _slot(self, entry):
        doc=self.docs.get(entry['document'])
        if doc is None:raise ContentError('A mapping requires a successfully read profiled document.',rule='CP-COVERAGE-001')
        slot=next((s for s in doc.profile['slots'] if s['id']==entry['slot']),None)
        if slot is None:raise ContentError('Select a registered profile slot.',rule='CP-COVERAGE-001',location={'path':doc.path,'line':1})
        return doc,slot

    def prepare(self):
        mappings={(c['document'],c['slot']):c for c in self.context.get('coverage',[])}
        visiting,visited=set(),set()
        def visit(node):
            if node in visiting:raise ContentError('Governing-view coverage contains a cycle. Locate an actual independent source.',rule='CP-COVERAGE-001')
            if node in visited:return
            visiting.add(node)
            locator=mappings[node]['source']
            source_doc=self.docs.get(locator['document'])
            if source_doc:
                start,end=source_doc.source.bounds(locator)
                for slot in source_doc.profile['slots']:
                    heading=() if not slot['heading'] else (slot['heading'],)
                    candidates=[s for s in source_doc.source.sections if s.path==heading]
                    target=(source_doc.key,slot['id'])
                    if target in mappings and target!=node and any(s.line<=start<=s.end for s in candidates):
                        visit(target)
            # A direct local locator names actual content, not a recursive self-map.
            visiting.remove(node);visited.add(node)
        for node in mappings:visit(node)
        for entry in self.context.get('coverage',[]):
            doc,slot=self._slot(entry)
            source=self.select(entry['source'])
            if slot['id']=='metadata' and source.source.key!=doc.key:
                raise ContentError('Document identity must come from its own canonical metadata.',rule='CP-METADATA-001',location=source.location)
            spec=next((s for s in doc.profile['tables'] if s['slot']==slot['id']),None)
            if spec:
                if len(source.tables)!=1 or source.tables[0][0].headers not in spec['headers']:
                    raise ContentError('This slot requires its registered table shape; prose or a different table cannot replace it.',rule='CP-COVERAGE-001',location=source.location)
                rows=source.tables[0][1]
                if source.source.key==doc.key:doc.native_tables.add(source.tables[0][0].line)
                if len(rows)<spec['min_rows']:raise ContentError('The located table has no applicable records.',rule='CP-COVERAGE-001',location=source.location)
                # Existing declared rows still get checked: a mapping cannot suppress local errors.
                original=doc.tables.get(spec['id'],[])
                identities={(r.path,r.line) for r in rows}
                doc.tables[spec['id']]=rows+[r for r in original if (r.path,r.line) not in identities]
                if slot['id']=='metadata':
                    metadata={}
                    for row in doc.tables[spec['id']]:
                        key=row.values['Document information']
                        if key in metadata:raise ContentError('Duplicate canonical metadata field.',rule='CP-METADATA-001',location=source.location)
                        metadata[key]=row.values['Value']
                    doc.metadata=metadata
            if slot['kind'] in ('prose','mixed') and not source.prose:
                raise ContentError('This content slot requires actual located explanation, not an empty heading or table alone.',rule='CP-COVERAGE-001',location=source.location)
            doc.sections[slot['heading']]=Section(slot['heading'],source.start,source.end,source.prose)
            doc.selections[slot['id']]=source.location
            doc.origins[slot['heading']]=source.location
            doc.origins[slot['id']]=source.location
        for entry in self.context.get('omissions',[]):
            doc,slot=self._slot(entry)
            if slot['required'] or (doc.key,slot['id']) in mappings:
                raise ContentError('Only an absent conditional slot can have an omission rationale; required content cannot be waived.',rule='CP-COVERAGE-001',location={'path':doc.path,'line':1})
            section=doc.sections.get(slot['heading'])
            if section and (section.prose or doc.tables.get(slot['id'])):
                raise ContentError('Existing source content must still be checked; omit only an absent conditional slot.',rule='CP-COVERAGE-001',location={'path':doc.path,'line':section.line})
            rationale=self.select(entry['rationale'])
            doc.omissions[slot['id']]=rationale.location
        for doc in self.docs.values():
            for table in doc.source.tables:
                if table.line not in doc.native_tables:
                    raise ContentError('A native table is outside the selected profile views. Locate it explicitly; records cannot be silently omitted.',
                                       rule='CP-TABLE-001', unsupported=True, location={'path':doc.path,'line':table.line})
        self._links()
        self._open_items()
        self._claims()

    def owner(self, selection):
        if not selection.row:
            return self.docs.get(selection.source.key)
        native = self.docs.get(selection.source.key)
        if native and any(row.path == selection.row.path and row.line == selection.row.line
                          for rows in native.tables.values() for row in rows):
            return native
        owners = [doc for doc in self.docs.values() if any(
            row.path == selection.row.path and row.line == selection.row.line
            for rows in doc.tables.values() for row in rows)]
        if len(owners) != 1:
            raise ContentError('The selected record has no unique checked baseline owner.', rule='CP-REFERENCE-001', location=selection.location)
        return owners[0]

    def _links(self):
        fields={('requirements','functional','Acceptance criteria'):'criterion',
                ('requirements','quality','Verification reference'):'criterion',
                ('requirements','acceptance','Requirement ID'):'requirement',
                ('system-design','quality','Requirement / concern'):'requirement',
                ('system-design','verification','Requirement / risk'):'requirement',
                ('system-design','quality','Verification reference / unresolved measure'):'criterion',
                ('system-design','verification','Planned check / evidence'):'criterion'}
        seen=set()
        for edge in self.context.get('links',[]):
            source=self.select(edge['from']);target=self.select(edge['to'])
            doc=self.owner(source)
            target_doc=self.owner(target)
            expected=fields.get((doc.profile['profile_id'],source.spec['id'],source.field)) if doc and source.spec else None
            baselines=[doc.key] if doc and doc.profile['profile_id']=='requirements' else self.specs[doc.key].get('requirements',[]) if doc else []
            if (not expected or not target_doc or target_doc.key not in baselines or not target.spec
                    or target.spec['record_type']!=expected or target_doc.profile['profile_id']!='requirements'):
                raise ContentError('Link a registered reference cell to the required record kind in its declared requirements baseline.',rule='CP-REFERENCE-001',location=source.location)
            # Both endpoints must participate in checked views, not hidden/unselected records.
            if (source.row not in doc.tables.get(source.spec['id'],[]) or
                    target.row not in target_doc.tables.get(target.spec['id'],[])):
                raise ContentError('Select source and target records in the checked profile views.',rule='CP-REFERENCE-001',location=source.location)
            key=(source.identity,target.identity)
            if key in seen:raise ContentError('An explicit reference edge is duplicated after resolving its source selectors.',rule='CP-REFERENCE-001',location=source.location)
            seen.add(key)
            self.links.setdefault((source.row.path,source.row.line,source.field),set()).add(target.row.values[target.spec['identity']])

    def _open_items(self):
        seen=set()
        for item in self.context.get('open_items',[]):
            source=self.select(item['item'])
            item_identity = (source.source.key, source.row.line if source.row else source.start)
            if item_identity in seen:raise ContentError('Locate each open item once; different cells cannot override one canonical row.',rule='CP-CONTEXT-001',location=source.location)
            seen.add(item_identity)
            affected=[]
            for locator in item['affected']:
                target=self.select(locator)
                owner=self.owner(target)
                if not owner or (target.row and target.spec['record_type']!='requirement'):
                    raise ContentError('Locate an actual affected requirement or declared document scope.',rule='CP-CONTEXT-001',location=target.location)
                affected.append({'document':owner.key,**target.location})
            fields={key:self.select(item[key]).location for key in ('effect','resolver','next_action')}
            self.mapped_items.append({'document':source.source.key,'record_id':source.location.get('record_id'),
                'kind':'mapped_open_item','location':source.location,'affected_records':sorted({x['record_id'] for x in affected if 'record_id' in x}),
                'affected_scopes':sorted(affected,key=lambda x:(x['document'],x['path'],x['line'])),
                'resolution_detail':'declared',**fields})

    def _claims(self):
        seen=set()
        for claim in self.context.get('claims',[]):
            source=self.select(claim['source'])
            if source.identity in seen:raise ContentError('Locate each observed claim once.',rule='CP-CLAIM-001',location=source.location)
            seen.add(source.identity)
            fields={key:self.select(value) for key,value in claim['fields'].items()}
            try:
                when=datetime.fromisoformat(plain(self.md,fields['time'].value).strip().replace('Z','+00:00'))
                if when.tzinfo is None or when.utcoffset() is None:raise ValueError()
            except ValueError as exc:
                raise ContentError('Locate an actual timezone-aware observation or decision time.',rule='CP-CLAIM-001',location=fields['time'].location) from exc
            if plain(self.md,fields['result'].value).strip().lower() in {'planned','proposed','not run','pending','not observed'}:
                raise ContentError('Planned work is not an observed result or accepted decision. Locate an actual scoped observation.',rule='CP-CLAIM-001',location=fields['result'].location)
            evidence=fields['evidence'];uris=[]
            for token in self.md.parseInline(evidence.value)[0].children or []:
                if token.type=='link_open':uris.append(token.attrGet('href'))
            if not uris:uris=[evidence.value.strip()]
            external=False
            for uri in uris:
                try:parts=urlsplit(uri)
                except ValueError as exc:raise ContentError('Use a supported local evidence path or HTTP(S) URI.',rule='CP-EVIDENCE-001',location=evidence.location) from exc
                if parts.scheme:
                    if parts.scheme not in {'https','http'} or not parts.hostname or parts.username or parts.password:
                        raise ContentError('Use a credential-free HTTP(S) evidence URI or a guarded local relative path.',rule='CP-EVIDENCE-001',location=evidence.location)
                    external=True
                else:
                    if parts.netloc or parts.query:raise ContentError('Use a root-guarded local evidence path without a host or query.',rule='CP-EVIDENCE-001',location=evidence.location)
                    path=PurePosixPath(evidence.source.path).parent/unquote(parts.path)
                    if not parts.path:raise ContentError('Locate an actual evidence file.',rule='CP-EVIDENCE-001',location=evidence.location)
                    self.inputs.read(str(path),'claim_evidence')
            status='external_not_checked' if external else 'local_hashed_not_authenticated'
            self.claims.append({'source':source.location,'kind':claim['kind'],
                'fields':{key:value.location for key,value in fields.items()},'evidence_status':status})
            self.claim_sources.append((source,claim['kind']))
            if external:self.findings.append({'document':source.source.key,'rule_id':'CP-EVIDENCE-REVIEW','severity':'warning',
                'category':'review','location':evidence.location,'message':'External evidence was not fetched or authenticated. Review the evidence and its source before relying on the claim.'})

    def claim_covers(self,path,line,kind='decision'):
        return any(k==kind and s.source.path==path and s.start<=line<=s.end for s,k in self.claim_sources)
