# Architecture Comparison Graph Mockup (SVG)

This is a ready-to-embed inline SVG mockup for the Accuracy vs Parameters chart.

## Usage
- Paste the SVG into your HTML where the chart should appear.
- Adjust width/height to fit the container.
- Replace labels/values if your data changes.

## SVG Mockup
```html
<svg viewBox="0 0 900 320" width="100%" height="320" role="img" aria-label="Model Size vs Test Accuracy">
  <defs>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B1121" />
      <stop offset="100%" stop-color="#0F172A" />
    </linearGradient>
    <filter id="cardGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="rgba(45,212,191,0.18)" />
    </filter>
    <filter id="dotGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="rgba(94,234,212,0.6)" />
    </filter>
  </defs>

  <!-- Card -->
  <rect x="0" y="0" width="900" height="320" rx="20" fill="url(#cardGrad)" stroke="rgba(20,184,166,0.35)" filter="url(#cardGlow)" />

  <!-- Title -->
  <text x="28" y="36" fill="#E2E8F0" font-size="18" font-weight="700">Model Size vs Test Accuracy</text>

  <!-- Plot Area -->
  <g transform="translate(60,60)">
    <!-- Gridlines -->
    <g stroke="rgba(148,163,184,0.12)" stroke-width="1">
      <line x1="0" y1="200" x2="780" y2="200" />
      <line x1="0" y1="150" x2="780" y2="150" />
      <line x1="0" y1="100" x2="780" y2="100" />
      <line x1="0" y1="50" x2="780" y2="50" />
      <line x1="0" y1="0" x2="780" y2="0" />
    </g>

    <!-- Axes -->
    <g stroke="rgba(148,163,184,0.35)" stroke-width="1.2">
      <line x1="0" y1="200" x2="780" y2="200" />
      <line x1="0" y1="0" x2="0" y2="200" />
    </g>

    <!-- Axis labels -->
    <text x="390" y="235" fill="#94A3B8" font-size="12" text-anchor="middle">Parameters (M)</text>
    <text x="-36" y="100" fill="#94A3B8" font-size="12" text-anchor="middle" transform="rotate(-90 -36 100)">Test Accuracy (%)</text>

    <!-- Points (scaled manually for mock) -->
    <!-- EfficientNetB0 Ensemble (20.27, 98.11) -->
    <g transform="translate(150,70)">
      <circle r="7" fill="#2DD4BF" filter="url(#dotGlow)" />
      <text x="-4" y="-14" fill="#5EEAD4" font-size="11" font-weight="700">EfficientNetB0</text>
      <text x="-4" y="0" fill="#94A3B8" font-size="10">20.27M · 98.11%</text>
    </g>

    <!-- ResNet50 Single (23.59, 98.11) -->
    <g transform="translate(320,70)">
      <rect x="-6" y="-6" width="12" height="12" fill="#F43F5E" />
      <text x="-4" y="-14" fill="#FDA4AF" font-size="11" font-weight="700">ResNet50</text>
      <text x="-4" y="0" fill="#94A3B8" font-size="10">23.59M · 98.11%</text>
    </g>

    <!-- ConvNeXtTiny Single (27.82, 97.48) -->
    <g transform="translate(610,120)">
      <polygon points="0,-7 7,7 -7,7" fill="#3B82F6" />
      <text x="-4" y="-14" fill="#93C5FD" font-size="11" font-weight="700">ConvNeXtTiny</text>
      <text x="-4" y="0" fill="#94A3B8" font-size="10">27.82M · 97.48%</text>
    </g>
  </g>
</svg>
```

## Color Tokens
- Card background: #0B1121 to #0F172A
- Border: rgba(20,184,166,0.35)
- Title: #E2E8F0
- Axis labels: #94A3B8
- Gridlines: rgba(148,163,184,0.12)
- EfficientNetB0: #2DD4BF
- ResNet50: #F43F5E
- ConvNeXtTiny: #3B82F6

## Notes
- Replace the point coordinates to match real scaling if embedding as data-driven SVG.
- If you switch to Chart.js/ApexCharts, reuse the colors and glow filters as CSS or canvas effects.
