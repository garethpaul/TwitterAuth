# Provider Error Log Redaction

Status: Completed

## Goal

Prevent OAuth transport and tweet API failures from copying provider-controlled
error details into Unity logs while preserving failure callbacks.

## Changes

- Replace request-token and access-token transport error details with stable
  failure messages.
- Replace tweet transport and response error details with stable failure
  messages.
- Add static contracts that reject the prior dynamic logging expressions and
  require each redacted message.

## Verification

- Run `make check`.
- Restore a dynamic `web.error` request-token log and confirm the static
  contract checker fails before restoring the redacted message.
