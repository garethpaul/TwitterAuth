#!/usr/bin/env python3
"""Focused source contract for single-flight demo tweet posting."""

import re


def validation_errors(demo_source):
    errors = []

    for contract in (
        "private int m_PostTweetGeneration;",
        "private bool m_PostTweetInFlight;",
        "private void OnPostTweet(int postTweetGeneration, bool success)",
    ):
        if contract not in demo_source:
            errors.append(f"post ownership contract is missing: {contract}")

    button_start = demo_source.find('if (GUI.Button(rect, "Post Tweet"))')
    button_end = demo_source.find("private void ClearLegacyStoredCredentials()")
    if button_start < 0 or button_end < 0 or button_start >= button_end:
        errors.append("post ownership contract cannot locate the Post Tweet handler")
        button_body = ""
    else:
        button_body = demo_source[button_start:button_end]

    ordered_button_contracts = (
        "if (m_PostTweetInFlight)",
        "else if (m_AccessTokenResponse != null",
        "int postTweetGeneration = ++m_PostTweetGeneration;",
        "m_PostTweetInFlight = true;",
        "StartCoroutine(API.PostTweet(",
        "success => OnPostTweet(postTweetGeneration, success)",
    )
    button_positions = [button_body.find(contract) for contract in ordered_button_contracts]
    if any(position < 0 for position in button_positions):
        errors.append("Post Tweet must guard, claim, and generation-bind one request")
    elif button_positions != sorted(button_positions):
        errors.append("Post Tweet ownership must be published before starting the coroutine")

    disable_match = re.search(
        r"private void OnDisable\(\)\s*\{(?P<body>.*?)\n\s*\}",
        demo_source,
        re.DOTALL,
    )
    disable_body = disable_match.group("body") if disable_match else ""
    for contract in ("m_PostTweetGeneration++;", "m_PostTweetInFlight = false;"):
        if contract not in disable_body:
            errors.append(f"post lifecycle contract is missing: {contract}")

    completion_start = demo_source.find(
        "private void OnPostTweet(int postTweetGeneration, bool success)"
    )
    if completion_start < 0:
        completion_body = ""
    else:
        completion_body = demo_source[completion_start:]

    stale_guard = (
        "if (postTweetGeneration != m_PostTweetGeneration)\n"
        "        {\n"
        "            return;\n"
        "        }"
    )
    if stale_guard not in completion_body:
        errors.append("post completion must ignore stale generations")

    clear_position = completion_body.find("m_PostTweetInFlight = false;")
    log_position = completion_body.find('print("OnPostTweet - "')
    if clear_position < 0 or log_position < 0 or clear_position > log_position:
        errors.append("current post completion must release ownership before reporting")

    return errors
