#!/usr/bin/env python3
"""Ship the front page for Monday 23 November 2026.

The repository holds one finished newspaper front page,
``front-page.png``. This program checks it against the entry rules
for the make.fun news-image bounty and, when it passes, places an
exact copy at ``$MAKEFUN_OUTPUT_DIR/entry.png`` (``/output/entry.png``
when that variable is unset).

Checks performed, all with the standard library only:

* the file is a real PNG (magic bytes) and no bigger than 1 MiB;
* its picture is at most 1024 pixels on either side;
* every chunk carries a correct CRC32, the first chunk is IHDR,
  and the file ends with a proper IEND chunk and nothing after it.

Nothing here draws or alters the picture: the shipped file is the
same bytes as the source, so the run is deterministic.
"""

from __future__ import annotations

import os
import struct
import sys
import zlib
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_FILE_BYTES = 1 << 20  # 1 MiB, the entry ceiling
MAX_SIDE_PIXELS = 1024
SOURCE_NAME = "front-page.png"
DEST_NAME = "entry.png"


class FrontPageError(Exception):
    """The front page breaks one of the entry rules."""


def _u32be(blob: bytes, at: int) -> int:
    """One unsigned big-endian 32-bit word out of ``blob``."""
    return struct.unpack_from(">I", blob, at)[0]


def _read_source() -> bytes:
    """Load the front page and check its size and magic bytes."""
    here = Path(__file__).resolve().parent
    raw = (here / SOURCE_NAME).read_bytes()
    if len(raw) > MAX_FILE_BYTES:
        raise FrontPageError(
            f"{SOURCE_NAME} is {len(raw)} bytes, over the 1 MiB ceiling"
        )
    if raw[: len(PNG_MAGIC)] != PNG_MAGIC:
        raise FrontPageError(f"{SOURCE_NAME} does not start with PNG magic bytes")
    return raw


def _dimensions(raw: bytes) -> tuple[int, int]:
    """Width and height out of the IHDR chunk at the head of the file."""
    if len(raw) < 8 + 8 + 13 + 4:
        raise FrontPageError("file too short to hold an IHDR chunk")
    if _u32be(raw, 8) != 13 or raw[12:16] != b"IHDR":
        raise FrontPageError("first chunk is not a 13-byte IHDR")
    return _u32be(raw, 16), _u32be(raw, 20)


def _walk_chunks(raw: bytes) -> None:
    """Walk every chunk, checking CRC32s and the closing IEND."""
    offset = 8
    first = True
    closed = False
    while offset < len(raw):
        if offset + 8 > len(raw):
            raise FrontPageError(f"truncated chunk header at byte {offset}")
        length = _u32be(raw, offset)
        kind = raw[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        if data_end + 4 > len(raw):
            raise FrontPageError(f"chunk {kind!r} runs past the end of the file")
        stored_crc = _u32be(raw, data_end)
        actual_crc = zlib.crc32(raw[offset + 4 : data_end]) & 0xFFFFFFFF
        if actual_crc != stored_crc:
            raise FrontPageError(f"chunk {kind!r} has a bad CRC32")
        if first and kind != b"IHDR":
            raise FrontPageError("first chunk is not IHDR")
        first = False
        if kind == b"IEND":
            if length != 0:
                raise FrontPageError("IEND chunk carries data")
            if data_end + 4 != len(raw):
                raise FrontPageError("bytes follow the IEND chunk")
            closed = True
            break
        offset = data_end + 4
    if not closed:
        raise FrontPageError("no closing IEND chunk found")


def _ship(raw: bytes) -> Path:
    """Write the validated bytes to the output entry path."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / DEST_NAME
    dest.write_bytes(raw)
    return dest


def main() -> int:
    try:
        raw = _read_source()
        width, height = _dimensions(raw)
        if width > MAX_SIDE_PIXELS or height > MAX_SIDE_PIXELS:
            raise FrontPageError(
                f"picture is {width}x{height}, over the 1024x1024 ceiling"
            )
        _walk_chunks(raw)
    except FrontPageError as exc:
        print(f"front page rejected: {exc}", file=sys.stderr)
        return 1
    dest = _ship(raw)
    print(f"front page ok: {len(raw)} bytes -> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
