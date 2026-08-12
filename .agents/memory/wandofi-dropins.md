---
name: Wandofi drop-in zips
description: How to apply owner-authored zip drop-ins for the wandofi.pt static site
---

- Drop-in zips from the owner are authoritative content updates for `artifacts/wandofi`, but they are often built from a stale base of `index.html`.
- **Rule:** after applying a zip that includes the home `index.html`, always diff against current first and re-apply intentional fixes the zip silently reverts. Known recurring omission: the `nav__brand` "W." logo link in the nav (`<a class="nav__brand" href="#hero" …>W<span class="nav__brand-dot">.</span></a>`) — the owner confirmed its removal was NOT intentional. Also watch: Zaask footer badge, worklist grid alignment fix, skip-link fix, scroll-to-top fix in main.js.
- **Why:** the owner generates zips from an older snapshot; blind copy loses fixes the user explicitly asked for.
- **How to apply:** unzip to /tmp, diff every file, apply, re-add missing fixes, verify locally, then publish via `pnpm --filter @workspace/scripts run publish-wandofi` and verify live 200s.
