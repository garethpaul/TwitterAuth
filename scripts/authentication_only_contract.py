#!/usr/bin/env python3
"""Focused source contract for the default authentication-only demo path.

Assertions run against comment-blanked source. Tweet posting being off by default
is a documented security posture, and a raw-text assertion cannot distinguish a
live guard from a commented-out one: commenting preserves every asserted literal
verbatim, so the contract would stay green while the guard is dead code.
"""

import re

from csharp_source import blank_comments


ORDERED_FRAGMENTS = (
    'GUI.Button(rect, "Enter PIN")',
    "if (!ALLOW_TWEET_POSTING)",
    'GUI.Label(rect, "Authentication-only mode. Tweet posting is disabled.")',
    "return;",
    "m_Tweet = GUI.TextField(rect, m_Tweet);",
    "API.PostTweet(",
)

ON_GUI_PATTERN = (
    r"private void OnGUI\(\)\s*\{(?P<body>.*?)"
    r"\n    \}\n\n    private void ClearLegacyStoredCredentials"
)


def validation_errors(demo_source):
    """Return a list of contract violations for Demo.cs source text."""
    errors = []
    demo = blank_comments(demo_source)

    if "public bool ALLOW_TWEET_POSTING;" not in demo:
        errors.append("tweet posting must require an explicit Inspector opt-in")
    if "public bool ALLOW_TWEET_POSTING = true;" in demo:
        errors.append("tweet posting must remain disabled by default")

    match = re.search(ON_GUI_PATTERN, demo, re.DOTALL)
    if match is None:
        errors.append("Demo.OnGUI must remain available for authentication-only verification")
        return errors

    body = match.group("body")
    positions = [body.find(fragment) for fragment in ORDERED_FRAGMENTS]
    if not all(position >= 0 for position in positions) or positions != sorted(positions):
        errors.append("authentication-only mode must stop before tweet input and posting")

    return errors
