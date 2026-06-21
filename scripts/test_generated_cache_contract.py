#!/usr/bin/env python3
"""Regression tests for executable Unity cache ignore semantics."""

from pathlib import Path
import subprocess
import tempfile

from check_unity_contracts import unity_library_cache_is_ignored


PROBE_PATH = "UnityTwitter/Library/.twitterauth-cache-probe"


def initialize_repository(root):
    subprocess.run(
        ["git", "init", "--quiet"],
        cwd=root,
        check=True,
    )


def require_ignore_result(rule, expected):
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        initialize_repository(root)
        (root / ".gitignore").write_text(rule, encoding="utf-8")
        actual = unity_library_cache_is_ignored(root, PROBE_PATH)
        if actual is not expected:
            raise AssertionError(
                f"ignore rule {rule!r} returned {actual}; expected {expected}"
            )


def main():
    require_ignore_result("", False)
    require_ignore_result("#/UnityTwitter/Library/\n", False)
    require_ignore_result("/UnityTwitter/Library/\n", True)
    require_ignore_result("/UnityTwitter/Library/\n!/UnityTwitter/Library/\n", False)
    print("Generated Unity cache ignore mutations passed (4 cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
