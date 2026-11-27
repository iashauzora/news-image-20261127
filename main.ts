// news-image-20261127 entry program.
//
// The repository ships a finished front-page image, entry.png, beside
// this file. This program checks that the image really is a whole,
// in-limits PNG, then copies it byte-for-byte into the output
// directory the runner names (MAKEFUN_OUTPUT_DIR, default /output)
// and prints a one-line summary.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1048576; // 1 MiB, the competition's size cap
const MAX_SIDE = 1024; // pixels, the competition's dimension cap
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const here = dirname(fileURLToPath(import.meta.url));
const sourcePath = join(here, "entry.png");

function fail(message: string): never {
  throw new Error("entry.png rejected: " + message);
}

function u32(buf: Buffer, offset: number): number {
  return buf.readUInt32BE(offset);
}

function chunkType(buf: Buffer, offset: number): string {
  return buf.toString("ascii", offset + 4, offset + 8);
}

// CRC-32, the checksum PNG stamps on every chunk, computed over the
// chunk's type bytes followed by its data bytes. The table is built
// once from the reflected polynomial 0xedb88320.
const CRC_TABLE: number[] = (() => {
  const table: number[] = [];
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    }
    table.push(c >>> 0);
  }
  return table;
})();

function crc32(buf: Buffer, start: number, end: number): number {
  let crc = 0xffffffff;
  for (let i = start; i < end; i++) {
    crc = CRC_TABLE[(crc ^ buf[i]) & 0xff] ^ (crc >>> 8);
  }
  return (crc ^ 0xffffffff) >>> 0;
}

// Compare the stored checksum of the chunk whose length field sits
// at `offset` against a fresh CRC of its type and data bytes.
function checkChunkCrc(buf: Buffer, offset: number): void {
  const length = u32(buf, offset);
  const stored = u32(buf, offset + 8 + length);
  const actual = crc32(buf, offset + 4, offset + 8 + length);
  if (stored !== actual) {
    fail("chunk " + chunkType(buf, offset) + " fails its CRC check");
  }
}

// Validate the PNG held in buf and return its dimensions. The chunk
// walk follows each chunk's declared length, verifies every chunk's
// CRC, and has to land exactly on the end of the file, just past
// the IEND chunk.
function checkImage(buf: Buffer): { width: number; height: number } {
  if (buf.length < PNG_SIGNATURE.length) {
    fail("file is too short to be a PNG");
  }
  if (buf.length > MAX_BYTES) {
    fail("file is over 1 MiB");
  }
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (buf[i] !== PNG_SIGNATURE[i]) {
      fail("missing PNG signature");
    }
  }

  // The first chunk must be IHDR with its 13 bytes of header data.
  let offset = 8;
  if (offset + 8 > buf.length) {
    fail("truncated before the first chunk");
  }
  if (chunkType(buf, offset) !== "IHDR" || u32(buf, offset) !== 13) {
    fail("first chunk is not a 13-byte IHDR");
  }
  const width = u32(buf, offset + 8);
  const height = u32(buf, offset + 12);
  if (width === 0 || height === 0) {
    fail("image has a zero-length side");
  }
  if (width > MAX_SIDE || height > MAX_SIDE) {
    fail("image is over 1024 pixels on a side");
  }
  checkChunkCrc(buf, offset);
  offset += 8 + 13 + 4; // header, IHDR data, IHDR checksum

  let sawIend = false;
  while (offset < buf.length) {
    if (offset + 8 > buf.length) {
      fail("truncated chunk header");
    }
    const length = u32(buf, offset);
    const type = chunkType(buf, offset);
    const next = offset + 8 + length + 4;
    if (next > buf.length) {
      fail("chunk " + type + " runs past the end of the file");
    }
    checkChunkCrc(buf, offset);
    offset = next;
    if (type === "IEND") {
      sawIend = true;
      break;
    }
  }
  if (!sawIend) {
    fail("no IEND chunk");
  }
  if (offset !== buf.length) {
    fail("bytes follow the IEND chunk");
  }
  return { width, height };
}

if (!existsSync(sourcePath)) {
  fail("entry.png is missing beside main.ts");
}
const image = readFileSync(sourcePath);
const size = checkImage(image);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "entry.png");
copyFileSync(sourcePath, outPath);

console.log(
  "entry.png: " +
    image.length +
    " bytes, " +
    size.width +
    "x" +
    size.height +
    ", PNG checks passed, copied to " +
    outPath,
);
