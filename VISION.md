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
- Reject whitespace-only or surrounding-whitespace OAuth inputs before signing
  or browser authorization
- Reject whitespace-only tweet text before OAuth signing or network requests
- Avoid logging access tokens and token secrets
- Keep demo OAuth tokens session-only and remove legacy plaintext PlayerPrefs
  values
- Avoid logging Twitter user IDs or screen names in demo console output
- Avoid logging raw OAuth response bodies
- Reject duplicated OAuth token or account-identity response fields
- Reject malformed OAuth form escapes, invalid UTF-8, and control characters
- Ignore superseded OAuth callbacks and consume request tokens once
- Invalidate pending OAuth callbacks when the demo component is disabled
- Avoid logging provider-controlled transport or API error details
- Avoid logging tweet body text during validation failures
- Generate OAuth nonces with cryptographic random bytes
- Format OAuth timestamps independently of the host locale
- Truncate OAuth timestamps and sort encoded signature parameters ordinally
- Public OAuth and posting coroutines reject missing callbacks before
  credentials, signing, or network work.
- Guard authorization-page launches when request tokens are missing
- Guard access-token exchanges when request tokens or PIN values are missing
- Avoid exchanging PINs before a request token exists
- Avoid posting tweets before an access token exists
- Keep authentication-only mode as the default and require an explicit
  Inspector opt-in before showing tweet posting controls
- Treat legacy Unity `WWW` and Twitter API assumptions as historical context
- Keep runtime network endpoints on HTTPS
- Keep demo logs redacted when OAuth succeeds
- Keep the static `make check` baseline running in GitHub Actions
- Keep legacy Unity setup, local credential, PIN OAuth, explicit posting,
  `WWW`, HTTPS endpoint, and retired API notes tied to checked-in evidence

Next priorities:

- Document platform credential-store integration if persistent login is revived

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
