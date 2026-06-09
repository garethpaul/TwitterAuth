#!/usr/bin/env python3
"""Static verification for the legacy Unity TwitterAuth sample."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DOCS_PLANS = ROOT / "docs/plans"
CANONICAL_PLAN = DOCS_PLANS / "2026-06-08-twitterauth-baseline.md"


def fail(message):
    print(f"check_unity_contracts.py: {message}", file=sys.stderr)
    return 1


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_required_project_files():
    for relative_path in [
        "UnityTwitter/Assets/Demo.cs",
        "UnityTwitter/Assets/Twitter.cs",
        "UnityTwitter/Assets/Demo.unity",
        "UnityTwitter/ProjectSettings/ProjectSettings.asset",
        "docs/readme-overview.svg",
        "docs/bugs/p2-plain-http-runtime-endpoint-af8489704cbb4afe.md",
    ]:
        require((ROOT / relative_path).exists(), f"{relative_path} must stay checked in")

    ET.parse(ROOT / "docs/readme-overview.svg")


def check_runtime_urls_are_https():
    for path in (ROOT / "UnityTwitter/Assets").glob("*.cs"):
        source = path.read_text(encoding="utf-8")
        require(
            not re.search(r'Application\.OpenURL\("http://', source),
            f"{path.relative_to(ROOT)} must not open plain HTTP URLs at runtime",
        )
        require(
            not re.search(r'new WWW\("http://', source),
            f"{path.relative_to(ROOT)} must not call plain HTTP URLs at runtime",
        )

    demo = read_text("UnityTwitter/Assets/Demo.cs")
    require("https://dev.twitter.com/apps/new" in demo, "registration URL must use HTTPS")


def check_bug_note_status():
    bug = read_text("docs/bugs/p2-plain-http-runtime-endpoint-af8489704cbb4afe.md")
    require("Status: Fixed" in bug, "plain HTTP bug note must record the fix status")
    require("https://dev.twitter.com/apps/new" in bug, "bug note must point to the HTTPS endpoint")


def check_demo_token_logging():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    require('"\\n    Token : " +' not in demo, "demo must not log access or request tokens")
    require('"\\n    TokenSecret : " +' not in demo, "demo must not log token secrets")
    require("Token : <redacted>" in demo, "demo logs must redact token values")
    require("TokenSecret : <redacted>" in demo, "demo logs must redact token secret values")


def check_demo_access_flow_guards():
    demo = read_text("UnityTwitter/Assets/Demo.cs")
    api = read_text("UnityTwitter/Assets/Twitter.cs")
    require(
        "m_RequestTokenResponse != null" in demo,
        "PIN submission must guard missing request-token state",
    )
    require(
        "Request token is missing" in demo,
        "PIN submission guard must explain missing request-token state",
    )
    require(
        "m_AccessTokenResponse != null" in demo,
        "tweet submission must guard missing access-token state",
    )
    require(
        "Access token is missing" in demo,
        "tweet submission guard must explain missing access-token state",
    )
    require(
        "response == null" in api and "string.IsNullOrEmpty(response.Token)" in api,
        "PostTweet must guard missing access-token response before OAuth signing",
    )
    require(
        "PostTweet - access token is missing." in api,
        "PostTweet guard must log missing access-token state without secrets",
    )
    require(
        "yield break;" in api,
        "PostTweet guard must stop before building signed requests",
    )


def check_docs_plans():
    require(DOCS_PLANS.is_dir(), "docs/plans must exist")
    plans = sorted(DOCS_PLANS.glob("*.md"))
    require(plans, "docs/plans must contain completed maintenance plans")
    require(CANONICAL_PLAN in plans, f"{CANONICAL_PLAN.relative_to(ROOT)} must be present")

    for plan in plans:
        text = plan.read_text(encoding="utf-8")
        require("Status: Completed" in text, f"{plan.name} must be completed")
        require("make check" in text, f"{plan.name} must document make check verification")


def main():
    checks = [
        check_required_project_files,
        check_runtime_urls_are_https,
        check_bug_note_status,
        check_demo_token_logging,
        check_demo_access_flow_guards,
        check_docs_plans,
    ]
    try:
        for check in checks:
            check()
    except (AssertionError, ET.ParseError) as exc:
        return fail(str(exc))

    print(f"Unity TwitterAuth contracts passed ({len(checks)} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
