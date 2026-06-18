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
- `artifacts/wandofi/public/styles.css` — all styling, palette and type scale (CSS custom properties at `:root`).
- `artifacts/wandofi/public/main.js` — all motion (vanilla, uses the CDN globals; full `prefers-reduced-motion` fallback).
- `artifacts/wandofi/public/assets/` — `portrait.png` (real photo, background removed → transparent cutout for the hero), `og-portrait.png` (original with background, used only for OG/Twitter social cards), and `wandofi-pm-logo.png` (the original logo, used as-is in the footer).
- `artifacts/wandofi/public/` — `robots.txt`, `sitemap.xml`, `_redirects`, `_headers` (Cloudflare-ready, copied verbatim on build).
- `artifacts/wandofi/src/global.d.ts` — stub only, so `tsc --noEmit` has an input. No app code in `src/`.

## Architecture decisions

- Built framework-free on purpose: the brief requires a Cloudflare-Pages-exportable site with GSAP/ScrollTrigger/Lenis as the only external deps. Everything lives in `public/` so Vite serves it untransformed and copies it verbatim on build.
- The footer "WANDOFI PM" logo is the original raster PNG (`wandofi-pm-logo.png`), used untouched and shown on a white plate (`.signature__plate`) so its dark wordmark stays legible over the near-black footer.
- The single red light is one fixed radial overlay (`#spotlight`, `mix-blend-mode: screen`) whose vertical position is scrubbed by scroll and dimmed near the footer.
- In the hero, that single light is also expressed as architecture: a glowing red **portal/threshold** framing the subject (`.hero__portal`, the graduated "Limiar — portal de luz" exploration). It is positioned with the same anchor as the portrait (`left:50%; top:76%; translate(-50%,-50%)`) and an `aspect-ratio: 372/540` so the frame brackets the figure; child spans render the two side `pillar`s, the top `lintel`, and a blurred `floor` reflection (all `var(--red)` + `--red-glow`, screen-blended where soft). It sits at `z-index:0` so the wordmark (z1) and portrait (z2) stay in front and the figure stands inside the doorway. Hidden at ≤880px (where the portrait goes static, so the absolute anchor no longer applies).
- Hero composition (Dribbble-style): centred nav (left `.nav__status` "Disponível…" dot, links absolutely centred at `left:50%`, CTA right via `margin-left:auto`); the `.display` wordmark is a flex row with `justify-content:space-between` so `WAN` sits far-left and `DOFI` far-right, and the absolutely-centred `.hero__portrait` fills the middle gap (so no text crosses the face). `.hero__meta` holds the eyebrow+actions (left) and social column (right). At ≤1040px the status text is hidden to avoid crowding the centred links; ≤880px stacks the stage/meta and the portrait goes static.
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
