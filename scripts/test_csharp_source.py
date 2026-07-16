#!/usr/bin/env python3
"""Executable tests for the C# comment scanner.

These run the scanner; they do not assert its source text.
"""

from pathlib import Path

from csharp_source import blank_comments


ROOT = Path(__file__).resolve().parents[1]
DEMO_PATH = ROOT / "UnityTwitter" / "Assets" / "Demo.cs"
API_PATH = ROOT / "UnityTwitter" / "Assets" / "Twitter.cs"


CASES = (
    # (name, source, expected)
    ("line comment is blanked", "int a; // gone\n", "int a;        \n"),
    ("block comment is blanked", "int a; /* gone */ int b;", "int a;            int b;"),
    (
        "block comment keeps newlines",
        "a;\n/* one\ntwo */\nb;",
        "a;\n      \n      \nb;",
    ),
    (
        "// inside a regular string survives",
        'OpenURL("https://dev.twitter.com/apps/new");',
        'OpenURL("https://dev.twitter.com/apps/new");',
    ),
    (
        "/* inside a regular string survives",
        'var s = "/* not a comment */";',
        'var s = "/* not a comment */";',
    ),
    (
        "// inside a verbatim string survives",
        'var s = @"https://api.twitter.com/oauth";',
        'var s = @"https://api.twitter.com/oauth";',
    ),
    (
        "escaped quote does not end a regular string",
        'var s = "a\\" // still string"; // gone\n',
        'var s = "a\\" // still string";        \n',
    ),
    (
        "doubled quote does not end a verbatim string",
        'var s = @"a""// still string"; // gone\n',
        'var s = @"a""// still string";        \n',
    ),
    (
        "interpolated string is respected",
        'var s = $"x{y}// not a comment"; // gone\n',
        'var s = $"x{y}// not a comment";        \n',
    ),
    (
        "interpolated verbatim string is respected",
        'var s = $@"a""//keep"; // gone\n',
        'var s = $@"a""//keep";        \n',
    ),
    (
        "verbatim interpolated (@$) string is respected",
        'var s = @$"a""//keep"; // gone\n',
        'var s = @$"a""//keep";        \n',
    ),
    (
        "quote character literal does not open a string",
        "if (c == '\"') { } // gone\n",
        "if (c == '\"') { }        \n",
    ),
    (
        "escaped backslash char literal",
        "if (c == '\\\\') { } // gone\n",
        "if (c == '\\\\') { }        \n",
    ),
    (
        "division is not a comment",
        "int a = b / c; int d = e / f;",
        "int a = b / c; int d = e / f;",
    ),
    (
        "unterminated block comment is blanked to end",
        "a; /* trailing",
        "a;            ",
    ),
    (
        "commented-out guard loses its literal",
        "        // if (!ALLOW_TWEET_POSTING)\n",
        "                                    \n",
    ),
)


def main():
    passed = 0
    for name, source, expected in CASES:
        actual = blank_comments(source)
        if actual != expected:
            raise AssertionError(
                f"comment scanner case failed: {name}\n"
                f"  source   : {source!r}\n"
                f"  expected : {expected!r}\n"
                f"  actual   : {actual!r}"
            )
        if len(actual) != len(source):
            raise AssertionError(f"comment scanner changed offsets: {name}")
        passed += 1

    # Offset preservation and literal safety on the real checked-in sources.
    for path in (DEMO_PATH, API_PATH):
        source = path.read_text(encoding="utf-8")
        blanked = blank_comments(source)
        if len(blanked) != len(source):
            raise AssertionError(f"{path.name}: comment scanner did not preserve offsets")
        if blanked.count("\n") != source.count("\n"):
            raise AssertionError(f"{path.name}: comment scanner did not preserve line count")
        passed += 2

    # The scanner must not corrupt string literals in the real sources. A naive
    # `split("//")` stripper truncates this URL and would fail correct source.
    demo_blanked = blank_comments(DEMO_PATH.read_text(encoding="utf-8"))
    if "https://dev.twitter.com/apps/new" not in demo_blanked:
        raise AssertionError("comment scanner corrupted the HTTPS registration URL")
    passed += 1

    api_blanked = blank_comments(API_PATH.read_text(encoding="utf-8"))
    for literal in ('@"<error>([^&]+)</error>"', '@"(?:^|&)"'):
        if literal not in api_blanked:
            raise AssertionError(f"comment scanner corrupted verbatim literal: {literal}")
        passed += 1

    # Real comments in the checked-in sources must actually be removed.
    for comment in ("Use this for initialization", "Update is called once per frame"):
        if comment not in DEMO_PATH.read_text(encoding="utf-8"):
            raise AssertionError(f"test fixture drifted: {comment} is no longer in Demo.cs")
        if comment in demo_blanked:
            raise AssertionError(f"comment scanner left a comment behind: {comment}")
        passed += 1

    print(f"C# comment scanner tests passed ({passed} cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
