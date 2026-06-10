# Session-Only OAuth Tokens

Status: Completed

## Context

The Unity demo stored long-lived Twitter access tokens, token secrets, and
account identifiers in `PlayerPrefs`. Unity preferences are not a secure
credential store and can expose account access on a shared or compromised
device.

## Changes

- Kept successful OAuth credentials in memory for the active demo session.
- Stopped reading or writing OAuth values through `PlayerPrefs`.
- Deleted the four legacy preference keys on startup to migrate existing users
  away from plaintext local credential storage.
- Added static contracts for session-only storage, stable CI runners, and
  root-independent local verification.

## Verification

- `make check`
- `python3 -m py_compile scripts/check_unity_contracts.py`
- Mutation checks for OAuth storage, migration, CI, and Makefile contracts
- `git diff --check`

The Unity editor is not installed on this host, so no engine build is claimed.
