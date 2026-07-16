#!/usr/bin/env python3
"""Mutation tests for the authentication-only demo guard.

Covers the comment-blindness class directly: a raw-source contract stays green
when a guard is commented out, because commenting preserves every asserted
literal verbatim. Each mutation below must be rejected.
"""

from pathlib import Path

from authentication_only_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = ROOT / "UnityTwitter" / "Assets" / "Demo.cs"

POSTING_GUARD = (
    "        if (!ALLOW_TWEET_POSTING)\n"
    "        {\n"
    '            GUI.Label(rect, "Authentication-only mode. Tweet posting is disabled.");\n'
    "            return;\n"
    "        }\n"
)

def require_rejected(name, demo_source, original):
    if demo_source == original:
        raise AssertionError(f"mutation did not apply: {name}")
    if not validation_errors(demo_source):
        raise AssertionError(f"mutation was not rejected: {name}")


def main():
    source = DEMO_PATH.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError(
            "baseline authentication-only demo contract failed: " + "; ".join(errors)
        )

    if source.count(POSTING_GUARD) != 1:
        raise AssertionError("authentication-only guard fixture drifted from Demo.cs")

    block_commented = source.replace(
        POSTING_GUARD, "        /*\n" + POSTING_GUARD + "        */\n", 1
    )
    line_commented = source.replace(
        POSTING_GUARD,
        "        // if (!ALLOW_TWEET_POSTING)\n"
        "        // {\n"
        '        //     GUI.Label(rect, "Authentication-only mode. Tweet posting is disabled.");\n'
        "        //     return;\n"
        "        // }\n",
        1,
    )

    mutations = (
        ("delete the posting guard", source.replace(POSTING_GUARD, "", 1)),
        ("comment out the posting guard with a block comment", block_commented),
        ("comment out the posting guard with line comments", line_commented),
        (
            "comment out only the posting guard condition",
            source.replace(
                "        if (!ALLOW_TWEET_POSTING)\n        {\n",
                "        // if (!ALLOW_TWEET_POSTING)\n        if (false)\n        {\n",
                1,
            ),
        ),
        (
            "enable posting by default",
            source.replace(
                "    public bool ALLOW_TWEET_POSTING;",
                "    public bool ALLOW_TWEET_POSTING = true;",
                1,
            ),
        ),
        (
            "comment out the posting opt-in field",
            source.replace(
                "    public bool ALLOW_TWEET_POSTING;",
                "    // public bool ALLOW_TWEET_POSTING;",
                1,
            ),
        ),
        (
            "move the guard after tweet input",
            source.replace(POSTING_GUARD, "", 1).replace(
                "        m_Tweet = GUI.TextField(rect, m_Tweet);\n",
                "        m_Tweet = GUI.TextField(rect, m_Tweet);\n" + POSTING_GUARD,
                1,
            ),
        ),
    )

    for name, mutated in mutations:
        require_rejected(name, mutated, source)

    print(f"Authentication-only demo mutations rejected ({len(mutations)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
