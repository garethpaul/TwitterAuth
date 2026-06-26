#!/usr/bin/env python3
"""Mutation tests for OAuth parser, timestamp, signature, and lifecycle contracts."""

from pathlib import Path

from oauth_hardening_contract import validation_errors


ROOT = Path(__file__).resolve().parents[1]
API_PATH = ROOT / "UnityTwitter" / "Assets" / "Twitter.cs"
DEMO_PATH = ROOT / "UnityTwitter" / "Assets" / "Demo.cs"


def require_rejected(name, api_source, demo_source):
    if not validation_errors(api_source, demo_source):
        raise AssertionError(f"mutation was not rejected: {name}")


def main():
    api_source = API_PATH.read_text(encoding="utf-8")
    demo_source = DEMO_PATH.read_text(encoding="utf-8")
    errors = validation_errors(api_source, demo_source)
    if errors:
        raise AssertionError("baseline OAuth hardening contract failed: " + "; ".join(errors))

    lifecycle_block = (
        "    private void OnDisable()\n"
        "    {\n"
        "        m_RequestTokenGeneration++;\n"
        "        m_AccessTokenGeneration++;\n"
        "        m_RequestTokenResponse = null;\n"
        "    }\n"
    )
    mutations = (
        (
            "accept malformed percent escapes",
            api_source.replace(
                "TryDecodeFormComponent(matches[0].Groups[1].Value, out decodedValue)",
                "true",
                1,
            ),
            demo_source,
        ),
        (
            "accept decoded control characters",
            api_source.replace(
                ") ||\n                decodedValue.Any(char.IsControl)",
                ")",
                1,
            ),
            demo_source,
        ),
        (
            "accept surrounding OAuth whitespace",
            api_source.replace(
                " ||\n                   !string.Equals(value, value.Trim(), StringComparison.Ordinal)",
                "",
                1,
            ),
            demo_source,
        ),
        (
            "round timestamps into the future",
            api_source.replace(
                "return ((long)ts.TotalSeconds).ToString(CultureInfo.InvariantCulture);",
                "return Convert.ToInt64(ts.TotalSeconds, CultureInfo.InvariantCulture).ToString(CultureInfo.InvariantCulture);",
                1,
            ),
            demo_source,
        ),
        (
            "sort signature parameters with current culture",
            api_source.replace(
                "string.CompareOrdinal(left.Key, right.Key)",
                "string.Compare(left.Key, right.Key)",
                1,
            ),
            demo_source,
        ),
        (
            "sort signature values with current culture",
            api_source.replace(
                "string.CompareOrdinal(left.Value, right.Value)",
                "string.Compare(left.Value, right.Value)",
                1,
            ),
            demo_source,
        ),
        (
            "keep request callbacks live while disabled",
            api_source,
            demo_source.replace(
                lifecycle_block,
                lifecycle_block.replace("        m_RequestTokenGeneration++;\n", ""),
                1,
            ),
        ),
        (
            "keep access callbacks live while disabled",
            api_source,
            demo_source.replace(
                lifecycle_block,
                lifecycle_block.replace("        m_AccessTokenGeneration++;\n", ""),
                1,
            ),
        ),
        (
            "retain stale request token while disabled",
            api_source,
            demo_source.replace(
                lifecycle_block,
                lifecycle_block.replace("        m_RequestTokenResponse = null;\n", ""),
                1,
            ),
        ),
        (
            "consume request token before PIN preflight",
            api_source,
            demo_source.replace(" &&\n                PINIsReady(m_PIN)", "", 1),
        ),
    )

    for name, mutated_api, mutated_demo in mutations:
        require_rejected(name, mutated_api, mutated_demo)

    print(f"OAuth hardening mutations rejected ({len(mutations)} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
