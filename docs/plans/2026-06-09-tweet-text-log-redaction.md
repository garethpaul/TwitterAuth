# Tweet Text Log Redaction

## Status: Completed

## Context

`API.PostTweet` rejects empty or over-length tweet text before building a signed
Twitter request. That validation failure previously logged the submitted text,
which could expose user-authored content in Unity logs even though the post was
not sent.

## Objectives

- Preserve tweet text validation before signed requests.
- Avoid logging tweet body content on validation failures.
- Keep the callback failure behavior unchanged.
- Extend static checks so the redacted validation message remains covered by
  `make check`.

## Work Completed

- Replaced the text-including validation log with a generic redacted message.
- Extended `scripts/check_unity_contracts.py` to reject tweet-content logging
  on validation failures.
- Required this completed plan in the Unity contract checker.
- Updated README, VISION, and CHANGES.

## Verification

- Negative check before implementation:
  `make check` failed with
  `PostTweet validation failures must not log tweet text`.
- `python3 scripts/check_unity_contracts.py`
- `make check`
- `git diff --check`

## Follow-Up Candidates

- Add a no-post authentication-only demo path.
- Document secure token storage alternatives to plain PlayerPrefs.
