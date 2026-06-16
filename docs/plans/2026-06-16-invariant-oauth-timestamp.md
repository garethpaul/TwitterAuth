# Invariant OAuth Timestamp

## Status: Planned

## Context

OAuth 1.0 timestamps are protocol values expressed as decimal Unix seconds.
`GenerateTimeStamp` currently converts and formats that value with the process
current culture, which makes a signed request depend on host locale instead of
the OAuth wire contract.

## Requirements

- R1. Format OAuth timestamps with `CultureInfo.InvariantCulture`.
- R2. Preserve whole-second UTC Unix-time behavior and the existing signing
  call path.
- R3. Add a static contract that rejects current-culture formatting and checks
  both numeric conversion and string formatting.
- R4. Keep legacy Unity, network, credential, and callback behavior unchanged.
- R5. Document the locale-independent signing boundary in maintained guidance.
- R6. Mutation tests must reject either conversion or formatting drifting back
  to `CurrentCulture`, removal of the checker registration, guidance drift, and
  stale plan status.

## Scope Boundaries

- Do not replace the legacy OAuth implementation, Unity `WWW`, or HMAC-SHA1.
- Do not change timestamp precision, add clocks or dependencies, or make live
  provider requests.
- Unity editor execution remains unavailable on this host.

## Implementation Units

### U1. Make timestamp formatting locale-independent

- **Files:** `UnityTwitter/Assets/Twitter.cs`
- Use invariant culture for the Unix-seconds conversion and decimal string.

### U2. Add mutation-sensitive contracts

- **Files:** `scripts/check_unity_contracts.py`
- Require invariant conversion and formatting, forbid current-culture use in
  `GenerateTimeStamp`, and register the completed plan.

### U3. Preserve maintained guidance

- **Files:** `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`
- Record the locale-independent OAuth timestamp boundary.

## Verification

- Pending implementation.
- Run focused timestamp contracts and full repository and external-directory
  `make check` gates.
- Run isolated hostile mutations for source, checker registration, guidance,
  and completed-plan evidence.
