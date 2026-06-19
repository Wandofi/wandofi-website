# Wandofi

Dark, single-red-light personal brand site for Mauro Cordeiro (Wandofi) — a project manager operacional in Lisbon offering site migration/creation, technical SEO, automations and business structure. Portuguese (pt-PT), built as a portfolio/landing page at wandofi.pt.

## Run & Operate

- The site runs via the `artifacts/wandofi: web` workflow (Vite dev server on the artifact's `PORT`).
- `pnpm --filter @workspace/wandofi run typecheck` — typecheck the artifact
- `pnpm --filter @workspace/wandofi run build` — production build (needs workflow-provided `PORT`/`BASE_PATH`)

## Stack

- Vanilla HTML + CSS + JS — no framework, no bundled app code. The page is plain static.
- Motion: GSAP + ScrollTrigger + Lenis, all loaded from CDN as `window` globals (the only external runtime deps).
- Fonts: Fraunces (display) + Inter (UI) + Petit Formal Script (section titles `.h2`) via Google Fonts.
- Hosted in a Vite (react-vite scaffold) artifact for the Replit preview, but the deliverable is framework-free and exportable to Cloudflare Pages without a rewrite.

## Where things live

- `artifacts/wandofi/index.html` — all markup + SEO head (canonical, OG/Twitter, JSON-LD Person + ProfessionalService).
- `artifacts/wandofi/public/styles.css` — all styling. The `:root` "TYPE SYSTEM" block is the single source of truth for every font property: families (`--display/--ui/--script`), weights (`--fw-*`), font sizes (fixed `--fs-2xs…--fs-step` + fluid `--fs-lead…--fs-display-sm`), line-heights (`--lh-*`), and tracking (`--track-*`). Every rule references these tokens — never hard-code type values (the only allowed literal is `.stat__unit`'s `0.45em`, which is relative to its parent).
- `artifacts/wandofi/public/main.js` — all motion (vanilla, uses the CDN globals; full `prefers-reduced-motion` fallback).
- `artifacts/wandofi/public/assets/` — `portrait.png` (real photo, background removed → transparent cutout for the hero), `og-portrait.png` (original with background, used only for OG/Twitter social cards), and `wandofi-pm-logo.png` (the original logo, used as-is in the footer).
- `artifacts/wandofi/public/` — `robots.txt`, `sitemap.xml`, `_redirects`, `_headers` (Cloudflare-ready, copied verbatim on build).
- `artifacts/wandofi/src/global.d.ts` — stub only, so `tsc --noEmit` has an input. No app code in `src/`.

## Architecture decisions

- Built framework-free on purpose: the brief requires a Cloudflare-Pages-exportable site with GSAP/ScrollTrigger/Lenis as the only external deps. Everything lives in `public/` so Vite serves it untransformed and copies it verbatim on build.
- The footer "WANDOFI PM" logo is the original raster PNG (`wandofi-pm-logo.png`), used untouched and shown on a white plate (`.signature__plate`) so its dark wordmark stays legible over the near-black footer.
- The single red light is one fixed radial overlay (`#spotlight`, `mix-blend-mode: screen`) whose vertical position is scrubbed by scroll and dimmed near the footer. In the hero it is reinforced by a static `.hero__glow` radial pooled at `75% 50%` (screen-blended) behind the subject.
- Hero composition ("Afordância & interação" exploration — left content · right portrait): floating-pill nav (left `.nav__status` availability pill with pulsing `.status-dot`; right `.nav__links` capsule, **no nav CTA**). `.hero__inner` is a flex row; `.hero__content` (left, `max-width:40rem`) holds `.hero__eyebrow` (red dash via `::before`), the `.hero__headline` (Fraunces, `WANDOFi`), `.hero__lead` (with `<strong>infraestrutura</strong>`), `.hero__actions` (`.btn--red` "Vamos falar" + `.btn--ghost` "Ver trabalho"), and the `.hero__contact` card (inline mail SVG + "Contacto directo" + mailto). The `.hero__portrait` is absolutely anchored bottom-right (`right:0; bottom:0; 45%/660px`) inside a `.hero__portrait-frame` (red `/0.20` border, `border-radius:2rem 2rem 0 0`, rounded-top only). `.hero__social` is absolute bottom-right as icon buttons (inline LinkedIn/GitHub/Instagram SVGs). At ≤1040px the status pill text is hidden; ≤880px hides the nav links pill, stacks `.hero__inner` to a column, and the portrait + socials go static.
- The visible `WANDOFi` headline carries an inline visually-hidden `.hero__seo` span (" — project manager operacional em Lisboa") so the `<h1>` stays SEO-descriptive without altering the brand wordmark.
- Hero entrance (`main.js heroTl`) animates `.hero__headline`, `.hero__portrait`, then the `.hero__eyebrow/.hero__lead/.hero__actions/.hero__contact/.hero__social` group. Hero `.reveal` elements are force-marked `is-in` so a deep-link never lands on hidden content.

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
