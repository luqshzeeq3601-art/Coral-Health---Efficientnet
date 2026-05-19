# Architecture Comparison Graph Plan

## Goal
Create a futuristic, modern, and easy-to-read scatter plot that compares model size (parameters) vs test accuracy for three models. The chart must be readable at a glance, look premium, and fit the Architecture Comparison tab style.

## Data (example)
- EfficientNetB0 Ensemble: 20.27M params, 98.11% accuracy
- ResNet50 Single: 23.59M params, 98.11% accuracy
- ConvNeXtTiny Single: 27.82M params, 97.48% accuracy

## Visual Direction
- Dark, glassy chart card with subtle neon edges (teal/cyan accent).
- Clean gridlines, low-contrast; labels in bright neutral.
- Data points as glowing glyphs with model-specific color and shape.
- Minimal clutter: direct label callouts or small legends, not both.

## Layout
- Card size: 100% width, 280-340px height.
- Title row: "Model Size vs Test Accuracy" on left, micro legend on right.
- Plot area: 16px padding top/bottom, 20px left/right.

## Axis Design
- X axis: "Parameters (M)" with 18-30 range.
- Y axis: "Test Accuracy (%)" with 97.0-98.4 range.
- Major gridlines only; minor ticks hidden.
- Axis labels in muted gray (#9CA3AF).

## Marks (3 models)
- EfficientNetB0 Ensemble: teal circle, glow.
- ResNet50 Single: rose/red square, glow.
- ConvNeXtTiny Single: blue triangle, glow.

## Labeling
Option A (preferred): short inline callouts near points.
- Use 1-2 line label with model name and accuracy.
- Small connector line with subtle neon stroke.

Option B: small legend chips with colors and shapes.

## Modern Futuristic Styling
- Card background: gradient from #0B1121 to #0F172A.
- Neon edge: 1px border with rgba(20,184,166,0.35).
- Soft ambient glow: box-shadow 0 0 24px rgba(45,212,191,0.18).
- Gridlines: rgba(148,163,184,0.12).
- Axis text: #94A3B8.
- Title text: #E2E8F0.

## Accessibility
- Contrast: text >= 4.5:1 against background.
- Do not rely only on color: use shape + label.

## Interaction (optional)
- Hover tooltip shows exact values.
- Focus ring for keyboard navigation on points.

## Implementation Notes
- Use SVG or canvas chart library (Chart.js / ApexCharts / D3).
- If using HTML/CSS only, render with inline SVG.
- Keep values in data array for easy updates.

## Deliverables
- Chart spec (this doc).
- SVG mock or HTML snippet (optional next step).
