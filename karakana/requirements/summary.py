"""Markdown renderers for requirement artifacts."""

from __future__ import annotations

from karakana.requirements.schemas import IssueDraft, ReadinessCheck, RequirementPRD, UserStory


def render_prd(prd: RequirementPRD) -> str:
    impact = prd.harness_impact
    standards = prd.standards_spec
    return f"""# Product Requirements Document

## Context

{prd.context}

## Problem

{prd.problem}

## Goal

{prd.goal}

## Non-Goals

{_bullets(prd.non_goals)}

## Users / Actors

{_bullets(prd.users_or_actors)}

## User Stories

{_bullets([f"As a {actor}, I want the capability described by this PRD so that {prd.goal}" for actor in prd.users_or_actors] or ["Needs review: user stories not generated yet."])}

## Functional Requirements

{_bullets(prd.functional_requirements)}

## Non-Functional Requirements

{_bullets(prd.non_functional_requirements)}

## Harness Subsystem Impact

### Instructions

{_bullets(impact.instructions)}

### Tools

{_bullets(impact.tools)}

### Environment

{_bullets(impact.environment)}

### State

{_bullets(impact.state)}

### Feedback

{_bullets(impact.feedback)}

## Standards

{_bullets(standards.standards)}

## Spec

{_bullets(standards.spec)}

## Acceptance Criteria

{_bullets(standards.acceptance_criteria)}

## Risks

{_bullets(prd.risks)}

## Safety Constraints

{_bullets(prd.safety_constraints)}

## Suggested Skills

{_bullets(prd.suggested_skills)}

## Suggested Skillpack

{prd.suggested_skillpack or "Needs review: no skillpack selected."}

## Model Routing

- Provider: {prd.model_route.get("provider") or "Needs review"}
- Model: {prd.model_route.get("model") or "Needs review"}
- Rationale: {prd.model_route.get("rationale") or "Needs review"}

## Test and Eval Plan

{_bullets(prd.test_and_eval_plan)}

## Rollout / Review Plan

{_bullets(prd.rollout_or_review_plan)}
"""


def render_stories(stories: list[UserStory]) -> str:
    body = ["# User Stories\n"]
    for story in stories:
        body.append(
            f"""## Story: {story.title}

As a {story.actor},
I want {story.want},
so that {story.outcome}.

### Acceptance Criteria

{_bullets(story.acceptance_criteria)}

### Standards

{_bullets(story.standards)}

### Risks

{_bullets(story.risks)}

### Required Skills

{_bullets(story.required_skills)}

### Required Tests / Evals

{_bullets(story.required_tests_or_evals)}

### Definition of Ready

{_bullets(story.definition_of_ready)}

### Definition of Done

{_bullets(story.definition_of_done)}
"""
        )
    return "\n".join(body)


def render_issues(issues: list[IssueDraft]) -> str:
    body = ["# Issue Drafts\n"]
    for issue in issues:
        route = issue.recommended_model_route
        body.append(
            f"""## Issue: {issue.title}

### Summary

{issue.summary}

### Story

{issue.story_id or "None"}

{_issue_metadata(issue)}

### Scope

{_bullets(issue.scope)}

### Out of Scope

{_bullets(issue.out_of_scope)}

### Acceptance Criteria

{_bullets(issue.acceptance_criteria)}

### Implementation Notes

{_bullets(issue.implementation_notes)}

### Suggested Skills

{_bullets(issue.suggested_skills)}

### Suggested Skillpack

{issue.suggested_skillpack or "Needs review"}

### Recommended Model Route

- Provider: {route.get("provider") or "Needs review"}
- Model: {route.get("model") or "Needs review"}
- Rationale: {route.get("rationale") or "Needs review"}
- Escalation conditions: security/auth, payments, migrations, process state, production risk, or repeated failures

### Safety Constraints

{_bullets(issue.safety_constraints)}

### Tests / Evals

{_bullets(issue.tests_or_evals)}

### Definition of Done

{_bullets(issue.definition_of_done)}

### Labels

{_bullets(issue.labels)}
"""
        )
    return "\n".join(body)


def _issue_metadata(issue: IssueDraft) -> str:
    if not issue.metadata:
        return ""
    lines = ["### Research and Evidence Mapping", ""]
    labels = [
        ("project_context", "Project context"),
        ("research_objective", "Research objective supported"),
        ("research_question", "Research question supported"),
        ("platform_capability", "Platform capability"),
        ("workflow", "Workflow"),
        ("evidence_artifact", "Evidence artifact produced"),
        ("schema_artifact", "Schema artifact"),
        ("verification_command", "Verification command"),
    ]
    for key, label in labels:
        if issue.metadata.get(key):
            lines.append(f"- {label}: {issue.metadata[key]}")
    target_files = issue.metadata.get("target_files")
    if target_files:
        lines.append("- Target files:")
        lines.extend(f"  - {path}" for path in target_files)
    return "\n".join(lines) + "\n"


def render_readiness(check: ReadinessCheck) -> str:
    return f"""# Requirements Readiness Review

## Summary

- Requirement: {check.req_id}
- Ready: {check.ready}
- Status: {check.status}

## Passed Checks

{_bullets(check.passed)}

## Failed Checks

{_bullets_or_none(check.failed)}

## Warnings

{_bullets_or_none(check.warnings)}

## Recommended Next Actions

{_bullets(check.recommended_next_actions)}
"""


def render_requirement_summary(req_id: str, paths: dict[str, str]) -> str:
    return "\n".join(["# Karakana Requirement", "", f"- Requirement ID: {req_id}"] + [f"- {name}: {path}" for name, path in paths.items()]) + "\n"


def _bullets(values: list[str]) -> str:
    if not values:
        return "- Needs review: not enough source evidence."
    return "\n".join(f"- {value}" for value in values)


def _bullets_or_none(values: list[str]) -> str:
    if not values:
        return "- None"
    return "\n".join(f"- {value}" for value in values)
