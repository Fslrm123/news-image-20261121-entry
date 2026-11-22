#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261121.

Copies the shipped front-page image (entry.png, rendered offline by
draw.py with Pillow) to the output directory: MAKEFUN_OUTPUT_DIR when
set, else /output. Standard library only; no network. Both runs write
identical bytes because the source file is fixed.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print(f"missing image: {src}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
