/* Hollow Coast — the one orchestrated motion.
 * Scroll position == playback position. A drawn waveform (not audio) is the nav:
 *   - the "played" portion (left of the playhead) lights up in phosphor teal
 *   - the playhead travels along the timeline as you scroll
 *   - the nearest marker becomes aria-current; the banner clock shows the timecode
 * Everything is transform/opacity/clip + a single --p custom property; no layout props animate.
 * prefers-reduced-motion: no traveling playhead, no scroll-link — the markers stay
 *   plain anchor links and aria-current is set on click only.
 */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ── Deterministic waveform geometry (stable across loads) ──
     Small seeded PRNG so the "recording" looks the same every time, with a few
     louder transients so it reads like a real envelope, not noise. */
  function makeRNG(seed) {
    var s = seed >>> 0;
    return function () {
      s = (s * 1664525 + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  function envelope(t) {
    // gentle swells + a couple of events, 0..1
    var swell = 0.42 + 0.30 * Math.sin(t * Math.PI * 2.0) * Math.sin(t * Math.PI * 0.6 + 0.4);
    var ev = Math.exp(-Math.pow((t - 0.40) * 14, 2)) * 0.5    // a transient ~07:12 region
           + Math.exp(-Math.pow((t - 0.66) * 9, 2)) * 0.7;    // a build ~weather/rooms
    return Math.min(1, Math.max(0.12, Math.abs(swell) + ev));
  }

  function buildBars(opts) {
    // returns { rectsMarkup, n, totalW }
    var n = opts.bars;
    var vw = opts.vw, vh = opts.vh;
    var gap = opts.gap;
    var slot = vw / n;
    var w = Math.max(1, slot - gap);
    var rng = makeRNG(opts.seed);
    var mid = vh / 2;
    var rects = "";
    for (var i = 0; i < n; i++) {
      var t = i / (n - 1);
      var amp = envelope(t) * (0.62 + 0.5 * rng()); // jitter on the envelope
      amp = Math.min(1, amp);
      var h = Math.max(opts.minH, amp * vh);
      var x = i * slot + (slot - w) / 2;
      var y = mid - h / 2;
      var cls = opts.hotFn && opts.hotFn(t, amp) ? ' class="bar bar--hot"' : ' class="bar"';
      rects += '<rect' + cls + ' x="' + x.toFixed(2) + '" y="' + y.toFixed(2) +
               '" width="' + w.toFixed(2) + '" height="' + h.toFixed(2) +
               '" rx="' + (w / 2).toFixed(2) + '"/>';
    }
    return rects;
  }

  /* ── Timeline waveform (the nav) ── */
  var waveSvg = document.querySelector("[data-bars]");
  var waveEl = document.querySelector("[data-wave]");
  var playedEl = document.querySelector("[data-played]");

  if (waveSvg && waveEl && playedEl) {
    var VW = 1000, VH = 100;
    var bars = buildBars({ bars: 120, vw: VW, vh: VH, gap: 3.4, minH: 4, seed: 0x9e37 });
    waveSvg.innerHTML = bars;

    // Build a mask SVG (same bars) so the "played" gradient only shows through the bars.
    // The mask reads luminance only; we feed it the page's own --ink token (a light,
    // tinted value) so no raw colour literal is introduced.
    var maskFill = getComputedStyle(document.documentElement)
      .getPropertyValue("--ink").trim() || "oklch(93% 0.012 245)";
    var maskSvg =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + VW + ' ' + VH +
      '" preserveAspectRatio="none">' +
      '<g fill="' + maskFill + '">' + bars.replace(/ class="[^"]*"/g, "") + "</g></svg>";
    var mask = 'url("data:image/svg+xml;utf8,' +
      encodeURIComponent(maskSvg).replace(/'/g, "%27").replace(/"/g, "%22") + '")';
    playedEl.style.setProperty("--wave-mask", mask);
  }

  /* ── Per-track mini waveforms (decorative, aria-labelled on the figure) ── */
  var minis = document.querySelectorAll("[data-minwave]");
  minis.forEach(function (svg, idx) {
    var rects = buildBars({
      bars: 80, vw: 600, vh: 60, gap: 2.6, minH: 3, seed: 0x51a3 + idx * 733,
      hotFn: function (t, amp) { return amp > 0.84; }
    });
    svg.innerHTML = rects;
  });

  /* ── Sections + markers wiring ── */
  var markers = Array.prototype.slice.call(document.querySelectorAll("[data-marker]"));
  var sections = markers.map(function (m) {
    var id = m.getAttribute("href").slice(1);
    return document.getElementById(id);
  });

  function setActive(idx) {
    markers.forEach(function (m, i) {
      if (i === idx) m.setAttribute("aria-current", "true");
      else m.removeAttribute("aria-current");
    });
    var m = markers[idx];
    if (m) {
      var t = m.querySelector(".marker__t");
      var n = m.querySelector(".marker__n");
      var clock = document.querySelector("[data-clock]");
      var here = document.querySelector("[data-here]");
      if (clock && t) clock.textContent = t.textContent;
      if (here && n) here.textContent = n.textContent;
    }
  }

  // Click always sets the active marker (works with motion off too).
  markers.forEach(function (m, i) {
    m.addEventListener("click", function () { setActive(i); });
  });

  setActive(0);

  /* ── Reduced motion: stop here. The timeline is now a static set of
        labelled anchor links; clicks still update aria-current + clock. ── */
  if (reduce.matches) return;

  /* ── The orchestrated motion: scroll == playback ──
        Drive --p (0..1) from how far the document is scrolled through the reel.
        playhead = translateX(--p), played fill = clip-path inset on --p.
        rAF-throttled; only transform/clip/opacity touched. */
  var timelineEl = document.getElementById("timeline");
  var root = document.documentElement;
  var ticking = false;

  function progress() {
    var doc = document.documentElement;
    var max = doc.scrollHeight - window.innerHeight;
    if (max <= 0) return 0;
    return Math.min(1, Math.max(0, window.scrollY / max));
  }

  function nearestMarkerIndex() {
    // the section whose top is closest to just under the docked timeline
    var dockPx = (timelineEl ? timelineEl.getBoundingClientRect().bottom : 0) + 8;
    var best = 0, bestDist = Infinity;
    sections.forEach(function (sec, i) {
      if (!sec) return;
      var top = sec.getBoundingClientRect().top;
      var dist = Math.abs(top - dockPx);
      // prefer sections at or above the dock line
      if (top - dockPx <= 24 && dist < bestDist) { bestDist = dist; best = i; }
    });
    return best;
  }

  var lastActive = -1;
  function frame() {
    ticking = false;
    var p = progress();
    if (waveEl) {
      waveEl.style.setProperty("--p", p.toFixed(4));
    }
    var idx = nearestMarkerIndex();
    if (idx !== lastActive) { setActive(idx); lastActive = idx; }
  }

  function onScroll() {
    if (!ticking) { ticking = true; requestAnimationFrame(frame); }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  frame();

  // If the user flips the OS setting mid-session, drop the live parts cleanly.
  if (reduce.addEventListener) {
    reduce.addEventListener("change", function (e) {
      if (e.matches) {
        window.removeEventListener("scroll", onScroll);
        if (waveEl) waveEl.style.removeProperty("--p");
      }
    });
  }
})();
