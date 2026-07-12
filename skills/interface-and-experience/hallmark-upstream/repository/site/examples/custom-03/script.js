/* Ferns & Fathom — periodic index of blends.
 * The table cells are the single source of truth: each <button class="cell">
 * carries its blend in data-* attributes. Selecting a cell copies those into
 * the assay panel. No duplicated data map, so nothing can drift out of sync.
 *
 * The ONE orchestrated motion: on select, the panel content lifts + settles
 * (.is-swapping for a frame). Honoured-off under prefers-reduced-motion.
 */
(function () {
  "use strict";

  var grid = document.querySelector(".ptable");
  var assay = document.getElementById("assay");
  if (!grid || !assay) return;

  var cells = Array.prototype.slice.call(grid.querySelectorAll(".cell"));

  var out = {
    index: document.getElementById("assay-index"),
    fam: document.getElementById("assay-fam"),
    sym: document.getElementById("assay-sym"),
    name: document.getElementById("assay-name"),
    origin: document.getElementById("assay-origin"),
    caf: document.getElementById("assay-caf"),
    temp: document.getElementById("assay-temp"),
    time: document.getElementById("assay-time"),
    body: document.getElementById("assay-body"),
    notes: document.getElementById("assay-notes")
  };

  var reduceMotion = window.matchMedia
    ? window.matchMedia("(prefers-reduced-motion: reduce)")
    : { matches: false };

  function fill(cell) {
    var d = cell.dataset;
    out.index.textContent = d.num;
    out.fam.textContent = d.famLabel;
    out.sym.textContent = d.sym;
    out.name.textContent = d.name;
    out.origin.textContent = d.origin;
    out.caf.textContent = d.caf;
    out.temp.textContent = d.temp;
    out.time.textContent = d.time;
    out.body.textContent = d.body;
    out.notes.textContent = d.notes;
  }

  var swapTimer = null;
  function select(cell, opts) {
    opts = opts || {};
    if (cell.getAttribute("aria-pressed") === "true" && !opts.force) return;

    cells.forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
    cell.setAttribute("aria-pressed", "true");

    if (reduceMotion.matches || opts.silent) {
      fill(cell);
    } else {
      // one orchestrated moment: content lifts out, swaps, settles back in
      assay.classList.add("is-swapping");
      window.clearTimeout(swapTimer);
      swapTimer = window.setTimeout(function () {
        fill(cell);
        // next frame: release the lift so it eases back to rest
        requestAnimationFrame(function () {
          assay.classList.remove("is-swapping");
        });
      }, 150);
    }
  }

  cells.forEach(function (cell) {
    cell.setAttribute("aria-pressed", "false");
    cell.addEventListener("click", function () { select(cell); });
  });

  // arrow-key roving across the spatial grid for keyboard users.
  // (Tab order already works; arrows make the table feel like a table.)
  grid.addEventListener("keydown", function (e) {
    var current = document.activeElement;
    if (!current || !current.classList || !current.classList.contains("cell")) return;
    var i = cells.indexOf(current);
    if (i === -1) return;

    var col = parseInt(getComputedStyle(current).getPropertyValue("--col"), 10) || 0;
    var next = null;

    if (e.key === "ArrowRight") {
      next = cells[i + 1];
    } else if (e.key === "ArrowLeft") {
      next = cells[i - 1];
    } else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      // move to the nearest cell in the adjacent populated row sharing column
      var dir = e.key === "ArrowDown" ? 1 : -1;
      var pool = cells
        .map(function (c, idx) { return { c: c, idx: idx }; })
        .filter(function (o) { return (dir > 0 ? o.idx > i : o.idx < i); });
      if (dir < 0) pool.reverse();
      var best = null, bestGap = Infinity;
      for (var k = 0; k < pool.length; k++) {
        var ccol = parseInt(getComputedStyle(pool[k].c).getPropertyValue("--col"), 10) || 0;
        var gap = Math.abs(ccol - col);
        if (gap < bestGap) { bestGap = gap; best = pool[k].c; }
        if (gap === 0) break;
      }
      next = best;
    } else {
      return;
    }

    if (next) {
      e.preventDefault();
      next.focus();
    }
  });

  // initialise with element 01 so the panel is never empty
  if (cells.length) select(cells[0], { silent: true, force: true });
})();
