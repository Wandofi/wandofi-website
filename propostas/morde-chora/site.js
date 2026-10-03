/* Morde & Chora Burguer · page behaviour.
   The engine runs the kit devices (in, count, reveal, progress). Everything
   bespoke lives here: the layered hero, the scrubbed bite of the peak, the
   Magoga slide, and the signature, a logo that gets eaten as you scroll. */
(function () {
  'use strict';

  ScrollCraft.mount(document.body);

  var reduce = matchMedia('(prefers-reduced-motion: reduce)');
  var finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  var clamp01 = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var smooth = function (a, b, v) { var t = clamp01((v - a) / (b - a)); return t * t * (3 - 2 * t); };

  // ---------------------------------------------------------- bite mark --
  // The mark is the burger-and-flames from the logo. Eight bites, placed
  // around the burger so the flames are what survives.
  var BITES = [
    [438, 300, 62], [52, 330, 58], [330, 238, 58], [418, 452, 60],
    [240, 492, 66], [74, 452, 58], [146, 244, 60], [238, 366, 98]
  ];
  var TOTAL = BITES.length;
  var uid = 0;

  function buildMark(host) {
    var id = 'bm' + (++uid);
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 476 500');
    svg.setAttribute('focusable', 'false');
    var defs = document.createElementNS(ns, 'defs');
    var mask = document.createElementNS(ns, 'mask');
    mask.setAttribute('id', id);
    mask.setAttribute('maskUnits', 'userSpaceOnUse');
    mask.setAttribute('x', '-40'); mask.setAttribute('y', '-40');
    mask.setAttribute('width', '556'); mask.setAttribute('height', '600');
    var bg = document.createElementNS(ns, 'rect');
    bg.setAttribute('x', '-40'); bg.setAttribute('y', '-40');
    bg.setAttribute('width', '556'); bg.setAttribute('height', '600');
    bg.setAttribute('fill', '#fff');
    mask.appendChild(bg);
    var groups = BITES.map(function (b) {
      var g = document.createElementNS(ns, 'g');
      g.setAttribute('class', 'bm-bite');
      var cx = b[0], cy = b[1], r = b[2];
      // the bite faces the burger's centre, so the scallops sit on that side
      var ang = Math.atan2(370 - cy, 240 - cx);
      var main = document.createElementNS(ns, 'circle');
      main.setAttribute('cx', cx); main.setAttribute('cy', cy); main.setAttribute('r', r);
      main.setAttribute('fill', '#000');
      g.appendChild(main);
      [-0.62, -0.21, 0.21, 0.62].forEach(function (d) {
        var c = document.createElementNS(ns, 'circle');
        c.setAttribute('cx', (cx + Math.cos(ang + d) * r).toFixed(1));
        c.setAttribute('cy', (cy + Math.sin(ang + d) * r).toFixed(1));
        c.setAttribute('r', (r * 0.27).toFixed(1));
        c.setAttribute('fill', '#000');
        g.appendChild(c);
      });
      mask.appendChild(g);
      return g;
    });
    defs.appendChild(mask);
    svg.appendChild(defs);
    var img = document.createElementNS(ns, 'image');
    img.setAttribute('href', 'assets/mark-dark.webp');
    img.setAttribute('width', '476'); img.setAttribute('height', '500');
    img.setAttribute('mask', 'url(#' + id + ')');
    svg.appendChild(img);
    host.appendChild(svg);
    return groups;
  }

  var barHost = document.querySelector('.bar [data-bite-mark]');
  var barBites = barHost ? buildMark(barHost) : [];
  var closeHost = document.querySelector('[data-bite-mark="all"]');
  var closeBites = closeHost ? buildMark(closeHost) : [];
  closeBites.forEach(function (g) { g.classList.add('is-on'); });

  var countEl = document.querySelector('[data-bite-count]');
  var wordEl = document.querySelector('[data-bite-word]');
  var biteSections = Array.prototype.slice.call(document.querySelectorAll('[data-bite]'));
  var eaten = 0;

  var regen = document.querySelector('[data-regen]');
  var regrown = false;
  var regrowTimers = [];

  function clearRegrow() {
    regrowTimers.forEach(clearTimeout);
    regrowTimers = [];
  }
  function later(fn, ms) { regrowTimers.push(setTimeout(fn, ms)); }

  // After the last bite the logo grows back, bite by bite, in reverse order,
  // in the close and in the bar at once.
  function regrow() {
    if (regrown) return;
    regrown = true;
    var gap = reduce.matches ? 0 : 140;
    later(function () {
      for (var k = TOTAL - 1; k >= 0; k--) {
        (function (k, d) {
          later(function () {
            [closeBites[k], barBites[k]].forEach(function (g) {
              if (!g) return;
              g.classList.add('is-regrow');
              g.classList.remove('is-on');
            });
          }, d);
        })(k, (TOTAL - 1 - k) * gap);
      }
      later(function () {
        if (regen) regen.classList.add('is-regen');
        [closeHost, barHost].forEach(function (h) {
          if (!h || reduce.matches) return;
          h.classList.remove('crunch', 'pop'); void h.offsetWidth; h.classList.add('pop');
        });
        if (countEl) countEl.textContent = '0';
        if (wordEl) wordEl.textContent = 'dentadas';
      }, TOTAL * gap + 120);
    }, reduce.matches ? 0 : 700);
  }

  // Leaving the close upwards puts the eaten logo back, so the whole story
  // can be told again on the way down.
  function unregrow() {
    if (!regrown) return;
    clearRegrow();
    regrown = false;
    if (regen) regen.classList.remove('is-regen');
    closeBites.forEach(function (g) { g.classList.remove('is-regrow'); g.classList.add('is-on'); });
    barBites.forEach(function (g) { g.classList.remove('is-regrow'); });
    eaten = -1;
  }

  // Bites follow the scroll position both ways: down eats, up un-eats.
  function setBites(n) {
    if (regrown || n === eaten) return;
    var more = n > eaten;
    eaten = n;
    for (var i = 0; i < barBites.length; i++) barBites[i].classList.toggle('is-on', i < n);
    if (countEl) countEl.textContent = n;
    if (wordEl) wordEl.textContent = n === 1 ? 'dentada' : 'dentadas';
    if (more && n > 0 && barHost && !reduce.matches) {
      barHost.classList.remove('crunch');
      void barHost.offsetWidth;
      barHost.classList.add('crunch');
    }
  }

  // ------------------------------------------------- replayable entrances --
  // The engine fires entrances once. Here they reset when their block drops
  // back below the fold, so scrolling up and down again replays them.
  var inEls = Array.prototype.slice.call(document.querySelectorAll('[data-sc-in]'));
  var counters = Array.prototype.slice.call(document.querySelectorAll('[data-count-to]'));
  counters.forEach(function (el) { el.textContent = reduce.matches ? el.getAttribute('data-count-to') : '0'; });

  function setIn(el, on) {
    el.classList.toggle('sc-in', on);
    var stagger = parseFloat(el.getAttribute('data-sc-stagger'));
    Array.prototype.forEach.call(el.children, function (kid, i) {
      if (!isNaN(stagger)) kid.style.transitionDelay = on ? (i * stagger) + 'ms' : '0ms';
      kid.classList.toggle('sc-in', on);
    });
  }

  function runCount(el) {
    var to = parseFloat(el.getAttribute('data-count-to'));
    if (reduce.matches) { el.textContent = to; return; }
    var t0 = performance.now(), dur = 1500, id = (el.__run = (el.__run || 0) + 1);
    (function step(now) {
      if (el.__run !== id) return;
      var k = clamp01((now - t0) / dur);
      el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(step);
    })(t0);
  }

  if ('IntersectionObserver' in window) {
    var replay = new IntersectionObserver(function (entries) {
      if (settled) return;
      entries.forEach(function (e) {
        var el = e.target, below = e.boundingClientRect.top > 0;
        if (el.hasAttribute('data-count-to')) {
          if (e.isIntersecting && !el.__shown) { el.__shown = true; runCount(el); }
          else if (!e.isIntersecting && below) { el.__shown = false; el.__run = (el.__run || 0) + 1; if (!reduce.matches) el.textContent = '0'; }
          return;
        }
        if (e.isIntersecting) setIn(el, true);
        else if (below) setIn(el, false);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.01 });
    inEls.concat(counters).forEach(function (el) { replay.observe(el); });
  }

  // ------------------------------------------------------------- scroll --
  var hero = document.querySelector('[data-hero]');
  var build = document.querySelector('[data-build]');
  var mcImg = document.querySelector('[data-mc-img]');
  var layers = build ? Array.prototype.slice.call(build.querySelectorAll('[data-layer]')) : [];
  var steps = build ? Array.prototype.slice.call(build.querySelectorAll('[data-step]')) : [];
  var slides = Array.prototype.slice.call(document.querySelectorAll('[data-slide]'));
  var root = document.documentElement;

  var mx = 0, my = 0, tx = 0, ty = 0;
  var dirty = true;

  // The story plays once. After the first descent, coming back to the hero
  // locks every section in its final state for the rest of the visit.
  var settled = false, deepest = 0;
  function settle() {
    settled = true;
    clearRegrow();
    root.classList.add('is-settled');
    inEls.forEach(function (el) { setIn(el, true); });
    counters.forEach(function (el) { el.__run = (el.__run || 0) + 1; el.textContent = el.getAttribute('data-count-to'); });
    regrown = true;
    if (regen) regen.classList.add('is-regen');
    closeBites.concat(barBites).forEach(function (g) { g.classList.remove('is-on'); });
    if (countEl) countEl.textContent = '0';
    if (wordEl) wordEl.textContent = 'dentadas';
    if (build) {
      layers.forEach(function (l) { l.style.setProperty('--t', '1'); });
      steps.forEach(function (s) { s.classList.add('is-on'); s.classList.remove('is-current'); });
      build.style.setProperty('--f', '1');
      build.style.setProperty('--name', '1');
      build.setAttribute('data-done', '');
      if (mcImg) mcImg.style.setProperty('--bite', '1');
    }
    slides.forEach(function (s) { s.style.setProperty('--s', '0'); });
  }

  function onScroll() { dirty = true; }

  function update() {
    var vh = innerHeight;

    // hero: one exit value for every plane; CSS gives each its own rate
    if (hero) {
      var h = reduce.matches ? 0 : clamp01(scrollY / vh);
      hero.style.setProperty('--h', h.toFixed(4));
    }

    if (!settled) {
      deepest = Math.max(deepest, scrollY);
      if (deepest > vh * 1.2 && scrollY < vh * 0.35) settle();
    }
    if (settled) return;

    // bites
    var n = 0;
    for (var i = 0; i < biteSections.length; i++) {
      if (biteSections[i].getBoundingClientRect().top < vh * 0.55) {
        n = Math.max(n, parseInt(biteSections[i].getAttribute('data-bite'), 10) || 0);
      }
    }
    var rt = regen ? regen.getBoundingClientRect().top : Infinity;
    if (regrown && rt > vh * 0.85) unregrow();
    setBites(n);
    if (regen && !regrown && eaten >= TOTAL && rt < vh * 0.6) regrow();

    // peak: the hand stacks the burger, then the real one, then the bite
    if (build) {
      var br = build.getBoundingClientRect();
      var bp = clamp01(-br.top / Math.max(1, br.height - vh));
      if (reduce.matches) bp = 1;
      var cur = -1;
      for (var L = 0; L < layers.length; L++) {
        var a = 0.03 + L * 0.062;
        var t = clamp01((bp - a) / 0.07);
        t = 1 - Math.pow(1 - t, 3);       // lands hard, settles soft
        layers[L].style.setProperty('--t', t.toFixed(4));
        if (t > 0.6) cur = L;
      }
      for (var S = 0; S < steps.length; S++) {
        steps[S].classList.toggle('is-on', S <= cur);
        steps[S].classList.toggle('is-current', S === cur && bp < 0.72);
      }
      var f = smooth(0.7, 0.76, bp);
      build.style.setProperty('--f', f.toFixed(4));
      build.style.setProperty('--name', smooth(0.74, 0.8, bp).toFixed(4));
      if (mcImg) mcImg.style.setProperty('--bite', smooth(0.8, 0.9, bp).toFixed(4));
      if (bp > 0.74) build.setAttribute('data-done', ''); else build.removeAttribute('data-done');
    }

    // Magoga travels sideways under a vertical hand
    if (!reduce.matches) {
      slides.forEach(function (s) {
        var sr = s.getBoundingClientRect();
        var p = clamp01((vh - sr.top) / (vh + sr.height));
        s.style.setProperty('--s', ((0.5 - p) * 70).toFixed(2));
      });
    }
  }

  function frame() {
    if (dirty) { dirty = false; update(); }
    // pointer depth in the hero, interpolated so it carries momentum
    if (hero && finePointer.matches && !reduce.matches && scrollY < innerHeight) {
      mx += (tx - mx) * 0.07; my += (ty - my) * 0.07;
      hero.style.setProperty('--mx', mx.toFixed(4));
      hero.style.setProperty('--my', my.toFixed(4));
    }
    requestAnimationFrame(frame);
  }

  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  if (hero) {
    hero.addEventListener('pointermove', function (e) {
      tx = (e.clientX / innerWidth) * 2 - 1;
      ty = (e.clientY / innerHeight) * 2 - 1;
    });
    hero.addEventListener('pointerleave', function () { tx = 0; ty = 0; });
  }
  requestAnimationFrame(frame);
})();
