---
name: Wandofi drop-in zips
description: How to apply owner-authored zip drop-ins for the wandofi.pt static site
---

- Drop-in zips from the owner are authoritative content updates for `artifacts/wandofi`, but they are often built from a stale base of `index.html`.
- **Rule:** after applying a zip that includes the home `index.html`, always diff against current first and re-apply intentional fixes the zip silently reverts. Known recurring omission: the `nav__brand` "W." logo link in the nav (`<a class="nav__brand" href="#hero" …>W<span class="nav__brand-dot">.</span></a>`) — the owner confirmed its removal was NOT intentional. Also watch: Zaask footer badge, worklist grid alignment fix, skip-link fix, scroll-to-top fix in main.js.
- **Why:** the owner generates zips from an older snapshot; blind copy loses fixes the user explicitly asked for.
- **How to apply:** unzip to /tmp, diff every file, apply, re-add missing fixes, verify locally, then publish via `pnpm --filter @workspace/scripts run publish-wandofi` and verify live 200s.
- Nested static pages can show the home in the Vite development preview because of its HTML fallback, even when their generated files are correct. **Why:** GitHub Pages serves directory `index.html` files differently from the dev server. **How to apply:** verify nested output in `dist/public`, then run browser tests against `wandofi.pt` after publishing.
- For local screenshots, use the explicit nested filename (e.g. `/seo/index.html`), not just `/seo/`. **Why:** the explicit filename serves the actual static page in Vite, avoiding the homepage fallback.
- The owner explicitly requested the complete light-theme replacement on 2026-09-11. **Why:** the new homepage and interior pages are an intentional redesign, not stale regressions. **How to apply:** do not restore the old dark homepage or W. navigation over that design; keep the legacy shared CSS required by the article pages.
