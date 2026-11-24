#!/usr/bin/env python3
"""news-image-20261123 entrypoint.

Copies the front page (front-page.png) built for this entry to the
output directory as entry.png. Before copying it checks the file is a
real PNG, no bigger than 1 MiB and no larger than 1024x1024 pixels.
Python 3.13 standard library only; no network access. Deterministic:
every run writes the same bytes.
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "front-page.png")
LIMIT_BYTES = 1048576
LIMIT_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_chunks(blob):
    """Walk every PNG chunk, verifying CRCs; require IEND with no tail."""
    cursor = 8
    first = True
    saw_iend = False
    while cursor < len(blob):
        if cursor + 8 > len(blob):
            raise ValueError("chunk header cut short at offset %d" % cursor)
        size = struct.unpack(">I", blob[cursor:cursor + 4])[0]
        kind = blob[cursor + 4:cursor + 8]
        stop = cursor + 8 + size + 4
        if stop > len(blob):
            raise ValueError(
                "chunk %s runs past the end of the file"
                % kind.decode("latin-1")
            )
        stored = struct.unpack(">I", blob[stop - 4:stop])[0]
        actual = zlib.crc32(kind + blob[cursor + 8:cursor + 8 + size])
        actual &= 0xFFFFFFFF
        if stored != actual:
            raise ValueError(
                "checksum mismatch in %s chunk" % kind.decode("latin-1")
            )
        if first and kind != b"IHDR":
            raise ValueError("first chunk is not IHDR")
        first = False
        cursor = stop
        if kind == b"IEND":
            saw_iend = True
            break
    if not saw_iend:
        raise ValueError("PNG has no IEND chunk")
    if cursor != len(blob):
        raise ValueError(
            "%d trailing bytes after IEND" % (len(blob) - cursor)
        )


def inspect(path):
    """Return (width, height, size, sha256) after validating the PNG."""
    with open(path, "rb") as handle:
        blob = handle.read()
    if blob[:8] != PNG_MAGIC:
        raise ValueError("front-page.png is not a PNG file")
    if len(blob) > LIMIT_BYTES:
        raise ValueError(
            "front-page.png is %d bytes, over the 1 MiB limit" % len(blob)
        )
    check_chunks(blob)
    width, height = struct.unpack(">II", blob[16:24])
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        raise ValueError(
            "image is %dx%d, over the 1024x1024 limit" % (width, height)
        )
    return width, height, len(blob), hashlib.sha256(blob).hexdigest()


def main():
    target = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    width, height, size, digest = inspect(SOURCE)
    os.makedirs(target, exist_ok=True)
    destination = os.path.join(target, "entry.png")
    shutil.copyfile(SOURCE, destination)
    with open(destination, "rb") as handle:
        copied = handle.read()
    if hashlib.sha256(copied).hexdigest() != digest:
        raise ValueError("entry.png does not match front-page.png")
    print(
        "wrote %s (%dx%d, %d bytes, sha256 %s)"
        % (destination, width, height, size, digest)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
