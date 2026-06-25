# Authentication-Only Scene Default

## Status: Completed

## Priority

1. Prevent checked-in Unity scene serialization from overriding the safe
   source-level posting default.
2. Add a hostile binary mutation that proves the invariant is enforced.
3. Keep the legacy scene bytes unchanged and avoid unsupported editor claims.

## Context

`ALLOW_TWEET_POSTING` is a public Unity field. Although its C# declaration
defaults false, a future Inspector save could serialize the field into
`Demo.unity` and silently alter fresh-checkout behavior. The legacy scene is a
Unity 4.3.4f1 binary and currently omits the new field token.

## Requirements

- R1. Require the checked-in Demo scene to omit `ALLOW_TWEET_POSTING` bytes.
- R2. Keep the binary scene itself unchanged.
- R3. Reject a focused mutation that appends the serialized field token.
- R4. Run the mutation from the public `make test` gate.
- R5. Document why source and scene defaults must remain aligned.

## Implementation Units

### U1. Expose the scene predicate

**Files:** `scripts/check_unity_contracts.py`

Add a reusable byte-level predicate and call it from the registered
authentication-only contract.

### U2. Prove mutation rejection

**Files:** `scripts/test_authentication_only_scene_contract.py`, `Makefile`

Verify the baseline scene is accepted, append an exact posting-field token,
and require rejection. Register the focused test in `make test`.

### U3. Record the serialization boundary

**Files:** `README.md`, `SECURITY.md`, `VISION.md`, `AGENTS.md`, `CHANGES.md`,
`docs/plans/2026-06-25-authentication-only-scene-default.md`

Document that checked-in scene bytes must not carry the posting opt-in.

## Verification Plan

- Prove the focused test fails before the predicate exists.
- Run the focused mutation and canonical checker.
- Run `make check` from the root and an external directory.
- Compile Python, inspect the exact diff, and run exact-head Codex review.

## Scope Boundaries

- Do not edit or reserialize `Demo.unity`.
- Do not infer the value of arbitrary future Unity binary fields.
- Do not change runtime OAuth or posting behavior.
- Do not claim Unity editor or provider execution.

## Work Completed

- Added a reusable scene-byte predicate and canonical assertion.
- Added and registered one hostile serialized-field mutation.
- Synchronized public, security, roadmap, contributor, maintenance, and plan
  guidance.

## Verification

- The focused test failed on the missing predicate before implementation on
  2026-06-25.
- The focused mutation and canonical 25-contract checker passed after the fix
  on 2026-06-25.
- `/usr/bin/python3 -m py_compile scripts/check_unity_contracts.py scripts/test_authentication_only_scene_contract.py`
  passed on 2026-06-25.
- Root and external-directory `/usr/bin/make check` both passed 25 canonical
  contracts, 30 Make authority cases, 4 cache mutations, 1 scene mutation, 6
  callback mutations, and 9 OAuth mutations on 2026-06-25.
- `git diff --check` passed and `Demo.unity` remained unchanged.
- No Unity editor or live provider request was used.
