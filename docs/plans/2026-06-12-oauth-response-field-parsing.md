# OAuth Response Field Parsing

Status: Completed

## Problem

Request-token and access-token responses extract fields with unanchored regular
expressions such as `oauth_token=...`. Those patterns can match inside a
different key like `shadow_oauth_token`, and returned values remain form
encoded. Provider responses should be parsed by exact field name and malformed
escaping should fail closed without logging response contents.

## Plan

1. Add one helper that finds form fields only at the start of the response or
   after `&`, using an escaped exact key.
2. Decode `+` and percent escapes, returning an empty value for a missing field
   or malformed escape sequence.
3. Route request-token, token-secret, user ID, and screen-name extraction
   through the helper while preserving existing missing-field callbacks.
4. Extend static contracts to reject unanchored direct extraction and require
   exact-key, decoding, and fail-closed behavior.

## Verification

- `make check` passed 16 static contract groups; Unity reported the documented
  host-toolchain skip.
- An external-working-directory Make invocation passed the same gate.
- Controlled mutations removing exact-key anchoring, restoring direct token
  extraction, and broadening malformed-decoding handling were rejected.
- `python3 -m py_compile scripts/check_unity_contracts.py` passed.
- `git diff --check` passed.

Unity compilation remains unclaimed because the historical Unity editor and
matching runtime toolchain are unavailable on this host.
