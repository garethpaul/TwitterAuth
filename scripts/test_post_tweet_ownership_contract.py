#!/usr/bin/env python3
"""Mutation tests for demo tweet-posting ownership."""

from pathlib import Path

from post_tweet_ownership_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = ROOT / "UnityTwitter" / "Assets" / "Demo.cs"

STALE_COMPLETION_GUARD = (
    "        if (postTweetGeneration != m_PostTweetGeneration)\n"
    "        {\n"
    "            return;\n"
    "        }\n"
)


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
            "remove post invalidation helper",
            source.replace(
                "    private void InvalidatePostTweetOwnership()\n"
                "    {\n"
                "        m_PostTweetGeneration++;\n"
                "        m_PostTweetInFlight = false;\n"
                "    }\n\n",
                "",
                1,
            ),
        ),
        (
            "accept callback after disable",
            source.replace(
                "        InvalidatePostTweetOwnership();\n"
                "        m_RequestTokenResponse = null;",
                "        m_RequestTokenResponse = null;",
                1,
            ),
        ),
        (
            "accept callback after account switch",
            source.replace(
                "                InvalidatePostTweetOwnership();\n"
                "                m_RequestTokenResponse = null;",
                "                m_RequestTokenResponse = null;",
                1,
            ),
        ),
        (
            "invalidate account switch after OAuth reset",
            source.replace(
                "                InvalidatePostTweetOwnership();\n"
                "                m_RequestTokenResponse = null;\n"
                "                m_AccessTokenResponse = new AccessTokenResponse();",
                "                m_RequestTokenResponse = null;\n"
                "                m_AccessTokenResponse = new AccessTokenResponse();\n"
                "                InvalidatePostTweetOwnership();",
                1,
            ),
        ),
        # Commenting a guard out can preserve every asserted literal verbatim, so
        # a raw-source contract stays green while the guard is dead code. The two
        # block-comment cases below were measured green against the previous
        # raw-source contract; the other two were already rejected, but only
        # incidentally (line comments shift the indentation this contract asserts,
        # and dropping `else` removes an asserted literal). All four are kept so
        # the class stays covered regardless of which literal a guard sits in.
        (
            "block-comment the stale completion guard",
            source.replace(
                STALE_COMPLETION_GUARD,
                "        /*\n" + STALE_COMPLETION_GUARD + "        */\n",
                1,
            ),
        ),
        (
            "line-comment the stale completion guard",
            source.replace(
                STALE_COMPLETION_GUARD,
                "        // if (postTweetGeneration != m_PostTweetGeneration)\n"
                "        // {\n"
                "        //     return;\n"
                "        // }\n",
                1,
            ),
        ),
        (
            "block-comment the in-flight guard",
            source.replace(
                "            if (m_PostTweetInFlight)\n"
                "            {\n"
                '                print("OnPostTweet - skipped. A post is already in progress.");\n'
                "            }\n"
                "            else if (m_AccessTokenResponse != null &&\n",
                "            /*\n"
                "            if (m_PostTweetInFlight)\n"
                "            {\n"
                '                print("OnPostTweet - skipped. A post is already in progress.");\n'
                "            }\n"
                "            */\n"
                "            if (m_AccessTokenResponse != null &&\n",
                1,
            ),
        ),
        (
            "block-comment ownership invalidation on disable",
            source.replace(
                "        InvalidatePostTweetOwnership();\n"
                "        m_RequestTokenResponse = null;",
                "        /* InvalidatePostTweetOwnership(); */\n"
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
