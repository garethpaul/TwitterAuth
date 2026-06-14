# Legacy Unity And Twitter API Setup Notes

## Status: Planned

## Context

The README tells contributors to use a compatible legacy Unity editor but does
not explain that the repository lacks `ProjectVersion.txt`, how credentials
were historically supplied, or which runtime assumptions are retired.

## Priority

Document the checked-in Unity project, local credential, session-only token,
PIN OAuth, posting, transport, and retired Twitter API boundaries without
inventing a supported Unity version.

## Requirements

- State that no exact Unity editor version is recorded and must not be claimed.
- Direct historical inspection to the checked-in `UnityTwitter` project and
  `Demo` scene.
- Explain that consumer key and secret values were entered locally on the Demo
  object and must never be committed.
- Keep access tokens session-only and describe reauthentication after restart.
- Identify PIN-based OAuth, explicit posting, Unity `WWW`, and the checked-in
  HTTPS Twitter endpoints as historical assumptions.
- State that Twitter API access, app registration, PIN authorization, posting,
  and Unity runtime behavior remain unverified.
- Add fail-closed documentation, source, suite, roadmap, changelog, and plan
  contracts plus hostile mutations.

## Verification

- focused static setup-note and source contracts
- repository and external-directory `make check`
- hostile Unity-version claim, credential configuration, token persistence,
  endpoint, transport, documentation, suite, roadmap, and plan-status mutations
- final artifact, credential, exact-diff, and hosted static-check audits

## Scope Boundary

This change does not add credentials, choose a Unity version, install Unity,
contact Twitter, authenticate, post a status, modernize `WWW`, or alter runtime
behavior.
