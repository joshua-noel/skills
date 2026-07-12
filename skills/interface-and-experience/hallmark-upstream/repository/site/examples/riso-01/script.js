/* OFF-REGISTER — riso fair. Progressive enhancement only.
   Three behaviours: page-load reveal stagger · catalogue filter · signup validation.
   Everything works without JS; JS only adds polish. */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.remove("no-js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── One orchestrated reveal on first load ────────────────── */
  // Assign reveal + a DOM-order index so CSS staggers via --i.
  var revealTargets = [
    ".hero__copy", ".hero__art",
    "#catalogue .band", ".filters", ".filters__status",
    "#programme .band", "#workshops .band", "#visit .visit__lede", "#visit .visit__info"
  ];
  if (!reduceMotion) {
    revealTargets.forEach(function (sel, i) {
      var el = document.querySelector(sel);
      if (el) {
        el.classList.add("reveal");
        el.style.setProperty("--i", i % 6); // cap stagger window
      }
    });
    // Cards reveal as a one-shot when the grid enters the viewport.
    var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
    if ("IntersectionObserver" in window && cards.length) {
      var io = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var card = entry.target;
            var idx = cards.indexOf(card);
            card.classList.add("reveal");
            card.style.setProperty("--i", Math.min(idx, 5));
            obs.unobserve(card);
          }
        });
      }, { rootMargin: "0px 0px -8% 0px", threshold: 0.1 });
      cards.forEach(function (c) { io.observe(c); });
    }
  }

  /* ── Catalogue filter ─────────────────────────────────────── */
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));
  var cardEls = Array.prototype.slice.call(document.querySelectorAll(".card"));
  var status = document.querySelector(".filters__status");
  var emptyMsg = status ? status.getAttribute("data-empty") : "";

  function applyFilter(value) {
    var shown = 0;
    cardEls.forEach(function (card) {
      var match = value === "all" || card.getAttribute("data-medium") === value;
      card.classList.toggle("is-hidden", !match);
      if (match) shown += 1;
    });
    if (status) {
      if (shown === 0) {
        status.textContent = emptyMsg;
      } else if (value === "all") {
        status.textContent = "Showing all " + shown + " of these nine featured studios.";
      } else {
        var labelChip = chips.filter(function (c) { return c.getAttribute("data-filter") === value; })[0];
        var label = labelChip ? labelChip.textContent.replace(/\s*\d+\s*$/, "").trim().toLowerCase() : value;
        status.textContent = "Showing " + shown + " featured " + label + (shown === 1 ? " studio." : " studios.");
      }
    }
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) {
        var on = c === chip;
        c.classList.toggle("is-active", on);
        c.setAttribute("aria-pressed", on ? "true" : "false");
      });
      applyFilter(chip.getAttribute("data-filter"));
    });
  });

  /* ── Signup validation (touched pattern · silent success) ─── */
  var form = document.querySelector(".signup");
  if (form) {
    var input = form.querySelector(".signup__input");
    var help = form.querySelector(".signup__help");
    var defaultHelp = help ? help.textContent : "";
    var touched = false;

    function validityMessage() {
      var v = input.value.trim();
      if (!v) return "Add your email address so we know where to send the map.";
      // Simple, forgiving shape check — enough to catch typos, not gatekeep.
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) {
        return "That doesn’t look like an email yet — check for a missing @ or dot.";
      }
      return "";
    }

    function setError(msg) {
      if (msg) {
        input.setAttribute("aria-invalid", "true");
        if (help) { help.textContent = msg; help.setAttribute("data-tone", "error"); }
      } else {
        input.removeAttribute("aria-invalid");
        if (help) { help.textContent = defaultHelp; help.removeAttribute("data-tone"); }
      }
    }

    input.addEventListener("blur", function () { touched = true; setError(validityMessage()); });
    input.addEventListener("input", function () { if (touched) setError(validityMessage()); });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      touched = true;
      var msg = validityMessage();
      setError(msg);
      if (msg) { input.focus(); return; }
      // Silent success: the form becomes a plain confirmation in place — no toast.
      var row = form.querySelector(".signup__row");
      if (row) row.remove();
      if (help) {
        help.textContent = "You’re on the list. Watch for a pink map the week before.";
        help.removeAttribute("data-tone");
      }
    });
  }
})();
