# CI Baseline

Status: Completed

## Context

The legacy Unity OAuth sample had comprehensive static contracts but no hosted
workflow enforcing them on changes to authentication and logging code.

## Changes

- Added read-only GitHub Actions checks on Python 3.10, 3.12, and 3.14.
- Pinned actions to immutable commits and bounded job runtime.
- Extended repository contracts and documentation to protect the hosted gate.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_unity_contracts.py`
- `git diff --check`
