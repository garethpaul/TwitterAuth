# Access Token Input Guard

## Status: Completed

## Context

The Unity demo guarded the PIN button when no request token existed, but the
public `API.GetAccessToken` coroutine could still be called directly with a
missing request token or PIN. That path built an OAuth-signed request with empty
or invalid verifier state before surfacing the failure through Twitter.

## Objectives

- Preserve the legacy PIN-based access-token flow.
- Fail early when the request token or PIN is missing.
- Keep missing-input diagnostics redacted.
- Stop before constructing a signed access-token request.
- Extend static checks to preserve the guard.

## Work Completed

- Added an early `GetAccessToken` guard for missing request-token or PIN values.
- Failed the callback with `false, null` before any signed request is built.
- Logged a redacted missing-input message.
- Extended `scripts/check_unity_contracts.py`.
- Updated README, VISION, and CHANGES.

## Verification

- Negative check: `python3 scripts/check_unity_contracts.py` failed before the
  C# guard was added.
- `python3 scripts/check_unity_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Document secure token storage alternatives to plain PlayerPrefs.
- Add a no-post authentication-only demo path.
