# OAuth Response Field Uniqueness

## Status: Completed

## Context

OAuth response parsing now matches exact field names and decodes form values,
but `Regex.Match` accepts the first occurrence when a provider response repeats
a token or identity field. Ambiguous security-sensitive responses should fail
closed instead of selecting an attacker-influenced value by position.

## Requirements

- R1. Require exactly one exact-key occurrence for every field read through
  `FormValue`.
- R2. Return an empty value for missing or duplicated fields so existing
  request-token and access-token validation invokes the redacted failure path.
- R3. Preserve exact-key anchoring, form decoding, plus handling, malformed-
  escape rejection, and whitespace-only value rejection.
- R4. Do not log response bodies, duplicate values, tokens, or account identity.
- R5. Add static fixtures for duplicate request-token, token-secret, user-ID,
  and screen-name fields in leading and trailing positions.
- R6. Preserve the existing single-field success contract and callback flow.
- R7. Mutation tests must reject first-match behavior, relaxed match counts,
  missing duplicate fixtures, and stale plan status.

## Scope Boundaries

- Do not revive the retired provider integration, replace Unity `WWW`, add a
  query-string library, or change OAuth signing.
- Do not add real credentials or make provider requests.
- Unity editor and coroutine execution remain unavailable on this host.

## Implementation Units

### U1. Reject ambiguous exact-key fields

- **Files:** `UnityTwitter/Assets/Twitter.cs`
- Use exact-key `Regex.Matches` and return empty unless the count is exactly one.

### U2. Add fail-closed parser contracts

- **Files:** `scripts/check_unity_contracts.py`
- Require uniqueness logic and synthetic duplicate fixtures for all consumed
  OAuth response fields.

### U3. Preserve repository guidance

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Register and document the ambiguous-response boundary.

## Verification

- `python3 -B -c '...check_oauth_response_field_parsing()'` passed exact-key,
  uniqueness, decoding, malformed-input, and four-field duplicate fixtures.
- Full local, external-directory, and space-containing-path `make check` runs
  passed all 17 contract groups; Unity remains unavailable on this host.
- Seven hostile mutations covering first-match behavior, count relaxation,
  indexed-match drift, exact-key anchoring, removed field fixtures, and stale
  plan status were rejected.
- Python syntax, workflow YAML, SVG XML, `git diff --check`, generated-artifact,
  and focused secret reviews are included in final validation.
