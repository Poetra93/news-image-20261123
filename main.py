#!/usr/bin/env python3
"""Ship the 23 November 2026 news front page as this entry's image.

The repository holds the finished front page as ``front-page.png``.
This program checks that the file is a whole PNG inside the
competition's limits and then copies it byte for byte to
``entry.png`` in the output directory, so both runs of the program
write exactly the same bytes.

Checks performed, in order:
  1. the file exists and is at most 1 MiB;
  2. the first eight bytes are the PNG signature;
  3. the first chunk is IHDR and its width and height are each
     between 1 and 1024 pixels;
  4. every chunk's CRC32 (over chunk type + chunk data) matches,
     no chunk runs past the end of the file, and the file ends
     with a zero-length IEND chunk and nothing after it.

Any failure exits non-zero with a plain-language reason.
Only the standard library is used.
"""

import os
import struct
import sys
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
SOURCE_NAME = "front-page.png"
TARGET_NAME = "entry.png"


class NewsImageError(Exception):
    """Raised when the front page fails any of the entry checks."""


def _u32be(buf, offset):
    """Read one unsigned 32-bit big-endian integer from buf."""
    return struct.unpack_from(">I", buf, offset)[0]


def _load_source(path):
    """Read the source file and reject it if it is too large."""
    try:
        with open(path, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        raise NewsImageError("cannot read %s: %s" % (path, exc))
    if not data:
        raise NewsImageError("source file is empty")
    if len(data) > MAX_BYTES:
        raise NewsImageError(
            "source is %d bytes, over the 1 MiB limit" % len(data)
        )
    return data


def _check_signature(data):
    """The first eight bytes must be the PNG signature."""
    if data[: len(PNG_SIGNATURE)] != PNG_SIGNATURE:
        raise NewsImageError("first bytes are not the PNG signature")


def _read_dimensions(data):
    """Parse the IHDR chunk and return (width, height).

    IHDR must be the first chunk, it must carry exactly 13 bytes,
    and both sides must fit inside 1024 pixels.
    """
    if len(data) < 8 + 8 + 13 + 4:
        raise NewsImageError("file too short to hold an IHDR chunk")
    length = _u32be(data, 8)
    kind = data[12:16]
    if kind != b"IHDR":
        raise NewsImageError("first chunk is %r, not IHDR" % kind)
    if length != 13:
        raise NewsImageError("IHDR chunk is %d bytes, expected 13" % length)
    width = _u32be(data, 16)
    height = _u32be(data, 20)
    if width < 1 or width > MAX_SIDE or height < 1 or height > MAX_SIDE:
        raise NewsImageError(
            "image is %dx%d, over the 1024x1024 limit" % (width, height)
        )
    return width, height


def _walk_chunks(data):
    """Walk every chunk, checking lengths and CRC32s.

    Returns the number of chunks seen. A chunk is length (4 bytes),
    type (4 bytes), data (length bytes) and CRC32 (4 bytes), the CRC
    covering type + data. The walk ends at IEND, which must be the
    last thing in the file. At least one IDAT chunk must appear,
    otherwise the file carries no image data at all.
    """
    offset = 8
    seen = 0
    seen_idat = False
    while True:
        if offset + 8 > len(data):
            raise NewsImageError("chunk header runs past the end of file")
        length = _u32be(data, offset)
        kind = data[offset + 4 : offset + 8]
        if kind == b"IDAT":
            seen_idat = True
        body_start = offset + 8
        body_end = body_start + length
        if body_end + 4 > len(data):
            raise NewsImageError(
                "chunk %r claims %d bytes past the end of file"
                % (kind, body_end + 4 - len(data))
            )
        wanted = zlib.crc32(data[offset + 4 : body_end]) & 0xFFFFFFFF
        stored = _u32be(data, body_end)
        if wanted != stored:
            raise NewsImageError(
                "chunk %r has a bad CRC32" % kind
            )
        seen += 1
        offset = body_end + 4
        if kind == b"IEND":
            if length != 0:
                raise NewsImageError("IEND chunk carries data")
            if not seen_idat:
                raise NewsImageError("no IDAT chunk: file has no image data")
            if offset != len(data):
                raise NewsImageError(
                    "%d trailing bytes after IEND" % (len(data) - offset)
                )
            return seen


def _emit(data, out_dir):
    """Write the validated bytes to entry.png in out_dir."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, TARGET_NAME)
    with open(target, "wb") as handle:
        handle.write(data)
    return target


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        data = _load_source(source)
        _check_signature(data)
        width, height = _read_dimensions(data)
        chunks = _walk_chunks(data)
        target = _emit(data, out_dir)
    except NewsImageError as exc:
        print("news-image-20261123: invalid front page: %s" % exc,
              file=sys.stderr)
        return 1
    print(
        "wrote %s (%dx%d, %d chunks, %d bytes)"
        % (target, width, height, chunks, len(data))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
