---
name: frontend-design
description: Design and build distinctive, production-grade web interfaces (pages, dashboards, components, landing pages, internal tools) that avoid the generic "AI-made" look. Use when the user asks to build, restyle, or improve any UI in HTML, CSS, React, Vue, Svelte or Tailwind, or says a page looks bland, generic, or template-like.
---

# Frontend Design

Build interfaces that look designed on purpose. Every page gets a clear visual direction before any code is written.

## Step 1: Fix the brief (2 minutes, before code)

Write these five lines at the top of your plan. If any is unknown, pick a sensible value and state it.

1. **Audience and job**: who uses it, and the one thing they must get done.
2. **Tone**: pick ONE direction and commit. Options: editorial, industrial/utilitarian, brutalist, refined luxury, playful, retro-technical, calm clinical, data-dense ops console.
3. **Signature element**: one memorable detail (an oversized numeral, a ticker strip, a custom cursor, a hatched border, a status LED, a grain overlay).
4. **Constraints**: framework, existing design system, accessibility level (default WCAG 2.2 AA), offline or CDN rules, RTL support (Arabic) if relevant.
5. **Density**: marketing (airy) or operational (dense, scannable).

## Step 2: Design tokens first

Define tokens as CSS custom properties before components:

```css
:root {
  --bg: #0f1115; --surface: #171a21; --text: #e8e6e3; --muted: #9aa0a6;
  --accent: #ff5a1f; --ok: #2fbf71; --warn: #f2b134; --crit: #e5484d;
  --radius: 6px; --space: 8px;
  --font-display: "Space Grotesk", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: light) { :root { --bg:#f7f6f3; --surface:#fff; --text:#16181d; --muted:#5b6169; } }
```

Rules:
- One dominant colour plus one sharp accent beats an even rainbow. Status colours are reserved for status.
- Two typefaces maximum. Pair a characterful display face with a neutral body face. Avoid defaulting to Inter-only, Roboto-only or Arial.
- Spacing on a 4 or 8 px scale. No magic numbers.
- Check text contrast: 4.5:1 for body, 3:1 for large text and UI controls.

## Step 3: Layout

- Start from content hierarchy: what must be read first, second, third.
- Use CSS Grid for page structure, Flexbox inside components.
- Break the grid once on purpose (an overlapping image, a full-bleed band, an offset heading). Once.
- Mobile first. Test at 360 px, 768 px, 1280 px. No horizontal scroll at 360 px.
- For dashboards: put the decision-making number top-left, trends next, detail tables last.

## Step 4: Motion and detail

- One orchestrated page-load sequence (staggered reveal with `animation-delay`) is worth more than ten random hovers.
- Respect `prefers-reduced-motion`.
- Texture: subtle noise, gradient mesh, hairline borders, or shadows with a tinted colour, chosen to match the tone.
- Empty, loading, and error states are designed, not left blank.

## Step 5: Self-review checklist (run before handing over)

- [ ] Could this page be swapped with any SaaS template? If yes, the signature element is too weak. Strengthen it.
- [ ] Purple-to-blue gradient on white with rounded cards? Remove it unless the brand demands it.
- [ ] Every interactive element reachable by keyboard, visible focus ring.
- [ ] Images have `alt`. Icons that act as buttons have `aria-label`.
- [ ] `lang` and `dir` set. If Arabic content exists, layout mirrors correctly with logical properties (`margin-inline-start`).
- [ ] Light and dark both checked.
- [ ] No console errors. Lighthouse accessibility 95+ where measurable.

## Anti-patterns to avoid

| Generic default | Do instead |
|---|---|
| Hero with centred H1, subtitle, two buttons | Asymmetric hero, a real data point or product image, one primary action |
| Three identical feature cards with emoji icons | Varied sizes, real numbers, or a comparison table |
| Lorem ipsum | Realistic content for the user's domain |
| Drop shadows everywhere | One elevation level, used for overlays only |
| Random accent colours per section | One accent, used for the primary action and key data |

## Example direction (security ops console)

Tone: industrial ops console. Signature: amber status LEDs and a monospace incident ticker. Tokens: near-black surface, amber accent, red reserved for P1. Layout: KPI strip (open incidents, MTTA, patrol completion %), then a 2-column grid (live incident list left, map or heatmap right). Density: high, 13 px body, tabular numerals for counts.

## Output

Deliver working code, then a 5-line note: tone chosen, signature element, fonts, accessibility checks run, anything not verified.
