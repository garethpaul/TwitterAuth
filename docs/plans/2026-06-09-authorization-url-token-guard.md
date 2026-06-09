# Authorization URL Token Guard

## Status: Completed

## Context

The OAuth helper opened the authorization page by interpolating the request
token directly into the URL. The demo normally calls that helper only after a
successful request-token response, but the public helper still allowed missing
tokens and did not encode token values before placing them in the query string.

## Objectives

- Preserve the legacy PIN-based authorization flow.
- Avoid opening the authorization page when no request token exists.
- URL-encode request tokens before inserting them into the authorization URL.
- Add static checker coverage for the guard and encoded URL construction.

## Work Completed

- Added a missing-token guard to `API.OpenAuthorizationPage`.
- Logged a redacted missing-token message instead of opening an invalid URL.
- Encoded request tokens with the existing OAuth URL encoder.
- Extended `scripts/check_unity_contracts.py`.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Document secure token storage alternatives to plain PlayerPrefs.
- Add a no-post authentication-only demo path.
