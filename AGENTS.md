# AGENTS.md

## Repository purpose

`garethpaul/TwitterAuth` is a public sample, documentation, or utility project. The checked-in files describe a public sample, documentation, or utility project with the structure summarized below.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `plans` - repository source or sample assets
- `UnityTwitter` - repository source or sample assets

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Combined verification: `make verify`
- Lint/static checks: `make lint`
- Tests: `make test`
- Build: `make build`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C# (2).

## Testing guidance

- Test-related files detected: `UnityTwitter/Library/InspectorExpandedItems.asset`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- Keep tweet posting disabled by default. Authentication-only checks should
  leave `ALLOW_TWEET_POSTING` off; enable it only for deliberate live-post
  testing with an appropriate test account.
- Do not serialize `ALLOW_TWEET_POSTING` into the checked-in scene. The legacy
  binary scene must omit the field so fresh checkouts retain the source-level
  false default.
- Preserve single-flight post ownership and invalidate its callback generation
  when the demo component is disabled.
- PIN UI preflight must reject placeholder or surrounding-whitespace text
  before clearing the retained request token.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-twitterauth-baseline.md` for the current static verification baseline.
- See `docs/plans/2026-06-08-twitterauth-pin-guard.md` for the request-token guard on PIN submission.
- See `docs/plans/2026-06-08-twitterauth-post-token-guard.md` for the access-token guard on tweet submission.
- See `docs/plans/2026-06-25-authentication-only-demo.md` for the default
  no-post demo path and explicit live-post Inspector opt-in.
- See `docs/plans/2026-06-25-authentication-only-scene-default.md` for the
  binary-scene serialization guard.
- See `docs/plans/2026-06-26-post-tweet-ownership.md` for live-post single-flight
  and callback-generation ownership.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
