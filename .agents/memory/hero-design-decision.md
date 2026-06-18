---
name: Hero design decision
description: Which Wandofi hero composition is approved vs. which canvas explorations were rejected.
---

# Approved hero

The **current** live hero is the approved one: centered top nav, the split
display wordmark `WAN ... DOFI` (Fraunces) with the transparent cutout portrait
centered between the two halves, and the bottom meta row (eyebrow + "Vamos falar"
/ "Ver trabalho" buttons left, social column right).

**Why:** the owner reviewed canvas explorations and said "keep design like this"
while pointing at the live site (no red frame, centered composition).

# Rejected explorations (do NOT re-apply unless asked)

These were canvas-only mockups in `artifacts/mockup-sandbox`, not adopted:

- **Red frame around the portrait** (`wandofi-hero/RedFrame.tsx`).
- **3 usability variants** in `wandofi-usability/`: `Hierarchy.tsx`
  (info hierarchy), `Affordance.tsx` (interaction affordance), `Accessible.tsx`
  (accessibility/readability).

**How to apply:** keep the existing hero markup/styles in `artifacts/wandofi`
as-is. The mockup-sandbox variants remain on the canvas purely as reference.
