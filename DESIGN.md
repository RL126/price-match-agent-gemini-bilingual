# Price Match Agent UI Design

This project uses a Shopify-inspired commerce dashboard language, adapted for a data-heavy internal tool rather than a marketing site.

## Visual direction

- Canvas: near-black, cinematic, quiet and premium.
- Transactional accent: aloe/mint green signals a safe pricing action or healthy margin.
- Surfaces: dark teal elevated panels with thin hairline borders.
- Controls: pill-shaped primary actions; compact rounded cards for data blocks.
- Density: dashboard content is scan-friendly, with generous spacing between decision bands.

## Tokens

```text
canvas-night: #000000
surface-dark: #0A0A0A
surface-elevated: #1E2C31
accent-aloe: #C1FBD4
accent-pistachio: #D4F9E0
text-primary: #F4FBF7
text-muted: #99B3AD
hairline-dark: rgba(193, 251, 212, 0.16)
radius-card: 12px
radius-hero: 20px
radius-pill: 9999px
spacing-unit: 8px
```

## Component rules

- Use a small eyebrow label above major sections.
- Use four KPI cards for the executive summary.
- Use one highlighted priority-action card to answer “what should I do next?”
- Keep simulation or data-quality caveats visible but visually quiet.
- Use mint only for positive actions, matched states, and healthy margin signals.
- Never let the model invent a number; show calculated values and their data source.

## Typography

- Display: Helvetica Neue / Arial fallback, light weight, tight tracking.
- Body: system sans-serif or Inter when available.
- Technical fields and trace output: system monospace.
