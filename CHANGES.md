# Changes

## 2026-06-09

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
