# TwitterAuth

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/TwitterAuth` is a public sample, documentation, or utility project. The checked-in files describe a public sample, documentation, or utility project with the structure summarized below.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C# (2).

## Repository Contents

- `README.md` - project overview and local usage notes
- `docs` - source or example code
- `SECURITY.md` - security reporting and disclosure guidance
- `UnityTwitter` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: UnityTwitter, docs
- Dependency and build manifests: none detected
- Entry points or build surfaces: none detected
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git

### Setup

```bash
git clone https://github.com/garethpaul/TwitterAuth.git
cd TwitterAuth
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Open `UnityTwitter` with a compatible legacy Unity editor and inspect the demo scene.
- Run `make check` for static checks. The build step runs Unity only on hosts
  where `unity` is installed.

## Testing and Verification

- `make check` runs static project, HTTPS endpoint, authorization URL
  token-safety, token-log redaction, OAuth nonce entropy, access-token exchange
  input guard, API-level consumer credential guard, tweet-text validation log
  redaction, OAuth-flow guard, and completed-plan checks.
- Completed maintenance plans live under `docs/plans` and are checked by
  `make check`.
- Legacy Unity editor validation for scene/runtime behavior

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include UnityTwitter/Assets/Demo.cs, UnityTwitter/Assets/Twitter.cs, UnityTwitter/Assets/readme.txt.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include UnityTwitter/Assets/Demo.cs, UnityTwitter/Assets/Twitter.cs, UnityTwitter/Assets/readme.txt, docs/bugs/p2-plain-http-runtime-endpoint-af8489704cbb4afe.md.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include UnityTwitter/Assets/Demo.cs, UnityTwitter/Assets/Twitter.cs, UnityTwitter/Assets/readme.txt, docs/bugs/p2-plain-http-runtime-endpoint-af8489704cbb4afe.md.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include UnityTwitter/Assets/Twitter.cs.

## Maintenance Notes

- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-08-twitterauth-baseline.md` for the current static
  verification baseline.
- See `docs/plans/2026-06-08-twitterauth-pin-guard.md` for the request-token
  guard on PIN submission.
- See `docs/plans/2026-06-08-twitterauth-post-token-guard.md` for the
  access-token guard on tweet submission.
- See `docs/plans/2026-06-09-oauth-response-log-redaction.md` for API-level
  OAuth response-body log redaction.
- See `docs/plans/2026-06-09-oauth-nonce-entropy.md` for cryptographic OAuth
  nonce generation coverage.
- See `docs/plans/2026-06-09-authorization-url-token-guard.md` for the
  authorization-page request-token guard and URL encoding coverage.
- See `docs/plans/2026-06-09-access-token-input-guard.md` for the
  access-token exchange request-token and PIN guard coverage.
- See `docs/plans/2026-06-09-consumer-credential-guards.md` for API-level
  consumer credential guard coverage.
- See `docs/plans/2026-06-09-tweet-text-log-redaction.md` for tweet body
  validation log redaction coverage.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
