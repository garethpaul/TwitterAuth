# Changes

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
