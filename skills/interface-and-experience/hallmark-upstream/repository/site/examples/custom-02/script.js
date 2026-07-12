/* Cascadia Nightjar ticket — drives the single orchestrated print/tear/stamp.
   Progressive enhancement only: the page is fully legible without JS. */
(function () {
  "use strict";

  var root = document.documentElement;

  var reduce = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduce) {
    // Honour reduced motion: show the finished ticket, no animation.
    root.classList.remove("is-ready");
    return;
  }

  // Run the print/tear/stamp sequence once, after first paint.
  // rAF gives the cleanest start; a timeout backstops it in case rAF is
  // throttled (background tab / automation) so the intro never silently stalls.
  var started = false;
  function play() {
    if (started) return;
    started = true;
    root.classList.add("is-ready");

    // Settle to the resting state when the intro ends. The timeout also
    // guarantees the final visible state in environments that freeze the
    // animation clock (background tabs, automation) — the ticket is never
    // left stranded on the hidden first frame.
    var settle = function () { root.classList.add("is-done"); };
    var ticket = document.querySelector(".ticket");
    if (ticket) ticket.addEventListener("animationend", settle, { once: true });
    setTimeout(settle, 1300);
  }

  function schedule() {
    requestAnimationFrame(play);
    setTimeout(play, 60);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", schedule, { once: true });
  } else {
    schedule();
  }
})();
