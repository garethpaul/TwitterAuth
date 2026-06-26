# Post Tweet Ownership

Status: Completed

## Problem

When live posting was explicitly enabled, every click on `Post Tweet` started a
new irreversible network side effect. The demo had no owner for the active
submission, so rapid clicks could publish duplicate statuses and a callback
could still update demo state after the component was disabled.

## Decision

- Keep authentication-only mode and the explicit Inspector opt-in unchanged.
- Allow only one active post coroutine at a time.
- Capture a monotonically increasing generation before starting the coroutine.
- Ignore completions whose generation no longer belongs to the demo.
- Invalidate the generation and clear local ownership when the component is
  disabled.

## Verification

- A focused source contract failed before the generation, in-flight guard, and
  lifecycle invalidation existed.
- Eight hostile mutations cover guard removal, ownership ordering, generation
  capture and callback binding, stale completion acceptance, and ownership
  release.
- `make check` runs the focused mutation suite with the full portable gate.
- Live posting remains unexecuted because it requires a compatible legacy Unity
  editor, provider availability, explicit credentials, and a safe test account.
