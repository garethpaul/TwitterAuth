#!/usr/bin/env python3
"""Mutation tests for the callback-preflight static contract."""

from pathlib import Path

from oauth_callback_preflight_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "UnityTwitter" / "Assets" / "Twitter.cs"


def require_rejected(name, source):
    if not validation_errors(source):
        raise AssertionError(f"mutation was not rejected: {name}")


def guard(operation):
    return (
        "            if (callback == null)\n"
        "            {\n"
        f'                Debug.Log("{operation} - callback is missing.");\n'
        "                yield break;\n"
        "            }\n\n"
    )


def main():
    source = SOURCE_PATH.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError("baseline callback contract failed: " + "; ".join(errors))

    mutations = []
    for operation in ("GetRequestToken", "GetAccessToken", "PostTweet"):
        mutations.append(
            (f"remove {operation} guard", source.replace(guard(operation), "", 1))
        )

    request_guard = guard("GetRequestToken")
    credential_guard = (
        "            if (ConsumerCredentialsAreMissing(consumerKey, consumerSecret))\n"
        "            {\n"
        "                Debug.Log(\"GetRequestToken - consumer credentials are missing.\");\n"
        "                callback(false, null);\n"
        "                yield break;\n"
        "            }\n\n"
    )
    mutations.extend(
        [
            (
                "move request-token guard after credentials",
                source.replace(
                    request_guard + credential_guard,
                    credential_guard + request_guard,
                    1,
                ),
            ),
            (
                "weaken access-token diagnostic",
                source.replace(
                    "GetAccessToken - callback is missing.",
                    "Callback is missing.",
                    1,
                ),
            ),
            (
                "remove post-tweet yield",
                source.replace(
                    "                Debug.Log(\"PostTweet - callback is missing.\");\n"
                    "                yield break;",
                    "                Debug.Log(\"PostTweet - callback is missing.\");",
                    1,
                ),
            ),
        ]
    )

    for name, mutated_source in mutations:
        require_rejected(name, mutated_source)

    print(f"OAuth callback preflight mutations rejected ({len(mutations)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
