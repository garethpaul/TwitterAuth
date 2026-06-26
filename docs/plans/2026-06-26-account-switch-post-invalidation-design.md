# Account-Switch Post Invalidation Design

Status: Completed

## Context

The demo generation-binds explicit live-post completions and invalidates them
when the component is disabled. The same ownership boundary is missing when the
user clicks the login button to register a different account: request/access
token state is replaced, but an earlier account's post generation remains
current. Its eventual completion is therefore accepted and reported after the
account switch began.

## Options Considered

1. Leave post ownership independent from authentication replacement. This
   accepts stale completion reporting from the prior account and was rejected.
2. Inline generation increment and ownership clearing in the login button. This
   fixes the immediate path but duplicates the existing disable lifecycle logic.
3. Extract one private invalidation helper and call it before replacement auth
   state and from `OnDisable`. This keeps one ordering contract and preserves the
   current public API and coroutine implementation.

## Decision

Use option 3. `InvalidatePostTweetOwnership()` increments the post generation
and clears the local in-flight owner. The login button calls it before clearing
request/access token state or launching a replacement request-token coroutine;
`OnDisable` calls the same helper.

The helper cannot revoke a provider request already transmitted. It guarantees
only that the prior request no longer owns current UI/lifecycle completion state.

## Verification

- Extend the focused post-ownership contract first and observe failure because
  replacement authentication lacks post invalidation.
- Implement the helper and both call sites.
- Reject mutations that remove the helper, reorder account-switch invalidation,
  or bypass either call site.
- Run root/external Make gates and hosted checks on the exact PR head.
- The final local gate is `make check`.
