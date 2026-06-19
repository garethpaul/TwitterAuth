#!/usr/bin/env python3
"""Focused source contract for OAuth parsing, signing, time, and lifecycle safety."""

import re


def validation_errors(api_source, demo_source):
    errors = []

    required_api_contracts = (
        "private static bool TryDecodeFormComponent(string value, out string decodedValue)",
        "new UTF8Encoding(false, true)",
        "private static int HexValue(char value)",
        "TryDecodeFormComponent(matches[0].Groups[1].Value, out decodedValue)",
        "decodedValue.Any(char.IsControl)",
        "!string.Equals(value, value.Trim(), StringComparison.Ordinal)",
        "return ((long)ts.TotalSeconds).ToString(CultureInfo.InvariantCulture);",
        "private static string NormalizeRequestParameters(IEnumerable<KeyValuePair<string, string>> parameters)",
        "encodedParameters.Sort((left, right) =>",
        "string.CompareOrdinal(left.Key, right.Key)",
        "string.CompareOrdinal(left.Value, right.Value)",
        "UrlEncode(NormalizeRequestParameters(nonSecretParameters))",
    )
    for contract in required_api_contracts:
        if contract not in api_source:
            errors.append(f"OAuth hardening contract is missing: {contract}")

    forbidden_api_contracts = (
        "Convert.ToInt64(ts.TotalSeconds",
        "orderby p.Key, p.Value",
        "return Uri.UnescapeDataString(matches[0].Groups[1].Value.Replace(\"+\", \" \"));",
    )
    for contract in forbidden_api_contracts:
        if contract in api_source:
            errors.append(f"OAuth hardening contract still contains unsafe behavior: {contract}")

    lifecycle_match = re.search(
        r"private void OnDisable\(\)\s*\{(?P<body>.*?)\n\s*\}",
        demo_source,
        re.DOTALL,
    )
    if lifecycle_match is None:
        errors.append("OAuth lifecycle contract is missing: private void OnDisable()")
        lifecycle_body = ""
    else:
        lifecycle_body = lifecycle_match.group("body")

    required_lifecycle_contracts = (
        "m_RequestTokenGeneration++;",
        "m_AccessTokenGeneration++;",
        "m_RequestTokenResponse = null;",
    )
    for contract in required_lifecycle_contracts:
        if contract not in lifecycle_body:
            errors.append(f"OAuth lifecycle contract is missing: {contract}")

    return errors
