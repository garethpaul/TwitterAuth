## TwitterAuth Vision

TwitterAuth is a Unity sample for OAuth-based Twitter authentication and posting
from a game or application.

The repository is useful as a historical Unity/C# example of request-token,
PIN-based authorization, access-token storage, OAuth signing, and posting a
status update.

The goal is to preserve the sample while making credential handling and
token-storage risks explicit.

The current focus is:

Priority:

- Preserve the OAuth token exchange and Unity demo scene
- Keep consumer keys and secrets configured by the developer, not committed
- Guard API-level OAuth helpers before signing requests with missing consumer
  credentials
- Avoid logging access tokens and token secrets
- Keep demo OAuth tokens session-only and remove legacy plaintext PlayerPrefs
  values
- Avoid logging Twitter user IDs or screen names in demo console output
- Avoid logging raw OAuth response bodies
- Avoid logging provider-controlled transport or API error details
- Avoid logging tweet body text during validation failures
- Generate OAuth nonces with cryptographic random bytes
- Guard authorization-page launches when request tokens are missing
- Guard access-token exchanges when request tokens or PIN values are missing
- Avoid exchanging PINs before a request token exists
- Avoid posting tweets before an access token exists
- Treat legacy Unity `WWW` and Twitter API assumptions as historical context
- Keep runtime network endpoints on HTTPS
- Keep demo logs redacted when OAuth succeeds
- Keep the static `make check` baseline running in GitHub Actions

Next priorities:

- Add README setup notes for Unity and API credential configuration
- Document platform credential-store integration if persistent login is revived
- Add a no-post demo path for authentication-only testing

Contribution rules:

- One PR = one focused OAuth, demo UI, posting, token, or documentation change.
- Do not commit consumer secrets or user access tokens.
- Keep live posting opt-in and visible.
- Include Unity version notes for behavior changes.

## Security And Responsible Use

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

OAuth samples can expose long-lived tokens and post on behalf of users. The
demo should avoid printing secrets, should keep posting explicit, and should
make revocation and storage behavior clear.

## What We Will Not Merge (For Now)

- Checked-in API credentials
- Token or account-identifier logging
- Silent posting
- Token storage changes without security notes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
