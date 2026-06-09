# OAuth Response Log Redaction

## Status: Completed

## Context

The Unity demo already redacted successful request-token and access-token logs,
but the OAuth API helper still printed the raw response body when token parsing
failed. A partial OAuth response can contain request tokens, access tokens, or
token secrets even when another required field is missing, so failure logging
should not include the response body.

## Objectives

- Preserve the legacy OAuth request-token and access-token flow.
- Avoid logging raw OAuth response bodies on parse failures.
- Keep missing-field diagnostics useful without exposing tokens.
- Extend static checks to preserve API-level log redaction.

## Work Completed

- Replaced raw request-token response logging with a redacted missing-field
  message.
- Replaced raw access-token response logging with a redacted missing-field
  message.
- Added static checker coverage that rejects the old raw response-body logs.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Document secure token storage alternatives to plain PlayerPrefs.
- Add a no-post authentication-only demo path.
