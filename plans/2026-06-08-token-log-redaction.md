# Token Log Redaction Gate

## Problem

The Unity demo printed request/access tokens and token secrets after successful
OAuth flows. Those logs can leak long-lived credentials when copied into bug
reports, screenshots, or shared console output.

## TDD Evidence

1. Extended `scripts/check_unity_contracts.py` with static checks that reject
   token/token-secret log concatenation and require redacted placeholders.
2. Ran `make lint` before changing `Demo.cs` and confirmed the new check failed
   on token logging.
3. Replaced token log values with `<redacted>`, added `make check`, and reran
   the full verification gate.

## Verification

- `make lint`
- `make test`
- `make build`
- `make verify`
- `make check`
- `git diff --check`
