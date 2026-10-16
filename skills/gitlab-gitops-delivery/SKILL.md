---
name: gitlab-gitops-delivery
description: Deliver source changes from GitLab through tested container publication, GitOps promotion and verified Argo CD rollout across repository boundaries.
version: 0.1.0
risk_level: high
category: infrastructure
scope: bundled
status: experimental
visibility: public
bucket: infrastructure
activation:
  keywords: [GitLab GitOps, eGA deployment, Argo image promotion]
  optional_tools: [git, docker, kubectl]
allowed_tools: [read_file, grep, code_search, run_tests]
requires_approval_for: [workflow_change, production_config_change, deployment, ci_secret_change]
---
# GitLab to GitOps Delivery

## Purpose

Keep source, image, overlay, GitOps and runtime evidence connected through release.

## When to use this skill

Use when a GitLab source repository builds images and promotes a separate
GitOps repository, especially where GitHub runners cannot reach source GitLab.

## When not to use this skill

Do not replace an application's existing CI provider merely because this skill
is available. Read the project's actual pipeline and release convention first.

## Quick Reference

Record source SHA, overlay SHA, pipeline URL, image tag/digest, GitOps commit,
Argo revisions and running image. A successful image build is not a rollout.

## Core concepts

The source MR, overlay PR, and GitOps promotion have different owners. Match
the protected deployment branch and runner tags. Validate runner capabilities
before selecting a builder. Protected masked variables belong in the CI store;
never include them in tracked files or supplied-at-runtime pipeline parameters.

## Standard workflow

1. Inspect current upstream branches, open changes, runner tags/capabilities,
   pipeline configuration, overlay pin and GitOps image-name mapping.
2. Test a bounded change on a task branch and use the project's MR/PR and
   squash-merge convention. Add required production configuration before a new
   image requiring it can be promoted.
3. Pin overlays immutably. When an overlay changes, update its pin and version
   and trigger the source pipeline; a source SHA alone cannot identify it.
4. Gate image publication/promotion on relevant tests. Promote coupled images
   together only after all builds succeed. Protect promotion from stale jobs
   and competing scheduled workflows.
5. Follow the pipeline through registry push and the actual GitOps commit.
   Check Argo sync/health and running images, then exercise public behavior.
6. Test notification configuration in its real execution network. Distinguish
   configured notifications, transport acceptance and observed inbox delivery.

## Safety rules

Respect existing explicit authorization for the bounded release. Do not change
shared runner host privileges or disclose credentials to solve a build failure.
Do not overwrite concurrent GitOps changes or infer all apps are deployed from
one successful pipeline.

## Required checks

CI lint, focused tests, paired image publication, correct immutable tags,
GitOps commit, Argo sync/health, running images and a relevant application test.
Record notification evidence without claiming unseen inbox delivery.

## Pitfalls

An online runner may reject untagged jobs or rootless user namespaces. A token
that reads source may lack package-push scope. A second scheduled promoter may
revert the new tag. Generic CI success does not prove the public workflow works.

## Verification

Use current CI job logs, registry metadata, GitOps source, Argo status and public
smoke tests. Diagnose the first failure before changing builder architecture.
Keep locally generated credentials and source archives outside tracked artifacts.

## Examples

If frontend compilation fails inside the image builder but passes in a regular
Node job, publish its compiled artifact and package it separately after verifying
that both jobs use the same source and overlay revisions.

## Output format

Return merged changes, source/overlay revisions, pipeline result, image identity,
GitOps commit, observed rollout and application checks, and unresolved failures.
