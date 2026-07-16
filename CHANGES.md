# Changes

## 2026-07-16 - P2 - Make the C# source contracts comment-aware

### Summary

The static contracts asserted raw C# source text, so commenting a guard out kept
every asserted literal present verbatim and left the contract green while the
guard became dead code. The authentication-only posting guard was fully exposed:
`make check` passed with the guard commented out in either C# comment form.

This is a verification gap, not a live defect. The checked-in C# is unchanged and
was correct before and after; what changed is that the gate can now detect a
commented-out guard.

### Work completed

- Added `scripts/csharp_source.py` with `blank_comments`, a scanner that tracks
  regular, verbatim (`@""`), and interpolated (`$"`) string literals, character
  literals, and escapes. Comments are blanked to spaces, so byte offsets are
  preserved and contracts that locate a `// PIN Input` style section marker in
  raw source still index correctly. A regex or `line.split("//")[0]` stripper
  was rejected: it truncates `Application.OpenURL("https://dev.twitter.com/apps/new")`
  and would fail correct source.
- Moved the Demo.cs authentication-only assertions into
  `scripts/authentication_only_contract.py` so the mutation test exercises the
  shipped contract rather than a copy of it.
- Made `scripts/post_tweet_ownership_contract.py` assert comment-blanked source
  while still locating the `// PIN Input` marker in raw source.
- Scoped deliberately: checks that assert prose or comment text keep reading raw
  source.

### Files changed

- `scripts/csharp_source.py` and `scripts/test_csharp_source.py` — the scanner
  and its 25 executable cases.
- `scripts/authentication_only_contract.py` and
  `scripts/test_authentication_only_demo_contract.py` — the extracted contract
  and seven hostile mutations, including both comment forms.
- `scripts/check_unity_contracts.py` — delegate the Demo.cs authentication-only
  assertions to the shared contract.
- `scripts/post_tweet_ownership_contract.py` and
  `scripts/test_post_tweet_ownership_contract.py` — comment-aware assertions and
  four added comment-form mutations (ten to fourteen).
- `Makefile` — run the two new suites from `make test`.

### Validation

- Measured before the fix, with each mutation's application verified on disk:
  block-commenting and line-commenting the `if (!ALLOW_TWEET_POSTING)` guard both
  left `make check` green (exit 0); deleting the same guard was caught. That
  control discrimination proves the contract was live but comment-blind.
- Block-commenting the `OnPostTweet` stale-generation guard left the contract
  itself green; `make check` failed only because the test harness noticed its own
  exact-whitespace mutation no longer applied, which is an incidental catch and
  not detection.
- Block-commenting `InvalidatePostTweetOwnership();` in `OnDisable` was a second
  measured blind spot in the post-ownership contract.
- Two of the four added post-ownership mutations were measured green against the
  previous raw-source contract; the other two were already rejected, but only
  incidentally, because line comments shift asserted indentation and dropping
  `else` removes an asserted literal.
- After the fix all six probes are rejected by the contract with a real
  diagnostic.
- `make check` passes: 26 canonical checks, 30 Make authority cases, 25 comment
  scanner cases, seven authentication-only demo mutations, fourteen
  post-ownership mutations, ten OAuth hardening mutations, six callback
  mutations, four cache mutations, and one scene mutation.
- Not verified: no .NET toolchain was available, so no mutation was compiled. The
  Unity build step remains skipped.

## 2026-06-26 13:20 PDT - P1 - Invalidate prior-account post completions

### Summary

Bound replacement authentication to the existing live-post lifecycle so a
completion from the prior account cannot remain current after OAuth state is
cleared and a different account flow begins.

### Work completed

- Added one shared post-ownership invalidation helper for generation advance
  and local in-flight release.
- Starting replacement authentication invalidates the prior account's post completion before OAuth state is cleared.
- Reused the same helper when the demo component is disabled.
- Expanded the focused contract from eight to ten hostile mutations, covering
  missing account-switch invalidation and incorrect ordering.

### Threads

- Started: none; the focused lifecycle correction was handled directly.
- Continued: none.
- Stopped: none.

### Files changed

- `UnityTwitter/Assets/Demo.cs` — invalidate post ownership before replacement
  OAuth state and share the disable lifecycle helper.
- `scripts/post_tweet_ownership_contract.py` and
  `scripts/test_post_tweet_ownership_contract.py` — enforce the helper and both
  lifecycle call sites.
- Guidance and plan files — document the account-switch boundary and runtime
  limit for already transmitted provider requests.

### Validation

- Red-first focused suite failed on the missing helper, missing account-switch
  ordering, and missing disable reuse.
- The repaired focused suite rejected ten hostile mutations.
- All six Make aliases passed from the repository root and an external
  directory: 26 canonical checks, 30 Make authority cases, ten post-ownership
  mutations, ten OAuth hardening mutations, six callback mutations, four cache
  mutations, and one scene mutation.
- The unrelated OAuth lifecycle mutation fixture was updated to the shared
  invalidation helper shape after the first full gate exposed its stale block.
- Unity build remains skipped without an absolute legacy editor executable.

### Bugs / findings

- P1 lifecycle correctness: clicking “register with a different Twitter
  account” replaced token state without invalidating the prior account's post
  generation, allowing its completion to be accepted afterward.

### Blockers

- A provider request already transmitted cannot be revoked by this local
  generation guard; the fix prevents stale completion ownership and reporting.

### Next action

- Run final audits, hosted checks, and exact-head review, then merge only the
  unchanged green PR head.

## 2026-06-26 04:42 PDT - P1 - Own explicit live-post submissions

### Summary

Prevented rapid `Post Tweet` clicks from starting concurrent irreversible
submissions and prevented disabled demo components from accepting stale post
completions.

### Work completed

- Added a single in-flight post owner and monotonically increasing generation.
- Bound each completion to its captured generation and released ownership only
  for the current request.
- Invalidated pending completions and cleared local ownership on disable.
- Added a focused portable contract, eight hostile mutations, public gate
  wiring, synchronized guidance, and a completed implementation plan.

### Validation

- The focused contract failed before the in-flight owner, generation binding,
  and lifecycle invalidation existed.
- Root and external-directory `make check` pass all 26 static checks, 30 Make
  authority cases, eight post-ownership mutations, and the existing cache,
  scene, callback, and OAuth mutation suites. Python compilation, shell syntax,
  and `git diff --check` also pass.
- Hosted validation remains a merge gate for the exact PR head; Unity live
  posting is intentionally not exercised without a safe test account and
  compatible editor.

### Blockers

- The retired provider flow cannot be verified locally without legacy Unity,
  explicit credentials, provider availability, and a dedicated test account.

## 2026-06-26 04:31 PDT - P2 - Preserve request tokens on invalid PIN input

### Summary

Rejected the instructional PIN placeholder and surrounding-whitespace PIN text
before the demo copies or clears its retained one-time request token.

### Work completed

- Named the PIN placeholder, added a reusable UI preflight, and kept valid PIN
  exchange ordering unchanged.
- Added the preflight to OAuth hardening contracts and a hostile mutation that
  removes it.
- Updated usage, security, roadmap, contributor, and plan guidance.

### Validation

- The focused hardening contract failed before implementation because no PIN
  preflight preceded token consumption.
- The repaired contract rejects 10 hostile mutations. Root and
  external-directory `make check`, all 25 static checks, 30 Make authority
  cases, generated-cache, scene, callback, and OAuth mutation suites, Python
  compilation, and `git diff --check` pass. Unity build skips because no
  absolute editor executable is configured; hosted checks remain merge gates.

### Blockers

- Live PIN OAuth still requires a compatible legacy Unity editor, test
  credentials, provider availability, and a test account.

## 2026-06-25 11:40 PDT - P2 - Guard the serialized no-post default

### Summary

Protected the checked-in binary Demo scene from silently serializing the public
tweet-posting opt-in. The source default and committed scene now have one
mutation-tested authentication-only boundary.

### Work completed

- Added a binary-scene helper that requires `Demo.unity` to omit the
  `ALLOW_TWEET_POSTING` field token.
- Added a hostile mutation that appends the serialized field token and proves
  the canonical safety predicate rejects it.
- Registered the focused mutation in `make test` and synchronized usage,
  security, roadmap, contributor, and plan guidance.

### Threads

- Started: none; the focused checker gap was fixed directly.
- Continued: none.
- Stopped: none.

### Files changed

- `scripts/check_unity_contracts.py` — enforced the binary scene invariant.
- `scripts/test_authentication_only_scene_contract.py` — added the hostile
  serialized-field mutation.
- `Makefile` — registered the focused mutation in the public test gate.
- `README.md`, `SECURITY.md`, `VISION.md`, `AGENTS.md` — documented the scene
  and source default boundary.
- `docs/plans/2026-06-25-authentication-only-scene-default.md` — recorded scope
  and verification evidence.

### Validation

- Red-first focused test — failed on the missing scene predicate import before
  checker implementation.
- Focused scene mutation — passed and rejected one appended posting-field token.
- Initial `/usr/bin/make check` expectation wrapper — incorrectly expected a
  failure after the focused fix; the full gate actually passed with the new
  mutation, and the wrapper alone returned nonzero.
- Diff review — found the first checker edit replaced the original no-post
  documentation assertions; corrected it to enforce both old and new phrases.
- `/usr/bin/python3 -m py_compile scripts/check_unity_contracts.py scripts/test_authentication_only_scene_contract.py`
  — passed.
- Root and external-directory `/usr/bin/make check` — both passed 25 canonical
  contracts, 30 Make authority cases, 4 cache mutations, 1 scene mutation, 6
  callback mutations, and 9 OAuth mutations; Unity skipped without an editor.
- `git diff --check` and explicit `Demo.unity` unchanged assertion — passed.
- Unity runtime — unavailable; the binary scene was inspected as bytes only.

### Bugs / findings

- P2: the source checker guaranteed a false field declaration but did not
  detect a future checked-in scene that serialized the public flag.

### Blockers

- No compatible legacy Unity editor is available to render the scene; the
  repository intentionally preserves its Unity 4.3.4f1 binary format.

### Next action

- Open the focused pull request, run exact-head review and hosted checks, and
  merge only if the reviewed commit remains green.

## 2026-06-25 11:35 PDT - P2 - Default to authentication-only demo mode

### Summary

Added a default authentication-only demo path so the legacy PIN OAuth flow can
be inspected without exposing tweet composition or posting controls. Live
posting now requires an explicit Inspector opt-in.

### Work completed

- Added a default-false `ALLOW_TWEET_POSTING` Demo setting and a visible
  authentication-only status label.
- Added a registered static contract that enforces the safe default, UI order,
  documentation, completed plan evidence, and checker registration.
- Updated public usage, security, roadmap, and contributor guidance.

### Threads

- Started: none; this focused change was completed directly.
- Continued: none.
- Stopped: none.

### Files changed

- `UnityTwitter/Assets/Demo.cs` — gated tweet input and posting behind an
  explicit Inspector setting.
- `scripts/check_unity_contracts.py` — added the authentication-only contract.
- `README.md`, `SECURITY.md`, `VISION.md`, `AGENTS.md` — documented the safe
  default and live-post opt-in.
- `docs/plans/2026-06-25-authentication-only-demo.md` — recorded scope and
  verification evidence.

### Validation

- Red-first focused contract — failed on the missing Inspector opt-in as
  expected before production changes.
- `python3 -I scripts/check_unity_contracts.py` — unsupported direct invocation
  failed because isolated mode omits the sibling contract module; validation
  used the repository-owned `scripts/run-python.sh` launcher instead.
- Initial copied mutation harness — failed before the focused contract because
  the copy removed `.git`, which the existing cache-ignore check requires; the
  harness was corrected to preserve repository metadata.
- Two focused source mutations — removing the posting guard and enabling the
  flag by default were both rejected for the intended contract violations.
- `/usr/bin/python3 -m py_compile scripts/check_unity_contracts.py` — passed.
- `/usr/bin/make check` — passed 25 canonical contracts, 30 Make authority
  cases, and the existing 4 cache, 6 callback, and 9 OAuth hostile mutations;
  Unity execution skipped truthfully because no editor was configured.
- `(cd /tmp && /usr/bin/make --no-print-directory -f <repo>/Makefile check)` —
  passed the same full gate from outside the repository.
- `git diff --check` — passed.
- Unity runtime — unavailable on this Linux host; no live provider request or
  tweet was attempted.

### Bugs / findings

- P2: the demo always exposed tweet composition and posting controls after
  authentication, leaving no safe authentication-only exercise path.

### Blockers

- A compatible legacy Unity editor and retired provider flow are unavailable
  locally; hosted static checks remain authoritative for the checked-in gate.

### Next action

- Open a focused pull request, run exact-head Codex review and hosted checks,
  and merge only if both remain clean.

## 2026-06-21

- Hardened the Make verification gate against caller-controlled Python
  expressions, shells, startup files, extra makefiles, and non-executing or
  error-ignoring modes.
- Added adversarial Make authority coverage and pinned hosted verification to
  `/usr/bin/make check` without changing the Unity application.
- Rejected later single-colon replacement of all public aliases, embedded the
  reviewed root and literal Python/Unity selections before later non-override
  target assignments, and pinned the public recipe shell.
- Kept GNU Make startup parse code outside the enforceable boundary while
  rejecting PATH-shadowed defaults and isolating Python from `PYTHONPATH`,
  user-site packages, and `sitecustomize.py`.

## 2026-06-19

- Rejected malformed percent escapes, invalid UTF-8, and decoded control
  characters in OAuth form responses before token state is accepted.
- Rejected surrounding whitespace in opaque OAuth credentials, tokens, PINs,
  and account fields before signing or provider side effects.
- Truncated OAuth timestamps to elapsed whole seconds instead of rounding into
  a future second, and normalized signature parameters by encoded ordinal key
  and value.
- Invalidated in-flight request/access token callbacks when the Unity demo is
  disabled so hidden or destroyed UI cannot restore stale authorization state
  or open a browser.

## 2026-06-17

- Public OAuth and posting coroutines reject missing callbacks before
  credentials, signing, or network work.

## 2026-06-16

- Made OAuth timestamp conversion and decimal formatting culture-independent
  so signatures use stable Unix-second protocol values on every host locale.
- Rejected whitespace-only tweet text before OAuth signing and request
  construction while preserving valid content exactly.

## 2026-06-14

- Documented the unpinned legacy Unity editor boundary, local-only Demo
  credentials, session-only tokens, PIN OAuth, explicit posting, legacy `WWW`
  transport, HTTPS endpoints, and retired Twitter API limitations.

## 2026-06-13

- Ignored superseded OAuth callbacks with per-stage generations, cleared prior
  auth state on replacement attempts, and consumed request tokens once.
- Required every consumed OAuth token and identity response field to occur
  exactly once, rejecting ambiguous duplicated fields through redacted paths.
- Added exact-key duplicate fixtures for request tokens, token secrets, user
  IDs, and screen names.
- Rejected whitespace-only OAuth credentials, request tokens, PINs, and access
  token fields before signing, network exchange, or browser authorization.

## 2026-06-12

- Replaced unanchored OAuth response regex extraction with exact-key form
  parsing, percent decoding, and fail-closed malformed-escape handling.
- Ignored Python bytecode caches produced by local contract compilation.

## 2026-06-10

- Replaced provider-controlled OAuth transport and tweet response error details
  in Unity logs with stable redacted failure messages.
- Stopped loading or saving long-lived OAuth values through `PlayerPrefs`, kept
  credentials session-only, and deleted legacy plaintext preference values on
  startup.
- Made local verification root-independent and fixed hosted runner and action
  release annotations to reviewed versions.
- Added a pinned, read-only GitHub Actions matrix on Python 3.10, 3.12, and
  3.14 that disables checkout credential persistence and runs the static
  `make check` baseline.
- Extended the Unity contract checker to require the CI workflow and completed
  CI plan.
- Bound the checkout credential-persistence assertion to the checkout step so
  moving the setting to another action cannot satisfy the hosted CI contract.

## 2026-06-09

- Redacted Twitter user IDs and screen names from successful OAuth demo logs.
- Added static checker coverage for account-identifier log redaction.
- Redacted tweet text from `PostTweet` validation failure logs.
- Extended static checker coverage for tweet-text validation log redaction.
- Guarded request-token, access-token, and tweet-post API helpers when consumer
  credentials are missing before signed requests are built.
- Added static checker coverage for API-level consumer credential guards.
- Guarded authorization-page launches when the request token is missing.
- URL-encoded request tokens before interpolating them into authorization URLs.
- Guarded access-token exchanges when the request token or PIN is missing.
- Added static checker coverage for access-token exchange input guards.
- Replaced predictable `System.Random` OAuth nonce generation with
  cryptographic random bytes.
- Added static checker coverage for OAuth nonce entropy.
- Replaced raw OAuth response-body failure logs with redacted missing-field
  messages in the request-token and access-token helper paths.
- Added static checker coverage for API-level OAuth response log redaction.

## 2026-06-08

- Guarded tweet submission when the Unity demo does not yet have an access
  token.
- Guarded PIN submission when the Unity demo does not yet have a request token.
- Added canonical `docs/plans` coverage to the Unity static contract checker.
- Redacted request/access token and token-secret values from Unity demo logs.
- Added a static contract for token-log redaction and `make check` as the
  shared verification alias.
- Added a `make verify` static gate for Unity project files and runtime URL security.
- Moved the demo registration link from plain HTTP to HTTPS.
- Marked the existing plain-HTTP runtime endpoint bug note as fixed.
