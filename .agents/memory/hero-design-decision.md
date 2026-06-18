---
name: Hero design decision
description: Which Wandofi hero composition is approved vs. which canvas explorations were rejected.
---

# Approved hero

The **current** live hero is the approved one: centered top nav, the split
display wordmark `WAN ... DOFI` (Fraunces) with the transparent cutout portrait
centered between the two halves, and the bottom meta row (eyebrow + "Vamos falar"
/ "Ver trabalho" buttons left, social column right). Plus the single red **horizon
line** (`.hero__line`) crossing the wordmark centre — see below.

**Why:** the owner reviewed canvas explorations and said "keep design like this"
while pointing at the live site (no red box frame, centered composition); then
later approved the "Linha — luz única literal" red-light treatment.

# Adopted: single red horizon line (graduated from canvas)

The owner explored "light AS the framing device" (questioning RedFrame's literal
box) and picked **Horizon / "Linha — luz única literal"**: one glowing horizontal
red line crossing the hero through the wordmark/subject. It was graduated into the
live site and kept *alongside* the scroll-scrubbed `#spotlight` (not replacing the
brand's single-light motif). The two sibling variants — **Spotlight ("Holofote")**
and **Threshold ("Limiar — portal de luz")** — were NOT chosen.

**Why:** the owner wanted the "single red light" reinterpreted as its most
restrained, literal form. Implementation mechanics live in `replit.md`.

**How to apply:** the line is tuned to cross the wordmark centre at desktop
(~1920); on mobile the stacked layout drops it to a subtle base glow — that is
acceptable, do not chase pixel-perfect cross-breakpoint alignment unless asked.

# Rejected explorations (do NOT re-apply unless asked)

These were canvas-only mockups in `artifacts/mockup-sandbox`, not adopted:

- **Red frame around the portrait** (`wandofi-hero/RedFrame.tsx`).
- **3 usability variants** in `wandofi-usability/`: `Hierarchy.tsx`
  (info hierarchy), `Affordance.tsx` (interaction affordance), `Accessible.tsx`
  (accessibility/readability).

**How to apply:** keep the existing hero markup/styles in `artifacts/wandofi`
as-is. The mockup-sandbox variants remain on the canvas purely as reference.

# Hero portrait is viewport-sensitive — do NOT shrink it to "fix" clipping

The hero portrait is absolutely positioned with a percentage `top` while the
`WAN|DOFI` wordmark is flex-centered, so the two drift apart at different aspect
ratios. The composition is tuned to look right at ~1920x1080 (the size the owner
views it at on the canvas iframe and in their approved print): full head on top,
face in the wordmark gap, crossed arms below.

**Why:** a previous attempt "fixed" perceived forehead-clipping (seen only when
screenshotting at 1280x720) by shrinking the portrait + adding `max-height` — this
cut off the crossed arms and broke the approved print composition; the owner
pushed back. The clipping was a screenshot-size artifact, not a real bug.

**How to apply:** judge the hero at 1920x1080, not at arbitrary widths. Keep the
portrait at `width: clamp(240px, 30vw, 400px)`, `top: 76%`, no `max-height`. If
real cross-viewport robustness is ever needed, re-anchor the portrait to the
wordmark/stage center rather than shrinking it.
