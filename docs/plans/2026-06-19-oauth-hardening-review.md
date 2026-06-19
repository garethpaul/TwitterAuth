# OAuth Hardening Review

Status: Completed

## Problem

The reviewed PR stack improved OAuth parsing, callback ownership, timestamp
formatting, and validation, but executable probes found four remaining boundary
defects:

- `Uri.UnescapeDataString` accepted malformed percent escapes and invalid UTF-8
  as token evidence instead of failing closed.
- OAuth values with accidental leading or trailing whitespace passed the
  missing-value guard and could reach browser, signing, or provider boundaries.
- `Convert.ToInt64(double)` rounded timestamps during the latter half of a
  second, allowing a signed request to claim the next Unix second.
- signature parameters were sorted before percent encoding and with the
  process string comparer rather than encoded ordinal ordering.
- disabling the Unity demo did not invalidate pending request/access token
  callbacks, allowing hidden lifecycle state to be restored later.

## Implementation

1. Decode percent runs with strict UTF-8 and reject malformed escapes or
   decoded control characters.
2. Reject surrounding whitespace without silently rewriting opaque OAuth
   values.
3. Truncate positive Unix elapsed seconds before invariant decimal formatting.
4. Percent-encode parameter names and values before ordinal sorting and base
   string construction.
5. Invalidate both callback generations and clear pending request-token state
   from `OnDisable`.
6. Add mutation-sensitive static contracts and run them from `make check`.

## Verification

- Red-first `scripts/test_oauth_hardening_contract.py` failed against the
  reviewed stack and now rejects nine hostile mutations.
- A Mono C# probe verifies malformed escapes, invalid UTF-8, and decoded NUL
  values fail closed while valid form values still decode.
- The full `Twitter.cs` and `Demo.cs` sources compile with `mcs` against narrow
  Unity API stubs.
- `make check`, external-directory `make check`, and `git diff --check` pass.
- Unity editor execution and credential-backed Twitter OAuth/posting remain
  unavailable and are not claimed.
