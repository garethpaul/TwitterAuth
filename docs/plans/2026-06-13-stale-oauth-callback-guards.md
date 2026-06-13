---
title: "fix: Ignore stale OAuth callbacks"
type: fix
date: 2026-06-13
---

# Ignore Stale OAuth Callbacks

## Status: Completed

## Context

The Unity demo keeps request-token and access-token responses in controller
fields. Starting a replacement attempt does not invalidate the previous state,
and callbacks do not prove that they belong to the latest coroutine. A failed
or late callback can therefore leave an older request token reusable or restore
credentials from a superseded authorization flow.

## Requirements

- R1. Assign monotonically increasing generations to request-token and
  access-token attempts.
- R2. Capture each generation in the callback passed to the existing API
  coroutine and ignore callbacks that do not match the current generation.
- R3. Clear request-token and access-token state when a replacement
  authorization flow starts.
- R4. Consume a request token before starting its access-token exchange so the
  PIN action cannot reuse it.
- R5. Clear the applicable state on current-generation failure while
  preserving redacted messages and existing success behavior.
- R6. Add portable fail-closed contracts and mutation coverage for generation
  capture, invalidation, callback ordering, one-time token use, documentation,
  and completed-plan status.

## Implementation Units

### U1. Bind callbacks to auth generations

- **Files:** `UnityTwitter/Assets/Demo.cs`
- Add separate request-token and access-token generation counters.
- Increment and capture the current generation when each coroutine starts.
- Return immediately from a callback whose captured generation no longer
  matches the controller state.

### U2. Invalidate and consume auth state

- **Files:** `UnityTwitter/Assets/Demo.cs`
- Clear both token response objects before a replacement request-token attempt.
- Copy and clear the request token before starting an access-token exchange.
- Clear failed current-generation response state without logging provider
  values or changing callback text.

### U3. Preserve the lifecycle contract

- **Files:** `scripts/check_unity_contracts.py`, `README.md`, `SECURITY.md`,
  `VISION.md`, `CHANGES.md`
- Add a focused static group covering generation ownership, state invalidation,
  one-time request-token use, callback order, and maintenance documentation.
- Register this completed plan with the canonical repository gate.

## Verification

- The focused stale-callback contract passed after implementation.
- The pre-completion repository gate passed all 18 non-plan contract groups.
- Sixteen hostile mutations covering missing generation capture, stale
  callback acceptance, retained replacement/failure state, request-token
  reuse, documentation drift, and stale plan status were rejected.
- Python checker syntax validation passed.
- Final local and external-working-directory `make check` runs are executed
  after this completed-plan record is written so the canonical plan contract
  validates the same state that is shipped.
- `make build` truthfully skipped Unity editor compilation because `unity` is
  unavailable on this host; no coroutine, browser, or provider behavior is
  claimed.

## Work Completed

- Added separate request-token and access-token generations and captured each
  generation in the corresponding coroutine callback.
- Cleared prior auth state before replacement attempts, invalidated the other
  stage where required, and ignored superseded callbacks before assignment.
- Copied and cleared request-token state before access-token exchange so a PIN
  action cannot reuse the same request token.
- Cleared current-generation failure state while preserving existing redacted
  messages and success behavior.

## Scope Boundaries

- Do not change API helper signatures, OAuth endpoints, persistence, GUI
  layout, provider error messages, or the retired integration itself.
- Do not add cancellation infrastructure, dependencies, or broad Unity
  modernization.
- Do not merge or close any pull request without explicit owner authorization.
