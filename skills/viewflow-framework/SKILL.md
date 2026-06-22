---
name: viewflow-framework
description: Use this skill when working on Django Viewflow workflows, process state, tasks, flow classes, forms, views, viewsets, frontend behavior, approvals, assignments, permissions, dashboards, or workflow testing.
version: 0.1.0
risk_level: high
category: development
scope: bundled
status: stable
visibility: public
bucket: development
activation:
  keywords:
    - viewflow
    - workflow
    - process
    - flow
    - task
    - viewset
    - frontend
    - approval
    - assignment
    - transition
    - dashboard
  required_files:
    - pyproject.toml
  optional_tools:
    - pytest
    - python
    - git
allowed_tools:
  - read_file
  - grep
  - code_search
  - run_tests
  - python
requires_approval_for:
  - workflow_state_change
  - permission_change
  - authentication_change
  - data_migration
  - production_config_change
  - destructive_command
---
# Viewflow Framework Skill

## Purpose

Guide safe analysis, design, debugging, and review of Django Viewflow workflows and related frontend behavior.

## When to use this skill

Use for Viewflow flow classes, process state, task transitions, approvals, assignments, forms, views, viewsets, dashboard behavior, permissions, workflow tests, migration risk, and stuck process debugging.

## When not to use this skill

Do not use for general Django bugs without workflow impact; use `django-debugging` instead. Do not use for billing-specific workflow rules without also considering `gepg-billing`, or Invenio workflow integration without also considering `invenio-framework`.

## Quick Reference

- Separate workflow/process state from domain/business data.
- Review permissions and assignment for every approval, ownership, or role-based workflow.
- Treat frontend form, viewset, and dashboard changes as workflow correctness changes.
- Require tests for valid transitions, invalid transitions, permissions, assignment, validation, completion, and cancellation where applicable.

## Core concepts

Flow data is workflow/process state: current step, task state, decisions, assignments, temporary values, and transition history.

Business data is domain state: invoices, samples, studies, submissions, registrations, patients, laboratory requests, payments, or other project records.

Workflow code should not hide business rules. Check whether rules are clearly expressed, testable, not buried only in UI code, and not duplicated between forms, views, and transitions.

Permission and assignment review is mandatory for approvals, ownership, role-based access, task claiming, task delegation, cancellation, rejection, and reopen behavior.

Frontend changes can affect workflow correctness. Forms, views, viewsets, templates, dashboard actions, and user-facing task controls can change how users move through a process.

Tests are mandatory for behavior changes and should cover valid transitions, invalid transitions, permissions, assignment, form validation, completed states, and cancelled states where applicable.

## Standard workflow

1. Identify the process, flow class, task nodes, forms, views/viewsets, and templates involved.
2. Separate flow data from business data and document where each is stored.
3. Map actors, permissions, assignments, transitions, approvals, rejection/rework paths, and final states.
4. Review frontend behavior for validation, available actions, task visibility, and dashboard navigation.
5. Check migration and active-process compatibility when changing existing workflows.
6. Add or request tests for valid paths, invalid paths, permissions, assignment, form validation, completed states, and cancelled states.

## Pitfalls

- Do not bury business rules only in forms, templates, or button visibility.
- Do not duplicate transition rules across UI and backend without tests.
- Do not change task names, process states, URLs, templates, or permissions without considering active processes.
- Do not assume frontend changes are presentation-only.
- Do not bypass permission or assignment checks to unblock stuck workflows.

## Verification

- Run focused workflow tests.
- Test valid and invalid transitions.
- Test permissions, ownership, assignment, and approval authority.
- Test form validation and frontend action availability.
- Test completed and cancelled states where applicable.
- Document active-process migration risk.

## Safety rules

- Do not change workflow state, permissions, authentication, migrations, production config, or destructive behavior without approval.
- Do not mutate active process data manually unless explicitly approved and backed by a tested recovery plan.
- Do not expose secrets or private workflow data in traces, reports, or logs.
- Keep workflow changes reviewable and reversible.

## Required checks

- Check flow data versus business data separation.
- Check permission and assignment rules.
- Check frontend forms, views, viewsets, templates, and dashboard behavior.
- Check migration and active-process compatibility.
- Run or request workflow behavior tests.

## Output format

Return workflow summary, actors, flow data, business data, transitions, permission/assignment review, frontend review, migration risk, tests, approval requirements, and remaining TODOs.

## Examples

- Review a new approval workflow for roles, rejection paths, and final states.
- Debug a stuck process by comparing expected state, actual state, current task, actor, and last transition.
- Review a Viewflow form/viewset change for validation, user actions, permissions, and tests.
