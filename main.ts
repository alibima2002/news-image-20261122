// news-image-20261122 entrypoint (Node 22, stdlib only).
// Copies the pre-rendered infographic entry.png next to this file into
// $MAKEFUN_OUTPUT_DIR/entry.png, byte for byte, then proves it by
// reading both files back and comparing every byte.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");

copyFileSync(source, target);

const a = readFileSync(source);
const b = readFileSync(target);
if (!a.equals(b)) {
  throw new Error(`byte mismatch: source ${a.length} bytes, output ${b.length} bytes`);
}
console.log(`wrote ${target} (${b.length} bytes, byte-identical)`);
