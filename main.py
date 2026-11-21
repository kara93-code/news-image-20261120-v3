#!/usr/bin/env python3
"""news-image-20261120 entry, v3 (AI-2 globe front page).

The picture was prepared on the dev machine and is bundled as
assets/entry.jpg (1024x683 JPEG, 307,878 bytes). This program only
checks that the bundled file is really the picture it claims to be,
then hands an exact copy to the grader as /output/entry.png.

No network, no Pillow, no third-party code: the grading sandbox runs
Python 3.13 with the standard library only, so this file imports
nothing beyond it.
"""

import hashlib
import os
import sys

MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8\xff"
EXPECTED_SHA256 = "63c4154869a2b25e7c62456254381a31a0460e0a94bf41850b281027e0bddd99"
EXPECTED_SIZE = 307878


def asset_bytes():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "assets", "entry.jpg")
    with open(path, "rb") as handle:
        return handle.read()


def looks_like_jpeg(blob):
    return blob[:3] == JPEG_MAGIC and blob[-2:] == b"\xff\xd9"


def run(argv):
    blob = asset_bytes()
    if not looks_like_jpeg(blob):
        raise SystemExit("assets/entry.jpg is not a whole JPEG")
    if len(blob) > MAX_BYTES:
        raise SystemExit("assets/entry.jpg is over the 1 MiB limit")
    if len(blob) != EXPECTED_SIZE:
        raise SystemExit("assets/entry.jpg has an unexpected size")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("assets/entry.jpg does not match its recorded hash")
    outdir = argv[1] if len(argv) > 1 else os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    target = os.path.join(outdir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(blob)
    os.chmod(target, 0o644)
    with open(target, "rb") as handle:
        written = handle.read()
    if written != blob:
        raise SystemExit("read-back mismatch: the output is not the bundled picture")
    if os.stat(target).st_mode & 0o777 != 0o644:
        raise SystemExit("output mode is not 0644")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv))
