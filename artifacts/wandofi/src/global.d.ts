// Wandofi is a static, dependency-light site: the markup lives in index.html and
// motion lives in /public/main.js (vanilla JS using GSAP, ScrollTrigger and Lenis
// loaded from CDN as window globals). This declaration file exists so the package
// has a TypeScript input for `tsc --noEmit`.

interface Window {
  gsap?: unknown;
  ScrollTrigger?: unknown;
  Lenis?: new (options?: Record<string, unknown>) => unknown;
}

export {};
