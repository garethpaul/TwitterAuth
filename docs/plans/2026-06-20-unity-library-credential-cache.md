# Unity Library Credential Cache Removal

Status: Completed

## Problem

The legacy Unity `Library` directory was tracked in Git. Two generated metadata
copies retained historical high-entropy OAuth access-token material after the
maintained source files were sanitized. The cache is generated local state and
is not required to build or understand the sample.

## Resolution

- Remove the tracked `UnityTwitter/Library` cache.
- Ignore future local cache regeneration.
- Keep hash-based rejection for the historical provider credentials.
- Fail verification whenever files under the generated cache become tracked.

Repository removal does not revoke provider credentials or erase Git history.
The repository owner must revoke the historical Twitter access token and token
secret, review provider activity, and remove any unrecognized authorized apps
or sessions.

## Verification

- `python3 scripts/check_unity_contracts.py`
- `make check`
- Current-tree Gitleaks scan with redacted output
