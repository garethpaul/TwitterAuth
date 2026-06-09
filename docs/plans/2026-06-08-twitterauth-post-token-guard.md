# TwitterAuth Post Token Guard

## Status: Completed

## Context

The Unity demo already guarded PIN submission when no request token was
available. The tweet submission path could still call `API.PostTweet` before an
access token and token secret existed, allowing the OAuth signing helper to
dereference missing token state.

## Objectives

- Preserve the OAuth and tweet-posting sample flow.
- Guard the Post Tweet button until access-token state exists.
- Guard `API.PostTweet` itself before signing requests.
- Keep missing-token feedback redacted and user-visible in logs.
- Extend static checks to preserve the guard.

## Work Completed

- Added access-token presence checks before starting the post-tweet coroutine.
- Added an `API.PostTweet` guard for missing token/token-secret state.
- Stopped the coroutine with `yield break` before building signed requests.
- Extended `scripts/check_unity_contracts.py`.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Add a no-post authentication-only demo path.
- Document secure token storage alternatives to plain PlayerPrefs.
