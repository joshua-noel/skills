#!/usr/bin/env node
// Put a rendered SVG into a page in place of {{SVG}}, so the model never copies the SVG by hand.
// Usage: node inline.mjs <page.html> <diagram.svg>   (edits page.html in place)
import { readFileSync, writeFileSync } from "node:fs";

const [page, svg] = process.argv.slice(2);
if (!page || !svg) { console.error("Usage: node inline.mjs <page.html> <diagram.svg>"); process.exit(2); }
const html = readFileSync(page, "utf8");
if (!html.includes("{{SVG}}")) { console.error(`${page}: no {{SVG}} placeholder`); process.exit(1); }
const out = html.replace("{{SVG}}", () => readFileSync(svg, "utf8"));
writeFileSync(page, out);
const left = out.match(/\{\{[^}]*\}\}/g) ?? [];
console.log(`inlined ${svg} into ${page}` + (left.length ? `; placeholders left: ${[...new Set(left)].join(", ")}` : ""));
