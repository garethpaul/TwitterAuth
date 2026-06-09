# Consumer Credential Guards

## Status: Completed

## Context

The Unity demo UI avoids starting OAuth when `CONSUMER_KEY` or
`CONSUMER_SECRET` is empty. The public API helpers could still be called
directly with missing consumer credentials and would build signed OAuth
requests before failing at the network/API layer.

## Objectives

- Preserve the existing request-token, access-token, and tweet-post flows.
- Stop request signing when the consumer key or secret is missing.
- Fail callbacks with non-secret, generic credential-missing messages.
- Reuse one credential guard across the API helpers.
- Extend static checks so direct API calls remain protected.

## Work Completed

- Added `ConsumerCredentialsAreMissing` to centralize missing consumer key or
  secret checks.
- Guarded `GetRequestToken` before calling `WWWRequestToken`.
- Guarded `GetAccessToken` before request-token/PIN validation and
  `WWWAccessToken` signing.
- Guarded `PostTweet` before access-token validation and signed tweet
  requests.
- Extended `scripts/check_unity_contracts.py` with API-level consumer
  credential guard checks and completed-plan coverage.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `git diff --check`

## Unity Notes

Unity was unavailable on this host, so editor/runtime validation was not run
here. The repository `make check` wrapper still runs the Unity build path when
`unity` is installed locally.

## Follow-Up Candidates

- Surface credential-missing state in the demo UI instead of only logging.
- Document secure local credential configuration for revived Unity usage.
