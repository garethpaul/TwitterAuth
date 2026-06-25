#!/usr/bin/env python3
"""Mutation test for the checked-in authentication-only scene default."""

from pathlib import Path

from check_unity_contracts import demo_scene_posting_is_disabled


ROOT = Path(__file__).resolve().parents[1]
SCENE_PATH = ROOT / "UnityTwitter" / "Assets" / "Demo.unity"
POSTING_FIELD = b"ALLOW_TWEET_POSTING"


def main():
    scene = SCENE_PATH.read_bytes()
    if not demo_scene_posting_is_disabled(scene):
        raise AssertionError("checked-in Demo scene must omit the posting opt-in")

    mutated_scene = scene + b"\0" + POSTING_FIELD + b"\0"
    if demo_scene_posting_is_disabled(mutated_scene):
        raise AssertionError("serialized posting opt-in mutation was not rejected")

    print("Authentication-only scene mutation rejected (1 case).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
