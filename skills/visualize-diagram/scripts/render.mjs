#!/usr/bin/env node
// Render a diagram spec (JSON) to one self-contained, interactive SVG.
// Usage: node render.mjs <spec.json> <out.svg> [--light]
// No dependencies. The output opens directly in a browser and can be inlined in HTML.
import { readFileSync, writeFileSync } from "node:fs";
import { basename } from "node:path";

const [input, output, ...flags] = process.argv.slice(2);
if (!input || !output) {
  console.error("Usage: node render.mjs <spec.json> <out.svg> [--light]");
  process.exit(2);
}
const spec = JSON.parse(readFileSync(input, "utf8"));
const light = flags.includes("--light") || spec.theme === "light";
// Unique per output file; prefixed so it is a valid CSS id even if the file name starts with a digit.
const uid = "dg-" + basename(output).replace(/\.[^.]+$/, "").replace(/[^a-zA-Z0-9_-]/g, "-");

// ---- Theme: clean-card arrows on console-style nodes. Dark is the default. ----
const T = light ? {
  bg: "#ffffff", ink: "#1f2937", muted: "#6b7280", groupFill: "#f6f8fa", groupStroke: "#e5e7eb",
  nodeFill: "#ffffff", nodeStroke: "#d0d7de", actorFill: "#f1f5f9", edge: "#94a3b8",
  badge: "#b7791f", badgeText: "#ffffff", tipFill: "#ffffff", tipStroke: "#d0d7de", actor: "#64748b",
  accents: ["#7c3aed", "#16a34a", "#d97706", "#0284c7", "#db2777", "#0891b2"],
} : {
  bg: "#1c2129", ink: "#e6edf3", muted: "#9ba5b3", groupFill: "#212731", groupStroke: "#2f3742",
  nodeFill: "#272e38", nodeStroke: "#3a4350", actorFill: "#2b333e", edge: "#8b98a9",
  badge: "#f0b429", badgeText: "#1c2129", tipFill: "#272e38", tipStroke: "#3a4350", actor: "#9ba5b3",
  accents: ["#a371f7", "#3fb950", "#f0b429", "#58a6ff", "#f778ba", "#39c5cf"],
};
const SANS = "'Segoe UI', Inter, system-ui, sans-serif", MONO = "'Cascadia Code', Consolas, monospace";

// ---- Validate the spec ----
const columns = spec.columns ?? [];
const shared = spec.shared ?? null;
const edges = spec.edges ?? [];
const steps = spec.steps ?? [];
const fail = msg => { console.error(`spec error: ${msg}`); process.exit(1); };
if (!columns.length) fail("columns[] is empty");
const byId = new Map();
columns.forEach((c, ci) => (c.nodes ?? []).forEach(n => {
  if (byId.has(n.id)) fail(`duplicate node id "${n.id}"`);
  byId.set(n.id, Object.assign(n, { ci, actor: !!c.actors }));
}));
(shared?.nodes ?? []).forEach(n => {
  if (byId.has(n.id)) fail(`duplicate node id "${n.id}"`);
  byId.set(n.id, Object.assign(n, { ci: -1, shared: true }));
});
edges.forEach((e, i) => {
  if (!byId.has(e.from)) fail(`edges[${i}].from "${e.from}" is not a node id`);
  if (!byId.has(e.to)) fail(`edges[${i}].to "${e.to}" is not a node id`);
  if (e.step && !steps[e.step - 1]) fail(`edges[${i}].step ${e.step} has no text in steps[]`);
});

// ---- Text helpers ----
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function wrap(s, max, limit = 3) {
  const lines = [];
  let cur = "";
  for (const w of String(s ?? "").split(/\s+/).filter(Boolean)) {
    if ((cur + " " + w).trim().length > max && cur) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim();
  }
  if (cur) lines.push(cur);
  return lines.slice(0, limit);
}

// ---- Layout: columns left to right, a shared row under them, a legend at the bottom. Sheet is 16:9. ----
const M = 40, TOP = 56, GAP = 90, ACTOR_W = 180, PAD = 18, VGAP = 22, NODE_H = 46, LINE_H = 13, CHAR_W = 6.4;
const sharedSpan = () => {
  const first = cols.find(c => !c.actors) ?? cols[0], last = cols[cols.length - 1];
  return { x: first.x, w: last.x + last.w - first.x };
};
let W = 1600, H, cols, areaH, sharedY, sharedH, footY;
// Legend: two columns of steps; the line-style note goes under the shorter second column.
const per = Math.ceil(steps.length / 2), noteRow = steps.length - per;
const footH = steps.length ? 34 + Math.max(per, noteRow + 1) * 22 : 44;
for (let pass = 0; pass < 4; pass++) {
  const groupCols = columns.filter(c => !c.actors).length;
  const actorCols = columns.length - groupCols;
  const groupW = Math.max(220, (W - 2 * M - actorCols * ACTOR_W - GAP * (columns.length - 1)) / Math.max(1, groupCols));
  let x = M;
  cols = columns.map(c => {
    const w = c.actors ? ACTOR_W : groupW;
    const col = { ...c, x, w, inset: c.actors ? 0 : PAD };
    x += w + GAP;
    return col;
  });
  for (const n of byId.values()) {
    if (n.shared) continue;
    const c = cols[n.ci], nw = c.w - 2 * c.inset;
    n.w = nw;
    n.lines = wrap(n.sub, Math.floor((nw - (n.actor ? 40 : 22)) / CHAR_W));
    n.h = NODE_H + LINE_H * Math.max(0, n.lines.length - 1) + (n.actor ? 6 : 0);
  }
  const needCol = Math.max(...cols.map(c => {
    const ns = (c.nodes ?? []);
    return ns.reduce((s, n) => s + n.h, 0) + VGAP * Math.max(0, ns.length - 1) + 2 * PAD + 14;
  }));
  if (shared?.nodes?.length) {
    const span = sharedSpan(), k = shared.nodes.length, nw = (span.w - 2 * PAD - VGAP * (k - 1)) / k;
    for (const n of shared.nodes) {
      n.w = nw;
      n.lines = wrap(n.sub, Math.floor((nw - 22) / CHAR_W), 2);
      n.h = NODE_H + LINE_H * Math.max(0, n.lines.length - 1);
    }
    sharedH = 2 * PAD + Math.max(...shared.nodes.map(n => n.h)) + 6;
  } else sharedH = 0;
  const needH = TOP + needCol + (sharedH ? 44 + sharedH : 0) + 30 + footH + 20;
  if (needH <= Math.round(W * 9 / 16)) break;
  W = Math.ceil(needH * 16 / 9);
}
H = Math.round(W * 9 / 16);
areaH = H - TOP - (sharedH ? 44 + sharedH : 0) - 30 - footH - 20;
sharedY = TOP + areaH + 44;
footY = (sharedH ? sharedY + sharedH : TOP + areaH) + 40;

// Spread nodes evenly down each column so lines have room.
for (const c of cols) {
  const ns = c.nodes ?? [];
  const inner = areaH - 2 * PAD - 14, used = ns.reduce((s, n) => s + n.h, 0);
  const gap = ns.length ? (inner - used) / (ns.length + 1) : 0;
  let y = TOP + PAD + 14 + gap;
  for (const n of ns) { n.x = c.x + c.inset; n.y = y; y += n.h + gap; }
}
if (sharedH) {
  const span = sharedSpan();
  shared.nodes.forEach((n, k) => { n.x = span.x + PAD + k * (n.w + VGAP); n.y = sharedY + PAD + 6; });
}

// ---- Edge routing ----
// kind: "fwd" (left to right), "back" (right to left), "same" (same column), "vert" (to or from the shared row)
const R = edges.map((e, i) => {
  const a = byId.get(e.from), b = byId.get(e.to);
  const kind = a.shared || b.shared ? "vert" : a.ci === b.ci ? "same" : a.ci < b.ci ? "fwd" : "back";
  return { e, i, a, b, kind };
});
// Ports: spread the ends that share one side of a node, sorted by the other end.
const sides = new Map();
const addPort = (n, side, r, end, other) => {
  const k = n.id + side;
  if (!sides.has(k)) sides.set(k, []);
  sides.get(k).push({ r, end, key: side === "top" || side === "bottom" ? other.x + other.w / 2 : other.y + other.h / 2 });
};
for (const r of R) {
  const { a, b, kind } = r;
  if (kind === "fwd") { addPort(a, "right", r, "s", b); addPort(b, "left", r, "t", a); }
  else if (kind === "back") { addPort(a, "left", r, "s", b); addPort(b, "right", r, "t", a); }
  else if (kind === "same") { addPort(a, "right", r, "s", b); addPort(b, "right", r, "t", a); }
  else { const down = a.y < b.y; addPort(a, down ? "bottom" : "top", r, "s", b); addPort(b, down ? "top" : "bottom", r, "t", a); }
}
for (const [k, list] of sides) {
  list.sort((p, q) => p.key - q.key);
  const n = byId.get(list[0].r[list[0].end === "s" ? "a" : "b"].id), vertical = /(top|bottom)$/.test(k);
  list.forEach((p, j) => {
    const f = list.length === 1 ? 0.5 : 0.25 + 0.5 * j / (list.length - 1);
    p.r[p.end + "p"] = vertical ? n.x + n.w * f : n.y + n.h * f;
  });
}
// Bends: edges that bend in the same gap get distinct x positions.
const gaps = new Map();
for (const r of R) {
  if (r.kind !== "fwd" && r.kind !== "back") continue;
  const hi = Math.max(r.a.ci, r.b.ci), target = r.b.ci;
  // Bend in the gap next to the target, so a long edge runs straight before it turns.
  const g = r.kind === "fwd" ? target - 1 : target;
  const gi = Math.min(Math.max(g, 0), hi - 1);
  if (!gaps.has(gi)) gaps.set(gi, []);
  gaps.get(gi).push(r);
}
for (const [gi, list] of gaps) {
  const L = cols[gi].x + cols[gi].w, Rx = cols[gi + 1].x;
  list.sort((p, q) => (p.sp + p.tp) - (q.sp + q.tp));
  list.forEach((r, j) => { r.mx = L + (Rx - L) * (j + 1) / (list.length + 1); });
}
for (const r of R) {
  const { a, b, kind } = r;
  let sx, sy, tx, ty, d, lx, ly;
  if (kind === "vert") {
    const down = a.y < b.y;
    sx = r.sp; tx = r.tp; sy = down ? a.y + a.h : a.y; ty = down ? b.y : b.y + b.h;
    const my = (sy + ty) / 2;
    d = sx === tx ? `M${sx} ${sy} V${ty}` : `M${sx} ${sy} C${sx} ${my}, ${tx} ${my}, ${tx} ${ty}`;
    lx = (sx + tx) / 2; ly = my;
  } else if (kind === "same") {
    sx = a.x + a.w; tx = b.x + b.w; sy = r.sp; ty = r.tp;
    const bx = Math.max(sx, tx) + 40;
    d = `M${sx} ${sy} C${bx} ${sy}, ${bx} ${ty}, ${tx} ${ty}`;
    lx = sx + 30; ly = (sy + ty) / 2;
  } else {
    const back = kind === "back";
    sx = back ? a.x : a.x + a.w; tx = back ? b.x + b.w : b.x; sy = r.sp; ty = r.tp;
    if (Math.abs(sy - ty) < 0.5) { d = `M${sx} ${sy} H${tx}`; lx = (sx + tx) / 2; ly = sy; }
    else { d = `M${sx} ${sy} C${r.mx} ${sy}, ${r.mx} ${ty}, ${tx} ${ty}`; lx = r.mx; ly = (sy + ty) / 2; }
  }
  Object.assign(r, { d, lx, ly });
}

// ---- Accent colour per column ----
let ai = 0;
const colAccent = columns.map(c => c.actors ? T.actor : T.accents[ai++ % T.accents.length]);
const sharedAccent = T.accents[ai % T.accents.length];
const accentOf = n => n.shared ? sharedAccent : colAccent[n.ci];

// ---- SVG ----
const out = [];
const r1 = v => Math.round(v * 10) / 10;
// id scopes the CSS: when the SVG is inlined in a page, its <style> applies to the whole document.
out.push(`<svg xmlns="http://www.w3.org/2000/svg" id="${uid}" viewBox="0 0 ${W} ${H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="${uid}-title" font-family="${SANS}" style="background:${T.bg}" data-steps="${esc(JSON.stringify(steps))}">`);
out.push(`<title id="${uid}-title">${esc(spec.title)}</title>`);
out.push(`<style>
  #${uid} .edge, #${uid} .node, #${uid} .badge { transition: opacity .15s; }
  #${uid}.focus .edge:not(.on), #${uid}.focus .node:not(.on), #${uid}.focus .badge:not(.on) { opacity: .15; }
  #${uid}.focus .edge.on { stroke-width: 2.4px; }
  #${uid} .node { outline: none; cursor: default; }
  #${uid} .node:focus-visible rect:first-child { stroke: ${T.ink}; }
  @media (prefers-reduced-motion: reduce) { #${uid} * { transition: none !important; } }
</style>`);
out.push(`<defs><marker id="${uid}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="${T.edge}"/></marker></defs>`);
out.push(`<rect width="${W}" height="${H}" fill="${T.bg}"/>`);

const groupBoxes = [];
cols.forEach((c, ci) => { if (!c.actors) groupBoxes.push({ x: c.x, y: TOP, w: c.w, h: areaH, title: c.title, sub: c.sub, accent: colAccent[ci] }); });
if (sharedH) { const s = sharedSpan(); groupBoxes.push({ x: s.x, y: sharedY, w: s.w, h: sharedH, title: shared.title, sub: shared.sub, accent: sharedAccent }); }
for (const g of groupBoxes) out.push(`<rect x="${r1(g.x)}" y="${r1(g.y)}" width="${r1(g.w)}" height="${r1(g.h)}" rx="12" fill="${T.groupFill}" stroke="${T.groupStroke}"/>`);

// One badge per step, on the first edge of that step.
const badgeFor = new Map();
for (const r of R) {
  out.push(`<path class="edge" data-i="${r.i}" data-f="${esc(r.e.from)}" data-t="${esc(r.e.to)}" data-back="${r.kind === "back" ? 1 : 0}" data-step="${r.e.step ?? ""}" d="${r.d.replace(/\d+\.\d+/g, v => r1(+v))}" fill="none" stroke="${T.edge}" stroke-width="1.6" stroke-dasharray="${r.e.step ? "" : "5 4"}" marker-end="url(#${uid}-arrow)"><title>${esc(r.e.label ?? "")}</title></path>`);
  if (r.e.step && !badgeFor.has(r.e.step)) badgeFor.set(r.e.step, r);
}
for (const [step, r] of badgeFor) {
  out.push(`<g class="badge" data-i="${r.i}"><circle cx="${r1(r.lx)}" cy="${r1(r.ly)}" r="10" fill="${T.badge}" stroke="${T.bg}" stroke-width="2"/><text x="${r1(r.lx)}" y="${r1(r.ly + 3.5)}" font-size="10.5" font-weight="700" text-anchor="middle" fill="${T.badgeText}">${step}</text></g>`);
}

// Group labels: a chip on the top border, drawn over any line that crosses it.
for (const g of groupBoxes) {
  if (!g.title) continue;
  const w = String(g.title).length * 7.6 + String(g.sub ?? "").length * 5.9 + 34;
  out.push(`<rect x="${r1(g.x + 14)}" y="${r1(g.y - 10)}" width="${r1(w)}" height="20" rx="6" fill="${T.groupFill}" stroke="${T.groupStroke}"/>`);
  out.push(`<text x="${r1(g.x + 24)}" y="${r1(g.y + 4)}" font-size="12" font-weight="700" fill="${g.accent}">${esc(g.title)}<tspan dx="10" font-size="10.5" font-weight="400" fill="${T.muted}">${esc(g.sub)}</tspan></text>`);
}

for (const n of byId.values()) {
  // "|" separates the card's lines: XML turns newlines inside attributes into spaces.
  const c = accentOf(n), d = wrap(n.desc, 46, 6).join("|");
  out.push(`<g class="node" data-id="${esc(n.id)}" data-x="${r1(n.x)}" data-y="${r1(n.y)}" data-w="${r1(n.w)}" data-h="${r1(n.h)}" data-title="${esc(n.title)}" data-sub="${esc(n.sub)}" data-desc="${esc(d)}" tabindex="0" role="button" aria-label="${esc(n.title)}: ${esc(n.desc)}">`);
  if (n.actor) {
    out.push(`<rect x="${r1(n.x)}" y="${r1(n.y)}" width="${r1(n.w)}" height="${r1(n.h)}" rx="${r1(n.h / 2)}" fill="${T.actorFill}" stroke="${T.nodeStroke}"/>`);
    out.push(`<circle cx="${r1(n.x + 20)}" cy="${r1(n.y + n.h / 2)}" r="4" fill="${c}"/>`);
  } else {
    out.push(`<rect x="${r1(n.x)}" y="${r1(n.y)}" width="${r1(n.w)}" height="${r1(n.h)}" rx="4" fill="${T.nodeFill}" stroke="${T.nodeStroke}"/>`);
    out.push(`<rect x="${r1(n.x)}" y="${r1(n.y)}" width="4" height="${r1(n.h)}" rx="2" fill="${c}"/>`);
  }
  const tx = n.x + (n.actor ? 32 : 14);
  // Centre the block: a 13px title plus one 13px row per sub line.
  const ty = n.y + (n.h - 13 * (1 + n.lines.length) - 2) / 2 + 11;
  out.push(`<text x="${r1(tx)}" y="${r1(ty)}" font-size="13" font-weight="700" fill="${T.ink}">${esc(n.title)}</text>`);
  n.lines.forEach((ln, k) => out.push(`<text x="${r1(tx)}" y="${r1(ty + 15 + k * LINE_H)}" font-size="10.5" font-family="${MONO}" fill="${T.muted}">${esc(ln)}</text>`));
  out.push(`</g>`);
}

// Legend and title block.
if (steps.length) {
  out.push(`<text x="${M}" y="${r1(footY)}" font-size="12" font-weight="700" fill="${T.ink}">${esc(spec.legendTitle ?? "Flow")}</text>`);
  const colX = Math.min(520, (W - 2 * M) / 3);
  steps.forEach((s, i) => {
    const x = M + (i < per ? 0 : colX), y = footY + 24 + (i % per) * 22;
    out.push(`<circle cx="${x + 9}" cy="${r1(y - 4)}" r="9" fill="${T.badge}"/><text x="${x + 9}" y="${r1(y)}" font-size="10" font-weight="700" text-anchor="middle" fill="${T.badgeText}">${i + 1}</text>`);
    out.push(`<text x="${x + 26}" y="${r1(y)}" font-size="12" fill="${T.ink}">${esc(s)}</text>`);
  });
  if (edges.some(e => !e.step)) out.push(`<text x="${M + colX}" y="${r1(footY + 24 + noteRow * 22)}" font-size="10.5" fill="${T.muted}">Solid line: numbered flow. Dashed line: other traffic.</text>`);
}
out.push(`<text x="${W - M}" y="${r1(footY)}" font-size="15" font-weight="700" text-anchor="end" fill="${T.ink}">${esc(spec.title)}</text>`);
if (spec.source) out.push(`<text x="${W - M}" y="${r1(footY + 20)}" font-size="11" text-anchor="end" fill="${T.muted}">Source: ${esc(spec.source)}</text>`);

// Hover card, filled by the script.
out.push(`<g class="tip" visibility="hidden" pointer-events="none"><rect rx="8" fill="${T.tipFill}" stroke="${T.tipStroke}"/><text font-size="12.5" fill="${T.ink}"></text></g>`);

// ---- Interaction ----
// Highlight rule for a hovered node:
// 1. Every edge that touches it.
// 2. Forward (left to right) edges, followed downstream.
// 3. Back (right to left) edges into any node reached in 2, one hop only.
// 4. Forward edges traced upstream from it to their origin.
// A node with no edges dims nothing; it only shows its card.
const script = `(() => {
  const svg = document.currentScript.closest("svg");
  const E = [...svg.querySelectorAll(".edge")].map(el => ({ el, f: el.dataset.f, t: el.dataset.t, back: el.dataset.back === "1", step: +el.dataset.step || 0 }));
  const nodes = [...svg.querySelectorAll(".node")], byId = new Map(nodes.map(g => [g.dataset.id, g]));
  const tip = svg.querySelector(".tip"), box = tip.querySelector("rect"), text = tip.querySelector("text");
  const VB = svg.viewBox.baseVal, TW = 330, NS = "http://www.w3.org/2000/svg";
  function pathThrough(id) {
    const ns = new Set([id]), es = new Set(), add = i => { es.add(i); ns.add(E[i].f); ns.add(E[i].t); };
    E.forEach((e, i) => { if (e.f === id || e.t === id) add(i); });
    const reached = new Set([id]), q = [id];
    while (q.length) { const c = q.shift(); E.forEach((e, i) => { if (e.f !== c || e.back) return; add(i); if (!reached.has(e.t)) { reached.add(e.t); q.push(e.t); } }); }
    E.forEach((e, i) => { if (e.back && reached.has(e.t)) add(i); });
    const up = [id], seen = new Set([id]);
    while (up.length) { const c = up.shift(); E.forEach((e, i) => { if (e.t !== c || e.back) return; add(i); if (!seen.has(e.f)) { seen.add(e.f); up.push(e.f); } }); }
    return { ns, es };
  }
  function apply(ns, es) {
    svg.classList.toggle("focus", ns.size > 1);
    nodes.forEach(g => g.classList.toggle("on", ns.has(g.dataset.id)));
    E.forEach((e, i) => e.el.classList.toggle("on", es.has(i)));
    svg.querySelectorAll(".badge").forEach(b => b.classList.toggle("on", es.has(+b.dataset.i)));
  }
  const rect = g => ({ x: +g.dataset.x, y: +g.dataset.y, w: +g.dataset.w, h: +g.dataset.h });
  function showTip(g, count) {
    text.textContent = "";
    const rows = [[g.dataset.title, "700", 13.5, null], [g.dataset.sub, "400", 11, "${MONO}"]]
      .concat(g.dataset.desc.split("|").filter(Boolean).map(l => [l, "400", 12.5, null]));
    if (count) rows.push([count + " connected", "400", 11.5, null]);
    let y = 22;
    rows.forEach(([s, wgt, size, fam], k) => {
      if (!s) return;
      const t = document.createElementNS(NS, "tspan");
      t.setAttribute("x", 12); t.setAttribute("y", y); t.setAttribute("font-weight", wgt); t.setAttribute("font-size", size);
      if (fam) t.setAttribute("font-family", fam);
      if (k === rows.length - 1 && count) t.setAttribute("opacity", ".7");
      t.textContent = s; text.appendChild(t); y += size + 5;
    });
    const th = y - 4;
    box.setAttribute("width", TW); box.setAttribute("height", th);
    const r = rect(g), lit = [...svg.querySelectorAll(".node.on")].filter(x => x !== g).map(rect);
    const clampX = x => Math.max(8, Math.min(x, VB.width - TW - 8));
    const spots = [[clampX(r.x), r.y + r.h + 8], [clampX(r.x), r.y - th - 8], [r.x + r.w + 8, r.y], [r.x - TW - 8, r.y]];
    const fits = ([x, y]) => x >= 8 && y >= 8 && x + TW <= VB.width - 8 && y + th <= VB.height - 8;
    const clear = ([x, y]) => lit.every(b => x > b.x + b.w || x + TW < b.x || y > b.y + b.h || y + th < b.y);
    const [x, y2] = spots.find(s => fits(s) && clear(s)) ?? spots.find(fits) ?? spots[0];
    tip.setAttribute("transform", "translate(" + x + " " + y2 + ")");
    tip.setAttribute("visibility", "visible");
  }
  function off() { svg.classList.remove("focus"); svg.querySelectorAll(".on").forEach(x => x.classList.remove("on")); tip.setAttribute("visibility", "hidden"); }
  function on(g) { const { ns, es } = pathThrough(g.dataset.id); apply(ns, es); showTip(g, ns.size - 1); }
  nodes.forEach(g => {
    g.addEventListener("mouseenter", () => on(g)); g.addEventListener("focus", () => on(g));
    g.addEventListener("mouseleave", off); g.addEventListener("blur", off);
  });
  // For pages that embed the diagram: light one numbered step, or clear.
  svg.highlightStep = n => {
    const es = new Set(), ns = new Set();
    E.forEach((e, i) => { if (e.step === n) { es.add(i); ns.add(e.f); ns.add(e.t); } });
    tip.setAttribute("visibility", "hidden"); apply(ns, es);
  };
  svg.clearHighlight = off;
})();`;
out.push(`<script><![CDATA[\n${script}\n]]></script>`);
out.push(`</svg>`);
writeFileSync(output, out.join("\n"));
console.log(`wrote ${output} (${W}x${H}, ${byId.size} nodes, ${edges.length} edges)`);
