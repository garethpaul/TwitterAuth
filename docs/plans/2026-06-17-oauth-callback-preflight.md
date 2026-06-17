# OAuth Callback Preflight

## Status: Completed

## Priority

1. Prevent null callback delegates from crashing public OAuth and posting
   coroutine entry points.
2. Reject invalid callback ownership before credentials, signing, or network
   construction.
3. Keep diagnostics redacted and preserve all existing success/failure callback
   behavior for valid callers.
4. Add mutation-sensitive contracts for every public coroutine boundary.

## Context

`API.GetRequestToken`, `API.GetAccessToken`, and `API.PostTweet` invoke their
callback delegates on validation, transport, and response paths without first
checking whether the delegate exists. A caller mistake can therefore produce a
`NullReferenceException`, including after a provider request has already been
sent.

## Requirements

- R1. Guard a missing callback at the start of each public coroutine.
- R2. Log only a fixed operation-specific callback-missing diagnostic.
- R3. Stop before consumer credential checks, OAuth value checks, signing,
  form/header construction, or network creation.
- R4. Preserve all existing callback invocations and results for non-null
  delegates.
- R5. Add a registered focused contract covering all three operations,
  preflight ordering, redacted diagnostics, and completed-plan evidence.
- R6. Synchronize README, security, roadmap, and change guidance.

## Implementation Units

### U1. Fail closed on missing delegates

**Files:** `UnityTwitter/Assets/Twitter.cs`

Add a callback-null preflight to the request-token, access-token, and tweet
coroutines. Each guard emits a fixed message and exits without constructing a
request.

### U2. Enforce callback preflight ordering

**Files:** `scripts/oauth_callback_preflight_contract.py`,
`scripts/test_oauth_callback_preflight_contract.py`,
`scripts/check_unity_contracts.py`, `Makefile`

Require each callback guard and operation-specific diagnostic before the first
credential or token validation. Register the contract in the canonical gate
and require completed plan evidence.

### U3. Record the API boundary

**Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`,
`docs/plans/2026-06-17-oauth-callback-preflight.md`

Document that public OAuth and posting coroutines reject missing callback
delegates before performing security-sensitive or network work.

## Verification Plan

- Run the focused checker and full repository/external-directory `make check`.
- Reject isolated mutations removing each callback guard, moving a guard after
  credentials, weakening a diagnostic, removing checker registration, or
  falsifying plan status/evidence.
- Compile the checker and audit the exact diff, generated artifacts, conflict
  markers, file modes, and credential-like additions.
- Capture one bounded exact-head hosted and security snapshot after push.

## Scope Boundaries

- Do not redesign callback types, add Tasks/events, migrate `WWW`, modernize
  Unity/C# syntax, or change valid-caller callback counts.
- Do not add retries, timeouts, live provider calls, or claim Unity runtime
  execution from Linux.
- Do not merge or close the existing stacked pull requests.

## Work Completed

- Added first-statement null-callback guards to request-token, access-token,
  and tweet-post coroutines with fixed redacted diagnostics.
- Added a reusable callback preflight ordering contract, registered it in the
  canonical checker, and wired six focused hostile mutations into `make test`.
- Synchronized the public API boundary across README, security, roadmap, and
  change guidance.

## Verification

- `python3 -m py_compile scripts/check_unity_contracts.py scripts/oauth_callback_preflight_contract.py scripts/test_oauth_callback_preflight_contract.py`
  passed on 2026-06-17.
- `python3 scripts/test_oauth_callback_preflight_contract.py` passed all six
  callback guard, ordering, diagnostic, and exit mutations on 2026-06-17.
- `make check` passed from the repository root on 2026-06-17 with 22 canonical
  contracts and six callback preflight mutations; Unity execution was skipped
  because the editor is unavailable on this Linux host.
- `make -f /home/gjones/code/private/worktrees/twitterauth-invariant-oauth-timestamp-20260616/Makefile check`
  passed from `/tmp` with the same 22 contracts, six mutations, and truthful
  Unity-editor skip on 2026-06-17.
