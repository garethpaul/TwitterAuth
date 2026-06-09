# TwitterAuth Baseline

Status: Completed

## Scope

Preserve the legacy Unity Twitter OAuth sample while keeping credential,
runtime URL, and token-log guardrails visible through static checks.

## Completed Work

- Kept Unity project-file and demo-scene presence checks behind `make check`.
- Preserved HTTPS registration-link and fixed-bug-note checks.
- Kept OAuth token and token-secret log redaction covered by the static checker.
- Added canonical `docs/plans` coverage to the Unity contract gate.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `git diff --check`
