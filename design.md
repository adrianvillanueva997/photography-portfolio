# Design — Adrian Villanueva Photography

Locked design system. Future Hallmark runs read this file first; pages defer
to it. Amend intentionally — the file is the rule.

## System
- Genre · atmospheric
- Macrostructure · Photographic
- Theme · Bloom (atmospheric cluster)
- Axes · light / geometric-sans / warm (65°)

## Tokens (canonical · `src/layouts/Layout.astro` `:root` is the source of truth)
```css
:root {
  --color-paper:      oklch(96%  0.012 75);
  --color-paper-2:    oklch(93%  0.014 75);
  --color-paper-3:    oklch(88%  0.016 75);
  --color-rule:       oklch(82%  0.008 75);
  --color-neutral:    oklch(60%  0.008 65);
  --color-muted:      oklch(42%  0.008 60);
  --color-ink:        oklch(18%  0.008 55);
  --color-ink-2:      oklch(26%  0.010 55);
  --color-accent:     oklch(72%  0.18  65);
  --color-accent-2:   oklch(60%  0.20  58);
  --color-accent-dark: oklch(35%  0.08  30);
  --color-focus:      oklch(65%  0.18  70);
  --color-glow:       oklch(80%  0.08  75 / 0.12);

  --font-display: 'Sora', system-ui, sans-serif;
  --font-body:    'Sora', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;

  /* 8-step spacing scale: --space-xs (0.25rem) … --space-3xl (6rem) */
  /* 8-step type scale 1.25: --text-micro (0.625rem) … --text-display (fluid) */

  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in:     cubic-bezier(0.7,  0, 0.84, 0);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);

  --dur-micro: 120ms;
  --dur-short: 220ms;
  --dur-long:  420ms;
}
```

## Nav
- Archetype · N5 Floating pill
- Fixed, centered, pill-shaped dark chip with backdrop blur
- Active page: accent background, light text
- Mobile: drawer overlay from right

## Footer
- Archetype · Ft5 Statement
- Centered, single-line tagline + mono colophon

## CTA voice
- Primary (nav active) · accent fill · pill (999px) · 0.4rem 0.75rem padding
- Secondary (nav link) · ghost · same radius · muted text on hover

## Motion stance
- Silent background; microinteractions only (color fades, opacity, transform)
- Reduced-motion fallback · ≤150 ms opacity crossfade via `prefers-reduced-motion`
- No motion library — hand-written CSS transitions

## Exports
`src/layouts/Layout.astro` `:root` block is the source of truth (no standalone
`tokens.css`). For Tailwind v4 `@theme`, DTCG `tokens.json`, or shadcn/ui
variables, ask *"extend design.md with <format>"* — Hallmark will append per
`export-formats.md`.
