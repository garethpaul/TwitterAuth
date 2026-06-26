# PIN Preflight Token Preservation

Status: Completed

## Problem

The demo stores instructional placeholder text as the PIN field value. Pressing
Enter PIN with that placeholder or surrounding whitespace copies and clears the
one-time request token before the API layer rejects the invalid PIN.

## Design

- Name the PIN placeholder as a constant.
- Treat empty, placeholder, and surrounding-whitespace PIN values as unusable.
- Require a usable PIN in the UI guard before copying or clearing the request
  token.
- Preserve the existing one-time token consumption and callback generation
  behavior once preflight succeeds.

## Verification Plan

Add a failing source contract and mutation, implement the guard, update public
guidance and `CHANGES.md`, then run `make check`, external-directory checks,
`git diff --check`, hosted checks, and exact-head review.

## Result

`PINIsReady` now rejects empty, placeholder, and surrounding-whitespace input
before the request token is copied or cleared. The focused hardening suite
rejects a mutation that removes this ordering guard. Root and
external-directory `make check`, Python compilation, and `git diff --check`
pass; Unity build skips without an absolute editor executable. Hosted checks
remain merge gates.
