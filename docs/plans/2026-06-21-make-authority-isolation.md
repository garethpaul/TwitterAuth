# Make Authority Isolation

## Status: Completed

## Context

The repository protected its derived root, but GNU Make still accepted caller-
controlled shell, startup-file, execution-mode, and Python expression state.

## Implementation

- Hardened the checked-in Makefile definitions after their parse boundary
  without changing C#, Unity project assets, OAuth behavior, or provider
  integration.
- Public aliases use double-colon rules, embed reviewed root plus literal
  Python/Unity command values before later non-override target variables can
  alter them, and pin `/bin/sh -c` against later non-override shell assignments.
- Added an adversarial authority harness and pinned CI to `/usr/bin/make check`.

## Verification

- Repository and external-directory `make check` passed 24 static checks and 19
  mutation cases; the Unity build retained its documented host skip.
- Authority tests cover 30 target/root/shell cases, a literal hostile Python
  path, command and environment Make-syntax rejection, command and environment
  `MAKEFILE_LIST` rejection, startup boundaries, caller `MAKEFLAGS`, and ten
  non-executing or error-ignoring modes.
- Regressions reject all six later single-colon recipe replacements, protect
  ordinary later root/Python/Unity/shell variables, and exercise the explicit
  override, startup, and PATH-tool exclusions.

## Scope Boundary

This is a local checked-in-Makefile boundary, not a sandbox for caller-supplied
Make programs. GNU Make startup files are parsed before repository checks, so
their parse-time code remains outside the local trust boundary. Later makefiles
using GNU Make `override` directives likewise remain outside the local trust
boundary. PATH resolution of the default `python3` and `unity` executable
selections is caller-controlled rather than authenticated by this repository.

Within that boundary, later non-override assignments cannot redirect the
reviewed root, Python command, Unity command, or recipe shell, and later
single-colon recipes fail closed. This change does not execute or modernize the
retired Unity/Twitter runtime.
