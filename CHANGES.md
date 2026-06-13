# Changes

## 2026-06-13

- Ignored superseded OAuth callbacks with per-stage generations, cleared prior
  auth state on replacement attempts, and consumed request tokens once.
- Required every consumed OAuth token and identity response field to occur
  exactly once, rejecting ambiguous duplicated fields through redacted paths.
- Added exact-key duplicate fixtures for request tokens, token secrets, user
  IDs, and screen names.
- Rejected whitespace-only OAuth credentials, request tokens, PINs, and access
  token fields before signing, network exchange, or browser authorization.

## 2026-06-12

- Replaced unanchored OAuth response regex extraction with exact-key form
  parsing, percent decoding, and fail-closed malformed-escape handling.
- Ignored Python bytecode caches produced by local contract compilation.

## 2026-06-10

- Replaced provider-controlled OAuth transport and tweet response error details
  in Unity logs with stable redacted failure messages.
- Stopped loading or saving long-lived OAuth values through `PlayerPrefs`, kept
  credentials session-only, and deleted legacy plaintext preference values on
  startup.
- Made local verification root-independent and fixed hosted runner and action
  release annotations to reviewed versions.
- Added a pinned, read-only GitHub Actions matrix on Python 3.10, 3.12, and
  3.14 that disables checkout credential persistence and runs the static
  `make check` baseline.
- Extended the Unity contract checker to require the CI workflow and completed
  CI plan.
- Bound the checkout credential-persistence assertion to the checkout step so
  moving the setting to another action cannot satisfy the hosted CI contract.

## 2026-06-09

- Redacted Twitter user IDs and screen names from successful OAuth demo logs.
- Added static checker coverage for account-identifier log redaction.
- Redacted tweet text from `PostTweet` validation failure logs.
- Extended static checker coverage for tweet-text validation log redaction.
- Guarded request-token, access-token, and tweet-post API helpers when consumer
  credentials are missing before signed requests are built.
- Added static checker coverage for API-level consumer credential guards.
- Guarded authorization-page launches when the request token is missing.
- URL-encoded request tokens before interpolating them into authorization URLs.
- Guarded access-token exchanges when the request token or PIN is missing.
- Added static checker coverage for access-token exchange input guards.
- Replaced predictable `System.Random` OAuth nonce generation with
  cryptographic random bytes.
- Added static checker coverage for OAuth nonce entropy.
- Replaced raw OAuth response-body failure logs with redacted missing-field
  messages in the request-token and access-token helper paths.
- Added static checker coverage for API-level OAuth response log redaction.

## 2026-06-08

- Guarded tweet submission when the Unity demo does not yet have an access
  token.
- Guarded PIN submission when the Unity demo does not yet have a request token.
- Added canonical `docs/plans` coverage to the Unity static contract checker.
- Redacted request/access token and token-secret values from Unity demo logs.
- Added a static contract for token-log redaction and `make check` as the
  shared verification alias.
- Added a `make verify` static gate for Unity project files and runtime URL security.
- Moved the demo registration link from plain HTTP to HTTPS.
- Marked the existing plain-HTTP runtime endpoint bug note as fixed.
