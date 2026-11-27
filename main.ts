// news-image-20261127 — "The World in a Day", Friday 27 November 2026.
//
// The deliverable is the front-page picture committed next to this file
// as entry.png. This program's job is narrow: prove the picture is a
// well-formed PNG inside the competition's limits, then place an exact
// copy of it in the output directory.

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024; // the 1 MiB ceiling from the rules
const MAX_SIDE = 1024;         // neither dimension may exceed this

function refuse(message: string): never {
  console.error("entry.png refused: " + message);
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const png = readFileSync(join(here, "entry.png"));

if (png.byteLength === 0) refuse("the file is empty");
if (png.byteLength > MAX_BYTES) {
  refuse("the file weighs " + png.byteLength + " bytes, past the 1 MiB limit");
}

// A PNG opens with an eight-byte signature; anything else is not a PNG.
const SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < SIGNATURE.length; i++) {
  if (png[i] !== SIGNATURE[i]) refuse("byte " + i + " breaks the PNG signature");
}

// The first chunk is always IHDR, and its payload begins with the width
// and the height as big-endian 32-bit integers (bytes 16 and 20).
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width === 0 || height === 0) refuse("IHDR claims a zero-sized picture");
if (width > MAX_SIDE || height > MAX_SIDE) {
  refuse("the picture is " + width + "x" + height + ", past 1024x1024");
}

// Walk the chunk list from just after the signature to the end of the
// file. Every chunk is length + type + data + CRC-32, and the CRC covers
// the type bytes and the data bytes. The walk has to finish exactly on
// the file's final byte, immediately after an IEND chunk; a file that
// ends early, overruns, or fails a CRC is corrupt and gets refused.
const crcTable = new Int32Array(256);
for (let n = 0; n < 256; n++) {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  crcTable[n] = c;
}
function crc32(slice: Buffer): number {
  let crc = -1;
  for (const byte of slice) crc = crcTable[(crc ^ byte) & 0xff] ^ (crc >>> 8);
  return (crc ^ -1) >>> 0;
}

let offset = 8;
let sawIend = false;
while (offset < png.byteLength) {
  if (offset + 12 > png.byteLength) refuse("a chunk header runs past the end");
  const length = png.readUInt32BE(offset);
  const type = png.toString("ascii", offset + 4, offset + 8);
  const dataStart = offset + 8;
  const dataEnd = dataStart + length;
  if (dataEnd + 4 > png.byteLength) refuse("chunk " + type + " runs past the end");
  const stored = png.readUInt32BE(dataEnd);
  const actual = crc32(png.subarray(offset + 4, dataEnd));
  if (stored !== actual) refuse("chunk " + type + " fails its CRC check");
  offset = dataEnd + 4;
  if (type === "IEND") { sawIend = true; break; }
}
if (!sawIend) refuse("no IEND chunk — the picture is truncated");
if (offset !== png.byteLength) refuse("trailing bytes after IEND");

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
writeFileSync(target, png);

console.log(
  "entry.png delivered: " + width + "x" + height + ", " +
  png.byteLength + " bytes -> " + target
);
