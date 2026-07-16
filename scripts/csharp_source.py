#!/usr/bin/env python3
"""C# source scanning helpers for the static contracts.

The repository's contracts assert C# source *text*. A raw-text assertion cannot
tell live code from commented-out code: commenting a guard preserves every
asserted literal verbatim, so the contract stays green while the guard is dead.

`blank_comments` removes that blind spot by blanking comments to spaces before a
contract asserts against the source.

Why a scanner and not a regular expression: `line.split("//", 1)[0]` truncates
string literals, and this repository's sources contain
`Application.OpenURL("https://dev.twitter.com/apps/new")` plus verbatim regex
literals. Splitting on `//` would corrupt them and fail correct source. The
scanner therefore tracks regular, verbatim, and interpolated string literals,
character literals, and escape sequences.

Comments are blanked to spaces rather than deleted so that every byte offset in
the returned text matches the input. Contracts that locate a structural
delimiter in the raw source (for example a `// PIN Input` section marker) can
reuse those offsets against the blanked text unchanged. Newlines are preserved
so line-oriented logic and diagnostics keep working.
"""


def blank_comments(source):
    """Return `source` with comment bodies replaced by spaces.

    Newlines are preserved. Every other character keeps its offset, so
    `len(blank_comments(s)) == len(s)`.
    """
    out = list(source)
    index = 0
    length = len(source)

    def blank(start, stop):
        for position in range(start, stop):
            if out[position] != "\n":
                out[position] = " "

    while index < length:
        character = source[index]

        # --- comments -----------------------------------------------------
        if character == "/" and index + 1 < length:
            following = source[index + 1]
            if following == "/":
                stop = source.find("\n", index)
                stop = length if stop == -1 else stop
                blank(index, stop)
                index = stop
                continue
            if following == "*":
                stop = source.find("*/", index + 2)
                stop = length if stop == -1 else stop + 2
                blank(index, stop)
                index = stop
                continue

        # --- string literals ---------------------------------------------
        # Prefixes: "  $"  @"  $@"  @$"
        prefix_length = 0
        verbatim = False
        if character == '"':
            prefix_length = 1
        elif character in "$@" and index + 1 < length:
            second = source[index + 1]
            if second == '"':
                prefix_length = 2
                verbatim = character == "@"
            elif (
                second in "$@"
                and second != character
                and index + 2 < length
                and source[index + 2] == '"'
            ):
                prefix_length = 3
                verbatim = True

        if prefix_length:
            index += prefix_length  # now just past the opening quote
            if verbatim:
                while index < length:
                    if source[index] == '"':
                        if index + 1 < length and source[index + 1] == '"':
                            index += 2  # "" is an escaped quote
                            continue
                        index += 1
                        break
                    index += 1
            else:
                while index < length:
                    current = source[index]
                    if current == "\\":
                        index += 2
                        continue
                    if current == '"' or current == "\n":
                        index += 1
                        break
                    index += 1
            continue

        # --- character literals -------------------------------------------
        if character == "'":
            index += 1
            while index < length:
                current = source[index]
                if current == "\\":
                    index += 2
                    continue
                if current == "'" or current == "\n":
                    index += 1
                    break
                index += 1
            continue

        index += 1

    return "".join(out)
