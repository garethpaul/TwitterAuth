# Authentication-Only Demo Mode

## Status: Completed

## Priority

1. Make authentication-only testing the safe default for the legacy demo.
2. Require an explicit, visible Inspector opt-in before tweet controls appear.
3. Preserve the existing PIN OAuth flow and live-post behavior when enabled.
4. Add mutation-sensitive static evidence without claiming runtime validation.

## Context

The Demo scene always rendered tweet composition and posting controls after the
PIN controls. That made the historical authentication flow unnecessarily easy
to turn into a live posting exercise and did not provide the no-post path named
in the project roadmap.

## Requirements

- R1. Add a public `ALLOW_TWEET_POSTING` Inspector setting that defaults false.
- R2. Keep request-token, browser authorization, PIN, and access-token behavior
  available while posting is disabled.
- R3. Show a visible authentication-only label and return before tweet input or
  `API.PostTweet` can be reached.
- R4. Preserve existing posting behavior when the setting is enabled.
- R5. Register a static contract for default state, guard ordering,
  documentation, plan evidence, and checker registration.
- R6. Document that live posting requires deliberate test-account opt-in.

## Implementation Units

### U1. Gate posting controls

**Files:** `UnityTwitter/Assets/Demo.cs`

Add the default-false Inspector setting and stop the OnGUI path after the PIN
flow when posting has not been explicitly enabled.

### U2. Enforce the safe default

**Files:** `scripts/check_unity_contracts.py`

Require the uninitialized public flag, visible label, and ordered early return
before tweet composition and posting. Require the contract to remain registered
and tied to completed plan evidence.

### U3. Record the live-post boundary

**Files:** `README.md`, `SECURITY.md`, `VISION.md`, `AGENTS.md`, `CHANGES.md`,
`docs/plans/2026-06-25-authentication-only-demo.md`

Document authentication-only use, explicit posting opt-in, and the lack of
local Unity/provider runtime validation.

## Verification Plan

- Prove the focused contract fails before adding the Inspector opt-in.
- Reject isolated mutations that remove the guard or enable posting by default.
- Run `make check`, Python compilation, diff hygiene, and exact-head review.
- Inspect hosted checks without attempting a provider request or live tweet.

## Scope Boundaries

- Do not change OAuth signing, token exchange, callback, or posting semantics.
- Do not modify the Unity scene serialization or invent a Unity version.
- Do not make provider calls, store credentials, or claim runtime execution.
- Do not modernize legacy OnGUI, `WWW`, or C# syntax in this focused change.

## Work Completed

- Added a default-false posting flag and visible authentication-only path.
- Added and registered a static ordering and documentation contract.
- Synchronized public usage, security, roadmap, contributor, and maintenance
  guidance.

## Verification

- The focused contract failed on the missing opt-in before production code was
  changed on 2026-06-25.
- Source mutations removing the guard or enabling posting by default were both
  rejected for the intended contract violations on 2026-06-25.
- `/usr/bin/python3 -m py_compile scripts/check_unity_contracts.py` passed on
  2026-06-25.
- `/usr/bin/make check` passed 25 canonical contracts, 30 Make authority cases,
  and the existing 4 cache, 6 callback, and 9 OAuth hostile mutations on
  2026-06-25.
- The same full `make check` gate passed through the repository Makefile from
  `/tmp` on 2026-06-25.
- Unity editor and retired provider execution were unavailable on this Linux
  host, so no runtime or live-post claim is made.
