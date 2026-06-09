# TwitterAuth PIN Guard

Status: Completed

## Scope

Prevent the legacy Unity demo from dereferencing a missing request token when a
user presses the PIN submission button before the OAuth request-token step has
succeeded.

## Completed Work

- Guarded PIN submission with a request-token presence check.
- Added a user-visible skipped-flow message for missing request-token state.
- Extended the static Unity contract checker to require the guard.
- Documented the guard in README, VISION, and CHANGES.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- `git diff --check`

Unity editor validation remains follow-up work on a host with the matching
legacy Unity toolchain.
