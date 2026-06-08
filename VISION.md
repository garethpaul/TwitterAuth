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
- Avoid logging access tokens and token secrets
- Treat legacy Unity `WWW` and Twitter API assumptions as historical context

Next priorities:

- Add README setup notes for Unity and API credential configuration
- Remove or redact token logs in the demo
- Document secure token storage alternatives to plain PlayerPrefs
- Add a no-post demo path for authentication-only testing

Contribution rules:

- One PR = one focused OAuth, demo UI, posting, token, or documentation change.
- Do not commit consumer secrets or user access tokens.
- Keep live posting opt-in and visible.
- Include Unity version notes for behavior changes.

## Security And Responsible Use

OAuth samples can expose long-lived tokens and post on behalf of users. The
demo should avoid printing secrets, should keep posting explicit, and should
make revocation and storage behavior clear.

## What We Will Not Merge (For Now)

- Checked-in API credentials
- Token logging
- Silent posting
- Token storage changes without security notes
