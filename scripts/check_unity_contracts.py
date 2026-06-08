#!/usr/bin/env python3
"""Static verification for the legacy Unity TwitterAuth sample."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]


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


def main():
    checks = [
        check_required_project_files,
        check_runtime_urls_are_https,
        check_bug_note_status,
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
