/* ============================================================
   WANDOFI — motion
   GSAP + ScrollTrigger + Lenis (loaded via CDN, used as globals)
   ============================================================ */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasGSAP = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";

  /* ---------- Nav: solidify on scroll ---------- */
  var nav = document.getElementById("nav");
  function onScrollNav() {
    if (window.scrollY > 24) nav.classList.add("is-scrolled");
    else nav.classList.remove("is-scrolled");
  }
  onScrollNav();
  window.addEventListener("scroll", onScrollNav, { passive: true });

  /* ---------- Reduced motion: reveal everything, skip the rest ---------- */
  if (reduceMotion || !hasGSAP) {
    document.querySelectorAll(".reveal").forEach(function (el) {
      el.classList.add("is-in");
    });
    document.querySelectorAll(".stat[data-count]").forEach(function (el) {
      el.textContent = (el.getAttribute("data-prefix") || "") +
        el.getAttribute("data-count") + (el.getAttribute("data-suffix") || "");
    });
    return;
  }

  var gsap = window.gsap;
  gsap.registerPlugin(window.ScrollTrigger);

  /* ---------- Lenis smooth scroll, wired into ScrollTrigger ---------- */
  var lenis = null;
  if (typeof window.Lenis !== "undefined") {
    lenis = new window.Lenis({ duration: 1.1, smoothWheel: true });
    lenis.on("scroll", window.ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);

    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var id = a.getAttribute("href");
        if (id.length > 1) {
          var target = document.querySelector(id);
          if (target) { e.preventDefault(); lenis.scrollTo(target, { offset: -10 }); }
        }
      });
    });
  }

  /* ---------- Hero entrance ---------- */
  var heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });
  heroTl
    .from(".display__solid, .display__outline", { yPercent: 115, duration: 1.1, stagger: 0.08 }, 0.1)
    .from(".hero__portrait", { opacity: 0, scale: 1.04, duration: 1.3, ease: "power2.out" }, 0.45)
    .from(".hero__status, .eyebrow, .hero__intro .lead, .hero__actions, .hero__social", {
      opacity: 0, y: 24, duration: 0.8, stagger: 0.08
    }, 0.7);

  // mark hero reveals so they don't double-hide
  document.querySelectorAll(".hero .reveal").forEach(function (el) { el.classList.add("is-in"); });

  /* ---------- Section reveals ---------- */
  gsap.utils.toArray(".reveal:not(.hero .reveal)").forEach(function (el) {
    gsap.to(el, {
      opacity: 1,
      y: 0,
      duration: 0.9,
      ease: "power3.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true },
      onStart: function () { el.classList.add("is-in"); }
    });
  });

  /* ---------- The red light travels with the scroll ---------- */
  var spotlight = document.getElementById("spotlight");
  gsap.to({ v: 12 }, {
    v: 88,
    ease: "none",
    scrollTrigger: {
      trigger: document.body,
      start: "top top",
      end: "bottom bottom",
      scrub: 0.6,
      onUpdate: function (self) {
        spotlight.style.setProperty("--spot-y", (12 + self.progress * 76) + "%");
      }
    }
  });

  // The light dims as we reach the footer, so the signature can glow alone
  window.ScrollTrigger.create({
    trigger: "#footer",
    start: "top 80%",
    end: "top 30%",
    scrub: true,
    onUpdate: function (self) {
      spotlight.style.setProperty("--spot-opacity", String(1 - self.progress * 0.85));
    }
  });

  /* ---------- Counters ---------- */
  document.querySelectorAll(".stat[data-count]").forEach(function (el) {
    var target = parseFloat(el.getAttribute("data-count"));
    var prefix = el.getAttribute("data-prefix") || "";
    var suffix = el.getAttribute("data-suffix") || "";
    var obj = { v: 0 };
    gsap.to(obj, {
      v: target,
      duration: 1.6,
      ease: "power2.out",
      scrollTrigger: { trigger: el, start: "top 88%", once: true },
      onUpdate: function () { el.textContent = prefix + Math.round(obj.v) + suffix; },
      onComplete: function () { el.textContent = prefix + target + suffix; }
    });
  });

  /* ---------- Footer signature: the real logo lifts in as the light fades ---------- */
  // The logo image is preserved exactly as delivered; we only drift it up from a
  // fully-visible start, so even if the trigger never fires the logo is still shown.
  var sigPlate = document.querySelector(".signature__plate");
  if (sigPlate) {
    gsap.from(sigPlate, {
      y: 18, scale: 0.97, duration: 0.9, ease: "power3.out",
      scrollTrigger: { trigger: "#signature", start: "top 92%", once: true }
    });
  }

  window.ScrollTrigger.refresh();
})();
