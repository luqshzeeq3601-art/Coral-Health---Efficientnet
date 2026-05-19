# Fix: Typography & Diagram Sizing — Grad-CAM Simulation Section

**Source:** Evaluation feedback on current interface  
**Stack:** Vanilla JS · TailwindCSS CDN · Lucide Icons  
**Change type:** CSS + HTML sizing fixes only — no structural change  

---

## Problem Summary

| # | Area | Problem | Fix |
|---|------|---------|-----|
| 1 | Step card body text | Light grey on white — poor contrast | Darken to `text-slate-600` |
| 2 | Diagram sublabels | Too small, too light | Larger size + medium weight |
| 3 | Neural network layer stack | Too small to read quickly | Scale up visual element |
| 4 | Probability bars (Classifier stage) | Too small to interpret | Wider bars + larger text |
| 5 | Result comparison images | Too small to see heatmap detail | Significantly larger thumbnails |
| 6 | Horizontal gaps between stages | Excessive — wastes space needed for graphics | Reduce gap, redistribute to content |

---

## Fix 1 — Step Card Body Text Contrast

### Problem
Steps 1, 3, and 4 description text uses `text-slate-400` or `text-gray-400` — approximately 3.5:1 contrast ratio against white. WCAG AA minimum is 4.5:1.

### Fix
Find all bottom step card description `<p>` tags. Change text colour:

```html
<!-- BEFORE -->
<p class="text-sm text-slate-400 mt-2">
  High-resolution footage is pre-processed into 224×224 RGB tensors...
</p>

<!-- AFTER -->
<p class="text-sm text-slate-600 mt-2 leading-relaxed">
  High-resolution footage is pre-processed into 224×224 RGB tensors...
</p>
```

Apply `text-slate-600` to **all four** step card descriptions (active and inactive).  
Active card title stays `font-bold text-slate-800` — no change needed there.

For inactive card titles, improve from `text-slate-400` to `text-slate-500`:

```html
<!-- BEFORE -->
<p class="font-semibold text-slate-400">Forward Pass</p>

<!-- AFTER -->
<p class="font-semibold text-slate-500">Forward Pass</p>
```

---

## Fix 2 — Diagram Sublabel Size + Weight

### Problem
Sublabels under workflow icons (e.g. "224×224 RGB", "Feature Mapping", "Last Conv Block", "Logit Computation") are rendered at `text-[10px]` with normal weight — invisible at a glance.

### Fix
Find each stage sublabel `<p>` and update:

```html
<!-- BEFORE -->
<p class="text-[10px] text-slate-400">224×224 RGB</p>

<!-- AFTER -->
<p class="text-xs font-medium text-slate-500 mt-0.5">224×224 RGB</p>
```

Apply consistently to all 5 stage sublabels:

| Stage | Label text | Was | Now |
|-------|-----------|-----|-----|
| 1 Input | "224×224 RGB" | `text-[10px] text-slate-400` | `text-xs font-medium text-slate-500` |
| 2 EfficientNetB0 | "Feature Mapping" | `text-[10px] text-slate-400` | `text-xs font-medium text-slate-500` |
| 3 Gradient Flow | "Last Conv Block" | `text-[10px] text-slate-400` | `text-xs font-medium text-slate-500` |
| 4 Classifier | "Logit Computation" | `text-[10px] text-slate-400` | `text-xs font-medium text-slate-500` |
| 5 Result | "Heatmap Output" | `text-[10px] text-slate-400` | `text-xs font-medium text-slate-500` |

Stage number labels (e.g. "1. INPUT") — increase tracking and weight:

```html
<!-- BEFORE -->
<p class="text-[10px] font-bold tracking-widest text-slate-400 uppercase">1. INPUT</p>

<!-- AFTER -->
<p class="text-xs font-bold tracking-widest text-slate-500 uppercase mb-1">1. INPUT</p>
```

---

## Fix 3 — Neural Network Layer Stack (Stage 2) Scale Up

### Problem
The EfficientNetB0 isometric layer stack is rendered too small — layers are thin and indistinguishable from each other.

### Fix
Find the stage 2 visual container and increase dimensions:

```html
<!-- BEFORE: small container -->
<div class="w-28 h-28 flex items-center justify-center">
  <!-- stacked layer divs -->
</div>

<!-- AFTER: larger container -->
<div class="w-40 h-36 flex items-center justify-center">
  <!-- stacked layer divs -->
</div>
```

For each individual layer rectangle inside the stack, increase height and gap:

```html
<!-- BEFORE: thin layers -->
<div class="w-24 h-3 rounded bg-teal-200 border border-teal-300 shadow-sm"></div>

<!-- AFTER: taller, more readable layers -->
<div class="w-32 h-5 rounded-md bg-teal-200 border border-teal-300 shadow-sm mb-1.5"></div>
```

If layers use absolute positioning for isometric effect, increase the vertical offset between each layer from `top-[Npx]` to `top-[N+4px]` to add breathing room.

---

## Fix 4 — Probability Bars (Stage 4 Classifier) Scale Up

### Problem
The three class probability bars (Healthy / Bleached / Dead) are narrow and the percentage labels are too small to read at a glance.

### Fix
Find the classifier card inside stage 4 and update:

```html
<!-- BEFORE: cramped bars -->
<div class="w-[140px] text-xs">
  <div class="flex justify-between mb-1">
    <span class="text-slate-600">Healthy</span>
    <span class="font-bold text-emerald-600">99.3%</span>
  </div>
  <div class="w-full bg-slate-100 rounded-full h-1.5 mb-2">
    <div class="bg-emerald-500 h-1.5 rounded-full" style="width:99.3%"></div>
  </div>
</div>

<!-- AFTER: larger, more readable bars -->
<div class="w-[180px]">
  <div class="flex justify-between items-center mb-1">
    <span class="text-xs font-medium text-slate-700">Healthy</span>
    <span class="text-sm font-bold text-emerald-600">99.3%</span>
  </div>
  <div class="w-full bg-slate-100 rounded-full h-2.5 mb-2.5">
    <div class="bg-emerald-500 h-2.5 rounded-full transition-all duration-700"
         style="width:99.3%"></div>
  </div>

  <div class="flex justify-between items-center mb-1">
    <span class="text-xs font-medium text-slate-700">Bleached</span>
    <span class="text-sm font-bold text-amber-500">0.3%</span>
  </div>
  <div class="w-full bg-slate-100 rounded-full h-2.5 mb-2.5">
    <div class="bg-amber-400 h-2.5 rounded-full" style="width:0.3%"></div>
  </div>

  <div class="flex justify-between items-center mb-1">
    <span class="text-xs font-medium text-slate-700">Dead</span>
    <span class="text-sm font-bold text-red-500">0.4%</span>
  </div>
  <div class="w-full bg-slate-100 rounded-full h-2.5">
    <div class="bg-red-500 h-2.5 rounded-full" style="width:0.4%"></div>
  </div>
</div>
```

Key changes: `w-[140px]` → `w-[180px]`, bar height `h-1.5` → `h-2.5`, label `text-xs` → `text-sm font-bold` for percentages.

---

## Fix 5 — Result Comparison Images (Stage 5) Scale Up

### Problem
Without/With Grad-CAM thumbnails are too small (approximately 100px tall) to see the thermal heatmap overlay detail.

### Fix
Find the result comparison image containers in stage 5 and increase height significantly:

```html
<!-- BEFORE: too small -->
<div class="flex-1 relative overflow-hidden" style="height: 100px;">
  <img ... class="w-full h-full object-cover">
</div>

<!-- AFTER: large enough to see heatmap detail -->
<div class="flex-1 relative overflow-hidden" style="height: 160px; min-width: 120px;">
  <img ... class="w-full h-full object-cover object-center">
</div>
```

Also increase the overall Stage 5 card width to accommodate larger images:

```html
<!-- BEFORE -->
<div class="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden w-[220px]">

<!-- AFTER -->
<div class="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden w-[280px]">
```

Increase the heatmap overlay radial gradient coverage to match the larger image:

```html
<!-- AFTER (larger overlay coverage on bigger image) -->
<div class="absolute inset-0" style="
  background:
    radial-gradient(ellipse 60% 55% at 58% 32%, rgba(220,38,38,0.78) 0%, transparent 55%),
    radial-gradient(ellipse 50% 45% at 42% 52%, rgba(251,146,60,0.60) 0%, transparent 55%),
    radial-gradient(ellipse 65% 60% at 68% 58%, rgba(250,204,21,0.45) 0%, transparent 60%),
    radial-gradient(ellipse 90% 85% at 50% 50%, rgba(59,130,246,0.18) 0%, transparent 80%);
  mix-blend-mode: multiply;">
</div>
```

---

## Fix 6 — Reduce Horizontal Gap Between Stages

### Problem
Connector arrows + stage spacing creates excessive whitespace, leaving no room to scale up visual elements.

### Fix — Pipeline container gap

```html
<!-- BEFORE -->
<div class="gradcam-pipeline flex items-start gap-4 ...">

<!-- AFTER: tighter gap between stages -->
<div class="gradcam-pipeline flex items-start gap-2 ...">
```

### Fix — Connector arrow width

```html
<!-- BEFORE: wide connector -->
<div class="flex items-center justify-center w-12 flex-shrink-0 mt-16">
  <div class="w-8 border-t border-dashed border-slate-300"></div>
  <span class="text-slate-300 text-xs">→</span>
</div>

<!-- AFTER: compact connector -->
<div class="flex items-center justify-center w-8 flex-shrink-0 mt-16">
  <div class="w-5 border-t border-dashed border-slate-300"></div>
  <span class="text-slate-300 text-[10px]">→</span>
</div>
```

### Fix — Stage min-width

Reduce each stage's min-width slightly to allow visual elements to be larger without causing overflow:

```css
/* BEFORE */
.gradcam-stage { min-width: 180px; }

/* AFTER */
.gradcam-stage { min-width: 160px; }
```

The space saved from smaller gaps and connectors goes directly into larger stage visuals.

---

## Summary of All Size Changes

| Element | Before | After |
|---------|--------|-------|
| Step card body text | `text-slate-400` | `text-slate-600` |
| Inactive card title | `text-slate-400` | `text-slate-500` |
| Stage sublabels | `text-[10px]` normal | `text-xs` medium |
| Stage number labels | `text-[10px]` | `text-xs` bold |
| Layer stack container | `w-28 h-28` | `w-40 h-36` |
| Individual layer height | `h-3` | `h-5` |
| Classifier card width | `w-[140px]` | `w-[180px]` |
| Probability bar height | `h-1.5` | `h-2.5` |
| Probability % label | `text-xs` | `text-sm font-bold` |
| Result image height | `100px` | `160px` |
| Result card width | `w-[220px]` | `w-[280px]` |
| Pipeline gap | `gap-4` | `gap-2` |
| Connector width | `w-12` / `w-8` line | `w-8` / `w-5` line |
| Stage min-width | `180px` | `160px` |

---

## Testing Checklist

- [ ] Step card body text passes WCAG AA contrast (≥4.5:1) against white background
- [ ] Stage sublabels readable without zooming in
- [ ] Neural network layer stack clearly shows 4–5 distinct layers
- [ ] Probability bar percentages legible at normal viewing distance
- [ ] Heatmap comparison images show clear colour difference at a glance
- [ ] Pipeline still fits within viewport width without extra scrolling
- [ ] No other section outside the Grad-CAM simulation block is affected
