# Wandofi

Dark, single-red-light personal brand site for Mauro Cordeiro (Wandofi) — a project manager operacional in Lisbon offering site migration/creation, technical SEO, automations and business structure. Portuguese (pt-PT), built as a portfolio/landing page at wandofi.pt.

## Run & Operate

- The site runs via the `artifacts/wandofi: web` workflow (Vite dev server on the artifact's `PORT`).
- `pnpm --filter @workspace/wandofi run typecheck` — typecheck the artifact
- `pnpm --filter @workspace/wandofi run build` — production build (needs workflow-provided `PORT`/`BASE_PATH`)

### Deploy to wandofi.pt (GitHub Pages)

Live site is published to GitHub Pages from the **`gh-pages` branch** of `github.com/Wandofi/wandofi-website` (Pages source = deploy-from-branch `gh-pages` / root, custom domain `wandofi.pt`, HTTPS enforced). It is **not** GitHub Actions: the Replit GitHub connection's OAuth token lacks the `workflow` scope, so `.github/workflows/*` files cannot be pushed.

To publish updated content (`gh-pages` does not auto-update from `main`), run one command:

```
pnpm --filter @workspace/scripts run publish-wandofi
```

The script (`scripts/src/publish-wandofi.ts`) builds the production site, pushes the built output (plus `.nojekyll`) to the `gh-pages` branch root via the GitHub Git Data API using the Replit GitHub connection token (never printed or written to disk), triggers a Pages build, and polls `https://wandofi.pt/` until it returns 200 with the new content. It fails hard if `CNAME` is missing from the build output.

## Stack

- Vanilla HTML + CSS + JS — no framework, no bundled app code. The page is plain static.
- Motion: GSAP + ScrollTrigger + Lenis, all loaded from CDN as `window` globals (the only external runtime deps). Appending `?nomotion` to the URL forces the reduced-motion path (useful for static screenshots/tests).
- Fonts (three, exactly): Instrument Serif (display — headlines, `.h2` italic, case titles, numerals; ships 400+italic only, never ask for other weights) + Instrument Sans (UI/body) + JetBrains Mono (technical labels: eyebrows, tags, nav counts, stat labels, timeline periods) via Google Fonts. Replaced Fraunces+Inter at owner's request 2026-07-17 — note this diverges from the wandofi-brand skill, which still says Fraunces+Inter.
- Hosted in a Vite (react-vite scaffold) artifact for the Replit preview, but the deliverable is framework-free and exportable to Cloudflare Pages without a rewrite.

## Where things live

- `artifacts/wandofi/index.html` — all markup + SEO head (canonical, OG/Twitter, JSON-LD Person + ProfessionalService).
- `artifacts/wandofi/public/styles.css` — all styling. The `:root` "TYPE SYSTEM" block is the single source of truth for every font property: families (`--display/--ui/--script`), weights (`--fw-*`), font sizes (fixed `--fs-2xs…--fs-step` + fluid `--fs-lead…--fs-display-sm`), line-heights (`--lh-*`), and tracking (`--track-*`). Every rule references these tokens — never hard-code type values (the only allowed literal is `.stat__unit`'s `0.45em`, which is relative to its parent).
- `artifacts/wandofi/public/main.js` — all motion (vanilla, uses the CDN globals; full `prefers-reduced-motion` fallback).
- `artifacts/wandofi/public/assets/` — `portrait.webp` (78 KB transparent cutout for the hero), `og-card.jpg` (1200×630 JPEG for OG/Twitter cards), and `wandofi-pm-logo.webp` (41 KB footer logo). The heavy originals (`portrait.png` 2 MB, `og-portrait.png` 1.8 MB, `wandofi-pm-logo.png` 285 KB, old `opengraph.jpg`) live in `attached_assets/originals/` so they don't ship in the build.
- `artifacts/wandofi/public/` — `robots.txt`, `sitemap.xml`, `_redirects`, `_headers` (Cloudflare-ready, copied verbatim on build).
- Favicons: `favicon.ico` (48/32/16), `favicon-96.png`, `apple-touch-icon.png` (180, flattened on `#050505`) — all derived from the hexagon icon in `attached_assets/originals/wandofi-pm-logo.png` (arrow is a transparent cutout, like the footer logo). The old placeholder `favicon.svg` was removed.
- `artifacts/wandofi/src/global.d.ts` — stub only, so `tsc --noEmit` has an input. No app code in `src/`.

## Architecture decisions

- Built framework-free on purpose: the brief requires a Cloudflare-Pages-exportable site with GSAP/ScrollTrigger/Lenis as the only external deps. Everything lives in `public/` so Vite serves it untransformed and copies it verbatim on build.
- The footer "WANDOFI PM" logo is `wandofi-pm-logo-light.webp` — derived from the original transparent PNG by remapping only the wordmark RGB to light (alpha untouched, so letterforms are exact); the icon is unchanged and its arrow is a transparent cutout, reading dark on the dark footer. No plate; `.signature__plate` now just adds drop-shadow + red ambient glow.
- The single red light is one fixed radial overlay (`#spotlight`, `mix-blend-mode: screen`) whose vertical position is scrubbed by scroll and dimmed near the footer. In the hero it is reinforced by a static `.hero__glow` radial pooled at `75% 50%` (screen-blended) behind the subject.
- Home nav now mixes anchors and pages (2026-07-29): Trabalho `#trabalho` · SEO `/seo/` (always visible, incl. mobile) · Tráfego `/gestao-de-trafego/` and Sites `/criacao-de-sites/` (both `.nav__link--extra`, hidden ≤880px) · Contacto `#contacto`. The `[6]` nav counters were removed. Owner's landing-fix drop-in (2026-07-29) later removed the service-card "Ver ↗" links, the `pages.css` include on the home, and the whole Experiência section, and depersonalized the Sobre copy (no personal details on the landing — brand voice is "Wandofi PM", not "Mauro").
- Nav responsive tiers: desktop shows the `.nav__status` pill + full links capsule; ≤1040px swaps the pill for a `.nav__brand` "W." mark; ≤880px the capsule becomes a compact `Menu` disclosure with all six destinations (Trabalho, SEO, Tráfego, Sites, Blog, Contacto) in a two-column panel.
- Hero composition ("Afordância & interação" exploration — left content · right portrait): floating-pill nav (left `.nav__status` availability pill with pulsing `.status-dot`; right `.nav__links` capsule, **no nav CTA**). `.hero__inner` is a flex row; `.hero__content` (left, `max-width:40rem`) holds `.hero__eyebrow` (red dash via `::before`), the `.hero__headline` (Fraunces, `WANDOFi`), `.hero__lead` (with `<strong>infraestrutura</strong>`), `.hero__actions` (`.btn--red` "Vamos falar" + `.btn--ghost` "Ver trabalho"), and the `.hero__contact` card (inline mail SVG + "Contacto directo" + mailto). The `.hero__portrait` is absolutely anchored bottom-right (`right:0; bottom:0; 45%/660px`) inside a `.hero__portrait-frame` (red `/0.20` border, `border-radius:2rem 2rem 0 0`, rounded-top only). `.hero__social` is absolute bottom-right as icon buttons (inline LinkedIn/GitHub/Instagram SVGs). At ≤1040px the status pill text is hidden; ≤880px hides the nav links pill, stacks `.hero__inner` to a column, and the portrait + socials go static.
- The visible `WANDOFi` headline carries an inline visually-hidden `.hero__seo` span (" — project manager operacional em Lisboa") so the `<h1>` stays SEO-descriptive without altering the brand wordmark.
- Hero entrance (`main.js heroTl`) animates `.hero__headline`, `.hero__portrait`, then the `.hero__eyebrow/.hero__lead/.hero__actions/.hero__contact/.hero__social` group. Hero `.reveal` elements are force-marked `is-in` so a deep-link never lands on hidden content.

## Product

Homepage (single-page: Hero, Posicionamento, Serviços (6), Trabalho (Lexia + VPA case + worklist), Processo, Sobre, CTA/contacto, Footer signature) plus 22 static interior pages delivered as an owner-provided drop-in (2026-07-29): `/sobre/`, `/contactos/`, `/blog/`, `/casos/`, `/criacao-de-sites/`, `/automacoes/`, `/gestao-de-trafego/` (+ google-ads, meta-ads) and the `/seo/` cluster (12 pages). Interior pages are plain HTML in `public/<path>/index.html`, styled by `public/pages.css` on top of `styles.css` tokens; `sitemap.xml` covers all pages.

## User preferences

- Vanilla stack only (HTML/CSS/JS + GSAP/ScrollTrigger/Lenis via CDN); must stay Cloudflare-Pages-exportable.
- Logo: light text (not black) with a touch of 3D shadowing.

## Gotchas

- Static files belong in `artifacts/wandofi/public/` and are referenced with root-absolute paths (`/styles.css`, `/main.js`, `/assets/...`); `BASE_PATH` is `/`.
- Pending real data to swap in: social URLs (LinkedIn/GitHub/Instagram are placeholders), exact experience dates, and any final portrait the owner prefers.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details
