# Make Authority Isolation

## Status: Completed

## Context

The repository protected its derived root, but GNU Make still accepted caller-
controlled shell, startup-file, execution-mode, and Python expression state.

## Implementation

- Hardened Make startup and every public target without changing C#, Unity
  project assets, OAuth behavior, or provider integration.
- Added an adversarial authority harness and pinned CI to `/usr/bin/make check`.

## Verification

- Repository and external-directory `make check` passed 24 static checks and 19
  mutation cases; the Unity build retained its documented host skip.
- Authority tests cover 30 target/root/shell cases plus tool, startup, and mode
  rejection.

## Scope Boundary

This change does not execute or modernize the retired Unity/Twitter runtime.
