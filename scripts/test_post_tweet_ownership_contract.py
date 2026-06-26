#!/usr/bin/env python3
"""Mutation tests for demo tweet-posting ownership."""

from pathlib import Path

from post_tweet_ownership_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = ROOT / "UnityTwitter" / "Assets" / "Demo.cs"


def require_rejected(name, source):
    if not validation_errors(source):
        raise AssertionError(f"mutation was not rejected: {name}")


def main():
    source = DEMO_PATH.read_text(encoding="utf-8")
    errors = validation_errors(source)
    if errors:
        raise AssertionError("baseline post ownership contract failed: " + "; ".join(errors))

    mutations = (
        ("remove in-flight guard", source.replace("if (m_PostTweetInFlight)", "if (false)", 1)),
        (
            "remove generation capture",
            source.replace(
                "int postTweetGeneration = ++m_PostTweetGeneration;",
                "int postTweetGeneration = m_PostTweetGeneration;",
                1,
            ),
        ),
        (
            "claim ownership after start",
            source.replace(
                "m_PostTweetInFlight = true;\n                StartCoroutine(API.PostTweet(",
                "StartCoroutine(API.PostTweet(",
                1,
            ),
        ),
        (
            "unbind completion generation",
            source.replace(
                "success => OnPostTweet(postTweetGeneration, success)",
                "success => OnPostTweet(m_PostTweetGeneration, success)",
                1,
            ),
        ),
        (
            "remove stale completion guard",
            source.replace(
                "        if (postTweetGeneration != m_PostTweetGeneration)\n"
                "        {\n"
                "            return;\n"
                "        }\n\n",
                "",
                1,
            ),
        ),
        (
            "retain completed ownership",
            source.replace(
                "        m_PostTweetInFlight = false;\n"
                "        print(\"OnPostTweet - \"",
                "        print(\"OnPostTweet - \"",
                1,
            ),
        ),
        (
            "accept callback after disable",
            source.replace("        m_PostTweetGeneration++;\n", "", 1),
        ),
        (
            "retain ownership after disable",
            source.replace(
                "        m_PostTweetGeneration++;\n"
                "        m_PostTweetInFlight = false;\n"
                "        m_RequestTokenResponse = null;",
                "        m_PostTweetGeneration++;\n"
                "        m_RequestTokenResponse = null;",
                1,
            ),
        ),
    )

    for name, mutated_source in mutations:
        if mutated_source == source:
            raise AssertionError(f"mutation did not apply: {name}")
        require_rejected(name, mutated_source)

    print(f"Post Tweet ownership mutations rejected ({len(mutations)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
