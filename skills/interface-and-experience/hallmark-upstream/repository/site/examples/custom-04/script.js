/* The Mend Assembly — custom poster
 * The registration-sweep entrance is pure CSS (one-shot @keyframes that ends in
 * the printed state), so the headline is never JS-dependent for visibility.
 * This file does ONE optional thing: duplicate the tally track so the marquee
 * loops seamlessly. It is a progressive enhancement — with no JS the strip still
 * shows the full list of repairs, just without the wrap.
 */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var track = document.getElementById("tally-track");

  // Only duplicate when the marquee is actually animating (motion welcome).
  if (track && !reduce) {
    track.innerHTML += track.innerHTML;
  }
})();
