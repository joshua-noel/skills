/* gen-13 · Bríd Halloran — Press Quaternary
 * Three small, purposeful behaviours:
 *   1. the live variable-font specimen (range axes drive font-variation-settings)
 *   2. a scroll-spy that marks the current section dot in the side-rail
 *   3. an optimistic enquire form with the full set of states
 * All motion respects prefers-reduced-motion.
 */
(function () {
  "use strict";

  /* ── 1 · Living variable specimen ───────────────────────── */
  var word = document.getElementById("liveWord");
  var fig = document.querySelector(".specimen-live");
  var axes = [
    { input: document.getElementById("axWght"), out: document.getElementById("wghtVal"), prop: "--w" },
    { input: document.getElementById("axWdth"), out: document.getElementById("wdthVal"), prop: "--wd" },
    { input: document.getElementById("axOpsz"), out: document.getElementById("opszVal"), prop: "--op" }
  ];

  function applyAxes() {
    if (!word) return;
    var w = axes[0].input ? axes[0].input.value : 320;
    var wd = axes[1].input ? axes[1].input.value : 100;
    var op = axes[2].input ? axes[2].input.value : 96;
    // write the variation directly so it overrides the breathing keyframes
    word.style.fontVariationSettings =
      "'wght' " + w + ", 'wdth' " + wd + ", 'opsz' " + op;
    axes.forEach(function (a) {
      if (a.out && a.input) a.out.textContent = a.input.value;
    });
  }

  axes.forEach(function (a) {
    if (!a.input) return;
    a.input.addEventListener("input", function () {
      if (fig) fig.dataset.grabbed = "true"; // stop the ambient breathe loop
      applyAxes();
    });
  });
  // initialise the value read-outs (breathing loop owns the glyph until first grab)
  axes.forEach(function (a) { if (a.out && a.input) a.out.textContent = a.input.value; });

  /* ── 2 · Scroll-spy for the rail dots ───────────────────── */
  var dotLinks = Array.prototype.slice.call(
    document.querySelectorAll(".rail__dots a")
  );
  var sections = dotLinks
    .map(function (a) {
      var id = a.getAttribute("href").slice(1);
      return { link: a, el: document.getElementById(id) };
    })
    .filter(function (s) { return s.el; });

  if ("IntersectionObserver" in window && sections.length) {
    var spy = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var match = sections.find(function (s) { return s.el === entry.target; });
          if (!match) return;
          dotLinks.forEach(function (l) {
            var on = l === match.link;
            l.classList.toggle("is-current", on);
            if (on) { l.setAttribute("aria-current", "true"); }
            else { l.removeAttribute("aria-current"); }
          });
        });
      },
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach(function (s) { spy.observe(s.el); });
  }

  /* ── 3 · Enquire form — optimistic, all states ──────────── */
  var form = document.getElementById("enquire");
  if (form) {
    var input = document.getElementById("enq-email");
    var help = document.getElementById("enq-help");
    var btn = form.querySelector(".enquire__btn");
    var label = btn ? btn.querySelector(".btn__label") : null;
    var defaultHelp = help ? help.textContent : "";
    var touched = false;

    function setHelp(text, tone) {
      if (!help) return;
      help.textContent = text;
      if (tone) help.setAttribute("data-tone", tone);
      else help.removeAttribute("data-tone");
    }

    function validEmail(v) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim());
    }

    function validate() {
      if (!input) return false;
      var ok = validEmail(input.value);
      input.setAttribute("aria-invalid", ok ? "false" : "true");
      return ok;
    }

    if (input) {
      input.addEventListener("blur", function () {
        touched = true;
        if (input.value && !validate()) {
          setHelp("That address is missing an @ or a domain. Check it and try again.", "error");
        } else {
          setHelp(defaultHelp, null);
        }
      });
      input.addEventListener("input", function () {
        if (!touched) return;
        if (validate()) setHelp(defaultHelp, null);
      });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      touched = true;
      if (!validate()) {
        setHelp("That address is missing an @ or a domain. Check it and try again.", "error");
        if (input) input.focus({ preventScroll: true });
        return;
      }

      // optimistic: show loading, then resolve to a quiet success (no toast)
      if (btn) { btn.dataset.state = "loading"; btn.disabled = true; }
      if (label) label.textContent = "Sending…";
      setHelp("Sending your note…", null);

      window.setTimeout(function () {
        if (btn) { btn.dataset.state = "success"; btn.disabled = false; }
        if (label) label.textContent = "Note sent ✓";
        if (input) { input.value = ""; input.setAttribute("aria-invalid", "false"); }
        setHelp("Thanks — your note is on its way. I’ll reply from studio@pressquaternary within a few days.", "success");
      }, 900);
    });
  }
})();
