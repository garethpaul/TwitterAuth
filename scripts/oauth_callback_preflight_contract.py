#!/usr/bin/env python3
"""Focused static contract for public coroutine callback preflights."""

import re


OPERATIONS = (
    (
        "GetRequestToken",
        "GetRequestToken - callback is missing.",
        "ConsumerCredentialsAreMissing(consumerKey, consumerSecret)",
    ),
    (
        "GetAccessToken",
        "GetAccessToken - callback is missing.",
        "ConsumerCredentialsAreMissing(consumerKey, consumerSecret)",
    ),
    (
        "PostTweet",
        "PostTweet - callback is missing.",
        "ConsumerCredentialsAreMissing(consumerKey, consumerSecret)",
    ),
)


def validation_errors(source):
    errors = []

    for operation, diagnostic, first_validation in OPERATIONS:
        match = re.search(
            rf"public static IEnumerator {operation}\([^)]*\)\s*\{{(?P<body>.*?)"
            + re.escape(first_validation),
            source,
            re.DOTALL,
        )
        if not match:
            errors.append(
                f"{operation} must expose its callback preflight before input validation"
            )
            continue

        preamble = match.group("body")
        guard = re.fullmatch(
            r"\s*if \(callback == null\)\s*\{\s*"
            + rf'Debug\.Log\("{re.escape(diagnostic)}"\);\s*'
            + r"yield break;\s*\}\s*if \($",
            preamble,
            re.DOTALL,
        )
        if not guard:
            errors.append(
                f"{operation} must reject a null callback first with its fixed diagnostic and yield break"
            )

        if source.count(f'Debug.Log("{diagnostic}");') != 1:
            errors.append(f"{operation} callback diagnostic must occur exactly once")

    return errors
