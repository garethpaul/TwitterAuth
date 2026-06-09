# OAuth Nonce Entropy

## Status: Completed

## Context

The OAuth helper generated request nonces with `System.Random`. That generator
is predictable and can repeat across nearby process starts, which weakens OAuth
request signing and can cause avoidable nonce collisions.

## Objectives

- Preserve the legacy OAuth signing flow.
- Replace predictable nonce generation with cryptographic random bytes.
- Keep generated nonce values header-safe without separators.
- Add static checker coverage for nonce entropy.

## Work Completed

- Updated `GenerateNonce` to draw 16 bytes from `RNGCryptoServiceProvider`.
- Formatted nonce bytes as uppercase hex without separator characters.
- Added static checker coverage that rejects `System.Random` nonce generation.
- Updated README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `make verify`
- `git diff --check`

## Follow-Up Candidates

- Document secure token storage alternatives to plain PlayerPrefs.
- Add a no-post authentication-only demo path.
