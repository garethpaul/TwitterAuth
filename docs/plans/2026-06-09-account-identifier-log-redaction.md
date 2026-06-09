# Account Identifier Log Redaction

Status: Completed

## Context

The Unity demo already redacted request tokens, access tokens, and token
secrets from successful OAuth logs. Those same log messages still printed
Twitter user IDs and screen names after loading saved credentials or completing
the access-token callback. Account identifiers are not secrets, but they are
user-specific data and should not be written to console logs by default.

## Plan

- Preserve the demo UI behavior that can show the signed-in account name on the
  login button.
- Redact Twitter user IDs and screen names from successful OAuth console logs.
- Extend `scripts/check_unity_contracts.py` so future changes cannot re-add
  user ID or screen-name concatenation to demo logs.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

On this host, `make verify` runs the static checks and skips Unity execution
because no `unity` binary is installed.
