/* Meridian Nine — shared page behaviour.
   Two small things only: the mobile nav toggle, and reveal-on-scroll.
   Both degrade to fully visible, fully usable content without JS. */

(function () {
  'use strict';

  // --- Mobile nav ---------------------------------------------------------
  var burger = document.querySelector('.mn-burger');
  var nav = document.getElementById('mn-nav');

  if (burger && nav) {
    var mq = window.matchMedia('(max-width: 820px)');

    // The nav is only ever hidden at phone widths; a desktop resize must
    // restore it regardless of what the toggle last did.
    var sync = function () {
      if (mq.matches) {
        nav.hidden = true;
        burger.setAttribute('aria-expanded', 'false');
      } else {
        nav.hidden = false;
      }
    };
    sync();
    mq.addEventListener('change', sync);

    burger.addEventListener('click', function () {
      var open = nav.hidden;
      nav.hidden = !open;
      burger.setAttribute('aria-expanded', String(open));
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A' && mq.matches) sync();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mq.matches && !nav.hidden) {
        sync();
        burger.focus();
      }
    });
  }

  // --- Reveal on scroll ---------------------------------------------------
  var targets = document.querySelectorAll('.mn-reveal');
  if (!targets.length) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    // Without motion (or without support) everything is simply present.
    targets.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-in');
      io.unobserve(entry.target);
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.08 });

  targets.forEach(function (el) { io.observe(el); });
})();
