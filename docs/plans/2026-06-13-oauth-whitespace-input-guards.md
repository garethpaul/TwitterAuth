---
title: "fix: Reject whitespace-only OAuth inputs"
type: fix
date: 2026-06-13
---

# Reject Whitespace-Only OAuth Inputs

## Status: Completed

## Context

The OAuth flow rejects null and empty credentials, tokens, and PIN values but
accepts whitespace-only strings. Those values can reach OAuth signing, network
request creation, or the browser authorization URL even though they cannot be
valid provider inputs.

## Requirements

- R1. Add one legacy-compatible helper that treats null, empty, and
  whitespace-only strings as missing without relying on newer framework APIs.
- R2. Use the helper for consumer keys and secrets before every signing path.
- R3. Use the helper for request tokens and PINs before access-token exchange
  or browser authorization.
- R4. Use the helper for access-token response fields before tweet signing.
- R5. Preserve redacted error messages, callbacks, and early coroutine exits.
- R6. Add static ordering and hostile-mutation coverage, then document actual
  verification and the unavailable Unity runtime.

## Scope Boundaries

This change does not trim values before signing, alter OAuth response parsing,
change endpoints, persist tokens, or revive the retired Twitter API.

## Implementation Units

### U1. Centralize Missing-Value Semantics

- **Files:** `UnityTwitter/Assets/Twitter.cs`
- Add a private helper using `string.IsNullOrEmpty(value) ||
  value.Trim().Length == 0`, then route OAuth input guards through it.

### U2. Enforce Guard Coverage

- **Files:** `scripts/check_unity_contracts.py`
- Require the helper and its use before request-token signing, access-token
  signing, browser launch, and tweet signing.

### U3. Document and Verify

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`, this plan.
- Record portable checks, mutations, and the Unity runtime limitation.

## Risks

- Trimming values for transmission could change signatures, so this change
  rejects whitespace-only inputs but otherwise preserves exact caller values.
- Static contracts cannot execute Unity coroutines or provider requests.

## Verification

- Focused OAuth input, browser authorization, access-token exchange, and
  consumer-credential contract functions: passed.
- `/tmp/engineering-bar/mutate-twitterauth-whitespace-inputs.sh`: rejected six
  helper, consumer-key, browser-token, PIN, request-response-token, and
  tweet-token empty-only mutations.
- `git diff --check`: passed.
- `make check`: passed all 17 Unity TwitterAuth contract groups; the build
  target truthfully reported that Unity is unavailable.
- `make -C /tmp/engineering-bar/twitterauth-whitespace-inputs-external/repo
  check`: passed the same portable gate from an external temporary path.
- Unity editor compilation and runtime execution: unavailable on this host.
