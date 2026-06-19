---
name: Hero design decision
description: Which Wandofi hero composition is approved vs. which canvas explorations were rejected, and why.
---

# Approved hero (current): the "Afordância & interação" / Affordance layout

The live hero is a **left content column + right framed portrait**, graduated from
the canvas mockup `wandofi-usability/Affordance.tsx`. It fully replaced the earlier
centered `WAN | DOFI` split-wordmark + "portal de luz" doorway hero. Implementation
mechanics (markup, classes, breakpoints) live in `replit.md` — read those, not here.

**Why:** the owner reviewed the canvas usability explorations and explicitly chose
the Affordance variant, asking to apply it faithfully to `artifacts/wandofi`.

**How to apply:** judge the hero at ~1920x1080. Unlike the old centered version, the
portrait is now anchored to the section corner (not the wordmark), so it is far less
viewport-sensitive — don't shrink it to "fix" clipping seen only at odd widths.

# Headline reads `WANDOFi`, not "Mauro Cordeiro"

The visible `<h1>` is the brand wordmark `WANDOFi`, matching the rendered mockup and
the owner's reference screenshot — even though the `Affordance.tsx` source string
says "Mauro Cordeiro". An inline visually-hidden span keeps the h1 SEO-descriptive.

**Why:** the rendered design and the owner's screenshot both show the wordmark; the
.tsx source string was stale. Trust the approved visual over the mockup source.

# Superseded / rejected treatments (do NOT re-apply unless asked)

Earlier *live* hero (now removed): centered nav + split `WAN | DOFI` wordmark with a
red **portal/threshold** doorway behind the subject. Also explored and rejected:
**Horizon** (single light line), **Spotlight/Holofote**, the literal **RedFrame**
box, and the sibling usability mockups `Hierarchy.tsx` / `Accessible.tsx`. These
survive only as canvas mockups under `artifacts/mockup-sandbox`.

**Why:** the owner iterated through several red-light framings before settling on the
Affordance layout, and the choice flipped repeatedly — so never assume from history;
check the live hero before changing it.
