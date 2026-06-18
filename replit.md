# Wandofi

Dark, single-red-light personal brand site for Mauro Cordeiro (Wandofi) — a project manager operacional in Lisbon offering site migration/creation, technical SEO, automations and business structure. Portuguese (pt-PT), built as a portfolio/landing page at wandofi.pt.

## Run & Operate

- The site runs via the `artifacts/wandofi: web` workflow (Vite dev server on the artifact's `PORT`).
- `pnpm --filter @workspace/wandofi run typecheck` — typecheck the artifact
- `pnpm --filter @workspace/wandofi run build` — production build (needs workflow-provided `PORT`/`BASE_PATH`)

## Stack

- Vanilla HTML + CSS + JS — no framework, no bundled app code. The page is plain static.
- Motion: GSAP + ScrollTrigger + Lenis, all loaded from CDN as `window` globals (the only external runtime deps).
- Fonts: Fraunces (display) + Inter (UI) via Google Fonts.
- Hosted in a Vite (react-vite scaffold) artifact for the Replit preview, but the deliverable is framework-free and exportable to Cloudflare Pages without a rewrite.

## Where things live

- `artifacts/wandofi/index.html` — all markup + SEO head (canonical, OG/Twitter, JSON-LD Person + ProfessionalService).
- `artifacts/wandofi/public/styles.css` — all styling, palette and type scale (CSS custom properties at `:root`).
- `artifacts/wandofi/public/main.js` — all motion (vanilla, uses the CDN globals; full `prefers-reduced-motion` fallback).
- `artifacts/wandofi/public/assets/` — `portrait.png` (real photo) and `wandofi-pm-logo.png` (reference; footer logo is recreated as inline SVG + styled text).
- `artifacts/wandofi/public/` — `robots.txt`, `sitemap.xml`, `_redirects`, `_headers` (Cloudflare-ready, copied verbatim on build).
- `artifacts/wandofi/src/global.d.ts` — stub only, so `tsc --noEmit` has an input. No app code in `src/`.

## Architecture decisions

- Built framework-free on purpose: the brief requires a Cloudflare-Pages-exportable site with GSAP/ScrollTrigger/Lenis as the only external deps. Everything lives in `public/` so Vite serves it untransformed and copies it verbatim on build.
- The footer "WANDOFI PM" logo is rendered as an inline SVG hexagon mark + HTML text (light fill + layered `text-shadow` for 3D depth), not the raster PNG, so colours/shadow are controllable on the dark background.
- The single red light is one fixed radial overlay (`#spotlight`, `mix-blend-mode: screen`) whose vertical position is scrubbed by scroll and dimmed near the footer.
- Key/visible elements (logo wordmark) are never hidden behind animation timing — only enhanced — so a direct deep-link (e.g. `#footer`) never shows a blank logo.

## Product

Single-page site: Hero, Posicionamento, Serviços (6), Trabalho (Lexia + VPA case + worklist), Experiência, Processo, Sobre, CTA/contacto, Footer signature.

## User preferences

- Vanilla stack only (HTML/CSS/JS + GSAP/ScrollTrigger/Lenis via CDN); must stay Cloudflare-Pages-exportable.
- Logo: light text (not black) with a touch of 3D shadowing.

## Gotchas

- Static files belong in `artifacts/wandofi/public/` and are referenced with root-absolute paths (`/styles.css`, `/main.js`, `/assets/...`); `BASE_PATH` is `/`.
- Pending real data to swap in: social URLs (LinkedIn/GitHub/Instagram are placeholders), exact experience dates, and any final portrait the owner prefers.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
