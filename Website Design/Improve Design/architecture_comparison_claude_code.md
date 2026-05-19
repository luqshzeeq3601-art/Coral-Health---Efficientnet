# Architecture Comparison Section — Claude Code Spec

> **Purpose**: This file provides all data, design decisions, and component specs needed for Claude Code to build or redesign the Architecture Comparison section as a standalone HTML/JS component (not a full dashboard).

---

## Section Goal

Display a scatter chart (Test Accuracy % vs. Parameters in Millions) comparing three CNN architectures, accompanied by a summary table and metric cards. This is a **single section**, not a tabbed dashboard.

---

## Data (Hardcoded — No CSV Needed)

### Model Comparison Table

| Model | Type | Params (M) | Accuracy (%) | Macro F1 | Errors |
|---|---|---|---|---|---|
| EfficientNetB0 Ensemble | 5-seed SWA ensemble | 20.3 | 98.11 | 0.98 | 3 |
| ResNet50 Single | Single robust SWA model | 23.6 | 98.11 | 0.96 | 3 |
| ConvNeXtTiny Single | Single robust SWA model | 27.8 | 97.48 | 0.97 | 4 |

### Class-Specific Performance (EfficientNetB0 Ensemble Only)

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healthy | 0.973 | 1.000 | 0.986 | 72 |
| Bleached | 0.986 | 0.972 | 0.979 | 72 |
| Dead | 1.000 | 0.933 | 0.966 | 15 |
| Macro Avg | 0.986 | 0.969 | 0.977 | 159 |
| Weighted Avg | 0.981 | 0.981 | 0.981 | 159 |

---

## Visual Design Spec

### Color Assignments (per model — fixed, not cycling)

| Model | Hex | Marker Shape |
|---|---|---|
| EfficientNetB0 Ensemble | `#1D9E75` (teal/green) | Circle ● |
| ResNet50 Single | `#378ADD` (blue) | Square ■ |
| ConvNeXtTiny Single | `#D85A30` (coral/orange) | Triangle ▲ |

- EfficientNetB0 is the **proposed/recommended model** — visually emphasize it (larger marker, bolder label, optional highlight ring)
- Do NOT use color alone to distinguish — pair each color with its unique marker shape

### Chart Spec

- **Type**: Scatter plot (X = Parameters in Millions, Y = Test Accuracy %)
- **X axis**: range 18–30, label "Number of parameters (millions)", step 2
- **Y axis**: range 97.0–98.5, label "Test accuracy (%)", ticks formatted as `XX.X%`
- **Grid**: light, subtle (`rgba(0,0,0,0.07)` light / `rgba(255,255,255,0.08)` dark)
- **Tooltip on hover**: show Model name, Parameters, Accuracy, Macro F1, Errors
- **Legend**: custom HTML below/above chart — small colored square + model name, not Chart.js default

### Metric Cards (3 cards, horizontal row above chart)

| Label | Value | Sub-label |
|---|---|---|
| Best accuracy | 98.11% | EfficientNetB0 Ensemble |
| Fewest parameters | 20.3M | EfficientNetB0 Ensemble |
| Best macro F1 | 0.98 | EfficientNetB0 Ensemble |

- Cards use muted background, centered text, 13px label, 22px value, 11px sub-label
- All three highlight EfficientNetB0 as the winner

---

## Layout Structure (Top to Bottom)

```
[ Section heading: "Architecture Comparison" ]
[ 3 metric cards in a row ]
[ Custom legend (colored squares + model names) ]
[ Scatter chart — full width, height ~300px ]
[ Summary table (Model | Type | Params | Accuracy | Macro F1 | Errors) ]
[ Optional: Key findings as 3 short bullet points ]
```

---

## Key Findings Copy (use verbatim in UI)

- EfficientNetB0 Ensemble achieves the highest macro F1 (0.98) with the fewest parameters (20.3M), demonstrating superior parameter efficiency.
- ResNet50 Single matches EfficientNetB0's accuracy (98.11%) but requires 16% more parameters and yields a lower macro F1 (0.96).
- ConvNeXtTiny Single uses the most parameters (27.8M) yet achieves the lowest accuracy (97.48%), indicating diminishing returns at higher model complexity for this dataset.

---

## Implementation Notes for Claude Code

- Use **Chart.js 4.4.1** via CDN: `https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js`
- Render custom marker shapes (circle, square, triangle) via a Chart.js `afterDatasetsDraw` plugin — Chart.js scatter default is circle only
- Disable Chart.js built-in legend (`plugins: { legend: { display: false } }`) and build custom HTML legend instead
- Wrap canvas in a `<div style="position:relative; height:300px">` — never set height on canvas directly
- All colors must work in both light and dark mode — use CSS variables for backgrounds and text, hardcoded hex only for the three model colors
- No `position: fixed` elements — use inline tooltip div repositioned via `mousemove`
- `<canvas>` must have `role="img"` and `aria-label` for accessibility
- Framework: **plain HTML + CSS + vanilla JS** (no React, no build step)

---

## File Context

- Project: Coral Reef Health Assessment via CNN-based Image Analysis
- Student ID: 221022249 — Muhammad Luqman Haziq Bin Mohamad Lofi
- Model pipeline: EfficientNetB0 + 5-seed SWA ensemble + Multi-Scale TTA + Grad-CAM
- Test set: 159 images, 3 classes (Healthy, Bleached, Dead)
- Final test accuracy: 98.11% (3 errors)
