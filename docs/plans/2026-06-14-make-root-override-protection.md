---
title: "fix: Protect the Make repository root from overrides"
date: 2026-06-14
---

# Protect the Make Repository Root from Overrides

## Status: Completed

## Context

The Makefile derives `ROOT` from its own path, but GNU Make command-line
assignments override an ordinary `:=` definition. A hostile root can redirect
the OAuth, workflow, documentation, and optional Unity verification away from
the reviewed checkout.

## Requirements

- Protect `ROOT` with GNU Make's `override` directive and keep deriving it from
  the loaded Makefile path.
- Preserve `PYTHON ?= python3` and the existing optional Unity build behavior.
- Require exact protected root and Python override lines in the portable
  checker.
- Pass local, external-directory, and hostile `ROOT=` full gates.
- Reject ordinary, recursive, `CURDIR`, first-Makefile, weakened-checker,
  Python-override, and plan-status mutations.
- Preserve all OAuth, workflow, Unity project, and documentation contracts.

## Implementation Units

- **Makefile:** protect only the internal repository root.
- **scripts/check_unity_contracts.py:** enforce exact Makefile lines and
  register this plan.
- **this plan:** record actual bounded validation before shipment.

## Verification Plan

- focused CI/Makefile contract and Python compilation
- full `make check` under a hard timeout
- external-directory and hostile-root full gates
- eight focused mutations
- workflow YAML, Unity XML/assets, SVG XML, intended-path, artifact,
  `git diff --check`, and changed-line secret audits

## Scope Boundaries

- Do not alter OAuth flow, Unity source, dependencies, workflows, or runtime
  behavior.
- Do not merge or close any stacked pull request without owner authorization.

## Work Completed

- Protected the Makefile-derived root while preserving the Python override.
- Added exact-line checker contracts and registered this completed plan.

## Verification

- Python compilation and the focused CI/Makefile contract passed.
- Local, external-directory, and hostile-root `make check` runs passed under
  240-second timeouts with all 18 contract groups; Unity correctly remained
  unavailable on Linux.
- Eight hostile root, checker, Python override, and plan-status mutations were
  rejected.
- Python syntax, workflow YAML, Unity XML, SVG XML, intended-path, artifact,
  `git diff --check`, and changed-line secret audits passed before shipment.
