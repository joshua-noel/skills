/* Hum · Bubble — N10 floating-on-scroll morph · counter tick-up · stage reveal · star-burst. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── N10 · morph the bar into a floating pill past a threshold (single class toggle) ── */
  var nav = document.getElementById('nav');
  if (nav) {
    var ticking = false;
    function onScroll() {
      var floating = window.scrollY > 24;
      nav.classList.toggle('is-floating', floating);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
    }, { passive: true });
    onScroll();
  }

  /* ── Counter tick-up on view-enter ── */
  var counters = Array.prototype.slice.call(document.querySelectorAll('.count'));
  function runCount(el) {
    var raw = el.dataset.to || el.textContent;
    var to = parseInt(String(raw).replace(/[^0-9]/g, ''), 10) || 0;
    function fmt(n) { return n.toLocaleString('en-US'); }
    if (reduce) { el.textContent = fmt(to); return; }
    var dur = 1200, start = performance.now();
    function tick(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(Math.round(to * eased));
      if (p < 1) { requestAnimationFrame(tick); }
      else {
        el.textContent = fmt(to);
        if (el.animate) { el.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.07)' }, { transform: 'scale(1)' }], { duration: 320, easing: 'ease-out' }); }
      }
    }
    requestAnimationFrame(tick);
  }

  /* ── Stage reveal · sweep in as each enters the viewport ── */
  var stages = Array.prototype.slice.call(document.querySelectorAll('.stage'));

  if ('IntersectionObserver' in window) {
    if (counters.length) {
      var ioCount = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { runCount(e.target); ioCount.unobserve(e.target); } });
      }, { threshold: 0.6 });
      counters.forEach(function (c) { ioCount.observe(c); });
    }
    if (stages.length) {
      var ioStage = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); ioStage.unobserve(e.target); } });
      }, { threshold: 0.25, rootMargin: '0px 0px -10% 0px' });
      stages.forEach(function (s) { ioStage.observe(s); });
    }
  } else {
    counters.forEach(runCount);
    stages.forEach(function (s) { s.classList.add('is-in'); });
  }

  /* ── Star-burst micro-celebration + character reaction on primary actions ── */
  var starter = document.getElementById('starter');
  function burst(x, y) {
    var s = document.createElement('span');
    s.className = 'star-burst';
    s.style.position = 'absolute';
    s.style.left = (x - 12) + 'px';
    s.style.top = (y - 12) + 'px';
    document.body.appendChild(s);
    setTimeout(function () { s.remove(); }, 460);
  }
  document.querySelectorAll('[data-burst]').forEach(function (el) {
    el.addEventListener('click', function (ev) {
      if (el.getAttribute('href') === '#') ev.preventDefault();
      if (reduce) return;
      burst(ev.pageX, ev.pageY);
      if (starter) { starter.classList.remove('is-react'); void starter.offsetWidth; starter.classList.add('is-react'); }
    });
  });
})();
