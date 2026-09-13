# Design — Adrian Villanueva Photography

Locked design system. Future Hallmark runs read this file first; pages defer
to it. Amend intentionally — the file is the rule.

## System
- Genre · atmospheric
- Macrostructure · Photographic
- Theme · System Journal (dark editorial archive)
- Axes · dark / geometric-sans / active green

## Tokens (canonical · `src/layouts/Layout.astro` `:root` is the source of truth)
```css
:root {
  --color-paper:      #08090a;
  --color-paper-2:    #0f1114;
  --color-paper-3:    #171a1e;
  --color-rule:       rgba(255, 255, 255, 0.06);
  --color-neutral:    #555d6b;
  --color-muted:      #9ba3ae;
  --color-ink:        #eaedf0;
  --color-ink-2:      #f7f8f9;
  --color-accent:     #00e68a;
  --color-accent-2:   #9b59b6;
  --color-accent-dark: #00e68a;
  --color-focus:      #00e68a;
  --color-glow:       rgba(0, 230, 138, 0.15);

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
- Archetype · System Journal header
- Fixed, full-width dark header with a centered content rail
- Active page: green system accent and light text
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
