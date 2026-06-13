---
title: "fix: Ignore stale OAuth callbacks"
type: fix
date: 2026-06-13
---

# Ignore Stale OAuth Callbacks

## Status: Planned

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

- Run the focused stale-callback contract before the full local and
  external-working-directory `make check` gates under explicit timeouts.
- Reject hostile mutations for missing generation capture, stale callback
  acceptance, missing state resets, request-token reuse, ordering drift,
  documentation removal, and stale plan status.
- Validate Python syntax, workflow YAML, Unity project metadata, intended
  paths, generated artifacts, whitespace, conflict markers, and changed-line
  secret patterns.
- Report Unity editor and coroutine runtime execution as unavailable on this
  host; do not claim provider or browser behavior that was not exercised.

## Scope Boundaries

- Do not change API helper signatures, OAuth endpoints, persistence, GUI
  layout, provider error messages, or the retired integration itself.
- Do not add cancellation infrastructure, dependencies, or broad Unity
  modernization.
- Do not merge or close any pull request without explicit owner authorization.
