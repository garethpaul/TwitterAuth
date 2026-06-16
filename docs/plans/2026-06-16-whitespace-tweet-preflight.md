# Reject Whitespace-Only Tweets Before OAuth Signing

Status: Completed

## Context

`API.PostTweet` rejects null, empty, and over-140-character text, but accepts a
string containing only spaces, tabs, or newlines. The method then includes that
meaningless value in the OAuth signature and sends a network request that
cannot produce useful user content.

## Requirements

- Reject null, empty, whitespace-only, and over-limit tweet text before form,
  header, signature, or network construction.
- Preserve valid tweet text exactly; do not trim or rewrite user content.
- Keep the existing access-token and consumer-credential preflights ahead of
  tweet validation.
- Keep diagnostics redacted and return one failed callback without sending.
- Add mutation-sensitive static coverage and maintained guidance without
  claiming live Twitter or Unity execution.

## Implementation

- Add a small tweet-text validity helper in `UnityTwitter/Assets/Twitter.cs`
  and route `PostTweet` through it before request construction.
- Extend `scripts/check_unity_contracts.py` with a registered focused contract
  for helper semantics, ordering, valid-text preservation, diagnostics, and
  completed-plan evidence.
- Update `README.md`, `SECURITY.md`, `VISION.md`, and `CHANGES.md` with the
  posting preflight boundary.

## Verification

- Run the focused contract and complete repository/external-directory Make
  gates.
- Compile the Python checker and retain all existing Unity project, OAuth,
  logging, callback-generation, and endpoint contracts.
- Reject isolated mutations that remove whitespace rejection, trim valid text,
  move validation after signing, weaken guidance, omit checker registration,
  or falsify completed plan evidence.
- Audit the exact diff, generated artifacts, file modes, conflicts, and
  credential-like additions before committing.

## Runtime Boundary

Unity editor execution and live Twitter OAuth are unavailable. This change is
verified through the repository's deterministic source contracts and hosted
portable Python matrix; no live posting claim is made.

## Work Completed

- Added a centralized tweet-text preflight that rejects null, empty,
  whitespace-only, and over-limit values before request construction.
- Preserved valid tweet text exactly in the OAuth parameters and form body.
- Added a registered static contract for helper semantics, validation order,
  early failure, redacted diagnostics, content preservation, guidance, and
  completed-plan evidence.
- Updated maintained posting, security, roadmap, and change documentation.

## Verification Completed

- `python3 -m py_compile scripts/check_unity_contracts.py`
- Focused `check_tweet_text_preflight` execution.
- All 20 implementation and repository contracts excluding the deliberate
  in-progress plan-status gate before this completion record was written.
- The first `make check` attempt rejected this plan because it described the
  gate without recording the literal command; this evidence entry corrects
  that documentation-contract failure before the canonical rerun.
- Repository-root and external-directory `make check` reruns passed all 21
  static contracts; Unity was unavailable and the documented build step
  skipped editor execution.
- Eight isolated mutations were rejected for whitespace-check removal, helper
  bypass, valid-text trimming, diagnostic weakening, README/security/vision
  guidance removal, and focused-check unregistration.
