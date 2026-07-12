/* Hollowback Apiary — progressive enhancement only.
 * Nothing here is required to read the page; it adds the card reveal
 * and the standing-jar form's states. No external requests. */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ── Card reveal: reveal-once on enter, never re-fires (motion.md) ── */
  var cards = document.querySelectorAll(".lot__grid .card");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    cards.forEach(function (c) { c.classList.add("in-view"); });
  } else {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in-view");
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.18, rootMargin: "0px 0px -8% 0px" });
    cards.forEach(function (c) { io.observe(c); });
  }

  /* ── Standing-jar form: idle → loading → success | error ──────────── */
  var form = document.getElementById("standing-form");
  if (!form) return;

  var input = document.getElementById("email");
  var help = document.getElementById("email-help");
  var button = form.querySelector("button[type=submit]");
  var idleText = help ? help.textContent : "";
  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function setHelp(state, message) {
    if (!help) return;
    help.dataset.state = state;
    help.textContent = message;
  }

  // Clearing an error the moment the field is corrected.
  input.addEventListener("input", function () {
    if (input.getAttribute("aria-invalid") === "true" && EMAIL.test(input.value.trim())) {
      input.removeAttribute("aria-invalid");
      setHelp("idle", idleText);
    }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var value = input.value.trim();

    // Error: name what's wrong and how to fix it (copy.md error structure).
    if (!EMAIL.test(value)) {
      input.setAttribute("aria-invalid", "true");
      setHelp("error", "That address is missing an @ or a domain. Try the format you@example.com.");
      input.focus();
      return;
    }

    // Loading: the effect (an email on file) isn't visible, so we narrate it.
    input.removeAttribute("aria-invalid");
    button.disabled = true;
    button.textContent = "Adding…";
    setHelp("idle", "Adding your jar to the season list…");

    // No backend in this demo; simulate the round-trip, then confirm the
    // invisible async result (this is the legitimate toast/confirm case).
    window.setTimeout(function () {
      button.disabled = false;
      button.textContent = "Start a standing jar";
      form.reset();
      setHelp("success", "You're on the list. We'll write the week the next pour ships — no jar bills until then.");
    }, reduceMotion ? 200 : 850);
  });
})();
