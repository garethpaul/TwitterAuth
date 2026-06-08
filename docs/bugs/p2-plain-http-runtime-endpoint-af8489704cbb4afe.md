# [P2] Move runtime network endpoint off plain HTTP

## Severity

P2 - security/reliability

## Evidence

- `UnityTwitter/Assets/Demo.cs:69`: `Application.OpenURL("http://dev.twitter.com/apps/new");`

## Problem

The application sends a runtime request to a plain-HTTP endpoint. That can expose or modify request data in transit and can also fail on modern platforms that block cleartext traffic by default.

## Suggested fix

Use HTTPS for the endpoint, move the URL into environment or build configuration, and surface request failures to the user or caller.

## Review metadata

- Repository: `garethpaul/TwitterAuth`
- Reviewed commit: `9f45acf44d7487d5c575a448dadcbc2793759b46`
- Labels: `bug`, `codex-review`, `severity:P2`
- Codex review fingerprint: `af8489704cbb4afe`
