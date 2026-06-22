"""Storage for self-improvement proposals."""

from __future__ import annotations

import json
import secrets
from datetime import datetime, timezone
from pathlib import Path

from karakana.improvement.schemas import ImprovementProposal
from karakana.improvement.summary import render_proposal_markdown


class ProposalStore:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.proposals_root = repo_root / ".karakana" / "proposals"

    def save(self, proposal: ImprovementProposal) -> Path:
        proposal_dir = self.proposals_root / proposal.proposal_id
        proposal_dir.mkdir(parents=True, exist_ok=True)
        (proposal_dir / "evidence").mkdir(exist_ok=True)
        proposal_path = proposal_dir / "proposal.json"
        proposal_path.write_text(json.dumps(proposal.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.write_summary(proposal)
        self._write_latest(proposal.proposal_id)
        return proposal_path

    def load(self, proposal_id: str) -> ImprovementProposal:
        proposal_path = self.proposals_root / proposal_id / "proposal.json"
        if not proposal_path.exists():
            raise FileNotFoundError(f"Proposal not found: {proposal_id}")
        return ImprovementProposal.from_dict(json.loads(proposal_path.read_text(encoding="utf-8")))

    def list_proposals(self, limit: int = 20) -> list[ImprovementProposal]:
        if not self.proposals_root.exists():
            return []
        proposals = []
        for path in self.proposals_root.iterdir():
            if not path.is_dir():
                continue
            proposal_path = path / "proposal.json"
            if proposal_path.exists():
                proposals.append(ImprovementProposal.from_dict(json.loads(proposal_path.read_text(encoding="utf-8"))))
        return sorted(proposals, key=lambda proposal: proposal.created_at, reverse=True)[:limit]

    def latest(self) -> ImprovementProposal | None:
        latest_file = self.proposals_root / "latest"
        if latest_file.exists():
            proposal_id = latest_file.read_text(encoding="utf-8").strip()
            if proposal_id:
                try:
                    return self.load(proposal_id)
                except FileNotFoundError:
                    pass
        proposals = self.list_proposals(limit=1)
        return proposals[0] if proposals else None

    def write_summary(self, proposal: ImprovementProposal) -> Path:
        summary_path = self.proposals_root / proposal.proposal_id / "proposal.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(render_proposal_markdown(proposal), encoding="utf-8")
        return summary_path

    def _write_latest(self, proposal_id: str) -> None:
        self.proposals_root.mkdir(parents=True, exist_ok=True)
        (self.proposals_root / "latest").write_text(proposal_id + "\n", encoding="utf-8")


def generate_proposal_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-improve-{secrets.token_hex(3)}"
