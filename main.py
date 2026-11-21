#!/usr/bin/env python3
"""Deliver the finished 20 November front page to the grading folder.

The picture was painted in advance by render.py (Pillow) and sits next
to this file as entry.png. This runner is deliberately boring: it uses
only the standard library, touches no network, and copies the exact
bytes into the folder the grader names. It then reads the copy back
and compares fingerprints, so a truncated or altered write fails
loudly instead of shipping a broken image.

The output folder comes from MAKEFUN_OUTPUT_DIR when the grader sets
it and falls back to /output otherwise.
"""

import hashlib
import os
import shutil
from pathlib import Path


def fingerprint(data):
    return hashlib.sha256(data).hexdigest()


def publish():
    root = Path(__file__).resolve().parent
    picture = root / "entry.png"
    original = picture.read_bytes()
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(picture, target)
    delivered = target.read_bytes()
    if fingerprint(delivered) != fingerprint(original):
        raise SystemExit("entry.png changed during the copy; refusing to ship it")
    print(f"delivered {target} ({len(delivered)} bytes, sha256 {fingerprint(delivered)})")


if __name__ == "__main__":
    publish()
