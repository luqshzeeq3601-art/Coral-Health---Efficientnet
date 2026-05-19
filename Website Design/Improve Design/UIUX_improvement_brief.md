# UI/UX Improvement Brief — CoralSight Frontend

**Scope:** Upload panel · Result card · Icons · Animations · Micro-interactions  
**Stack:** Vanilla JS · TailwindCSS CDN · Lucide Icons · Flask  
**Principle:** Every improvement must feel like it belongs in a polished marine science tool — not a generic dashboard.

---

## Current State Audit

| Area | What exists now | Problem |
|------|----------------|---------|
| Model radio cards | Box with text + small badges | Static, no visual weight difference between selected/unselected |
| Grad-CAM toggle | Standard grey switch | Looks disconnected from the action it controls |
| File upload area | Image preview + filename row | No visual feedback during drag; preview feels like an afterthought |
| Prediction header | Green pill badge (99.3%) + large text | Confidence badge is passive — no animation on load |
| Confidence bar | Single static progress bar | No entrance animation; doesn't communicate urgency for low confidence |
| Class probability bars | Three static coloured bars | All render at once — no stagger, no sense of comparison |
| Run Again button | Outlined teal border button | Blends in with the result card; easy to miss |
| Grad-CAM heatmap area | Three image boxes side by side | No label hierarchy; no loading skeleton when Grad-CAM fetches |
| Overall colour | Teal + slate only | Safe but flat; no visual language for health severity |

---

## Section 1 — Icons

### 1.1 Coral health class icons

**Current:** Leaf 🌿 / Bubble 🫧 / Skull 💀 emoji  
**Problem:** Emoji rendering is OS-dependent and looks unpolished in a scientific tool.

**Improvement — use Lucide SVG icons with semantic colour:**

| Class | Lucide icon | Colour token |
|-------|------------|-------------|
| Healthy | `<leaf>` | `text-emerald-600` |
| Bleached | `<thermometer>` | `text-amber-500` |
| Dead | `<skull>` | `text-red-500` |

Replace emoji with inline `<i data-lucide="leaf" class="w-5 h-5">` so rendering is crisp at all DPIs and colour is controlled by CSS.

---

### 1.2 Toggle icon reinforcement

**Current:** Toggle is a bare switch with no icon.  
**Improvement:** Add a small `eye` icon (ON state) and `eye-off` icon (OFF state) from Lucide, swapped by JS alongside the hint text. This makes the toggle's meaning instantly scannable.

```html
<!-- swap these with JS on onGradcamChange() -->
<i id="gradcam-icon-on"  data-lucide="eye"     class="w-4 h-4 text-teal-600"></i>
<i id="gradcam-icon-off" data-lucide="eye-off" class="w-4 h-4 text-slate-400 hidden"></i>
```

---

### 1.3 Model card icons

**Current:** No icon — pure text cards.  
**Improvement:** Add a Lucide icon to each card for instant visual scanning.

| Card | Icon | Rationale |
|------|------|-----------|
| Ensemble | `layers` | Communicates stacking / multiple models |
| Base | `cpu` | Communicates single computation unit |

---

### 1.4 Run Again button icon

**Current:** `refresh-cw` icon (generic).  
**Improvement:** Keep `refresh-cw` but add a `animate-spin` class **only during loading**, then revert. This gives the button a live loading state without a separate spinner element.

```javascript
// on run start:
document.getElementById('run-again-icon').classList.add('animate-spin');
// on run end:
document.getElementById('run-again-icon').classList.remove('animate-spin');
```

---

## Section 2 — Animations

### 2.1 Result card entrance

**Current:** Result card appears instantly — no transition.  
**Improvement:** Fade + slide up on result render. Add to your existing result container:

```css
/* Add once to your <style> block */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
.result-enter {
  animation: slideUp 0.35s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
```

```javascript
// Add inside renderResult(), after making result container visible:
resultContainer.classList.remove('result-enter');
void resultContainer.offsetWidth;   // force reflow to restart animation
resultContainer.classList.add('result-enter');
```

---

### 2.2 Confidence bar fill animation

**Current:** Bar renders at full width instantly.  
**Improvement:** Animate width from 0 to final value on result load.

```css
.confidence-bar-fill {
  width: 0%;
  transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}
```

```javascript
// After setting bar width in renderResult():
requestAnimationFrame(() => {
  document.getElementById('confidence-bar').style.width = result.confidence + '%';
});
```

---

### 2.3 Class probability bars — staggered entrance

**Current:** All three bars appear at the same time.  
**Improvement:** Stagger each bar's animation with a delay so they appear to cascade — reinforcing the comparison between classes.

```css
.prob-bar { width: 0%; transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1); }
```

```javascript
// In your existing probability render loop, add delay per index:
probBars.forEach((bar, i) => {
  setTimeout(() => {
    bar.style.width = probabilities[i] + '%';
  }, i * 120);   // 0ms, 120ms, 240ms stagger
});
```

---

### 2.4 Confidence badge pulse on high confidence

**Current:** Green confidence pill is static.  
**Improvement:** If confidence ≥ 90%, add a one-shot ring pulse on load to draw attention to the strong result. Remove for low confidence so it doesn't feel celebratory when uncertain.

```css
@keyframes ringPulse {
  0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.5); }
  70%  { box-shadow: 0 0 0 10px rgba(16,185,129,0); }
  100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
}
.badge-pulse { animation: ringPulse 0.8s ease-out 0.4s 1 forwards; }
```

```javascript
if (result.confidence >= 90) {
  confidenceBadge.classList.add('badge-pulse');
}
```

---

### 2.5 Toggle switch transition

**Current:** Snap toggle with no easing.  
**Improvement:** The existing Tailwind `peer` toggle already supports `transition-all` — ensure `duration-300` is on the knob and track:

```html
<div class="... transition-all duration-300 ease-in-out peer-checked:bg-teal-500 ..."></div>
```

Also add a subtle `scale` effect on the Grad-CAM section when it appears:

```css
@keyframes expandDown {
  from { opacity: 0; transform: scaleY(0.95); transform-origin: top; }
  to   { opacity: 1; transform: scaleY(1); }
}
.gradcam-enter { animation: expandDown 0.3s ease-out forwards; }
```

---

### 2.6 Loading skeleton for Grad-CAM fetch

**Current:** Grad-CAM section is hidden during fetch — no feedback.  
**Improvement:** Show a shimmer skeleton in place of the three image boxes while the backend computes heatmaps.

```html
<!-- shown during gradcam fetch, hidden otherwise -->
<div id="gradcam-skeleton" class="hidden grid grid-cols-3 gap-3 mt-4">
  <div class="h-36 rounded-xl bg-slate-200 animate-pulse"></div>
  <div class="h-36 rounded-xl bg-slate-200 animate-pulse" style="animation-delay:0.1s"></div>
  <div class="h-36 rounded-xl bg-slate-200 animate-pulse" style="animation-delay:0.2s"></div>
</div>
```

```javascript
// show skeleton before fetch:
document.getElementById('gradcam-skeleton').classList.remove('hidden');
// hide after renderResult():
document.getElementById('gradcam-skeleton').classList.add('hidden');
```

---

## Section 3 — UI/UX Improvements

### 3.1 Severity colour system

**Current:** Result card header is always teal — same colour regardless of health status.  
**Improvement:** Drive the accent colour from the prediction class. This creates immediate visual language — the entire card "feels" the health state.

| Class | Header accent | Confidence badge | Bar colour |
|-------|--------------|-----------------|-----------|
| Healthy | `emerald-500` | `bg-emerald-500` | `bg-emerald-500` |
| Bleached | `amber-500` | `bg-amber-500` | `bg-amber-400` |
| Dead | `red-500` | `bg-red-500` | `bg-red-500` |

```javascript
const SEVERITY_COLORS = {
  Healthy:  { bar: 'bg-emerald-500', badge: 'bg-emerald-500', border: 'border-emerald-400' },
  Bleached: { bar: 'bg-amber-400',   badge: 'bg-amber-500',   border: 'border-amber-400'   },
  Dead:     { bar: 'bg-red-500',     badge: 'bg-red-500',     border: 'border-red-400'     },
};
// Apply in renderResult():
const colors = SEVERITY_COLORS[result.prediction];
resultCard.classList.add(colors.border);   // top border accent
confidenceBadge.className = `... ${colors.badge} ...`;
confidenceBar.className   = `... ${colors.bar} ...`;
```

---

### 3.2 Model card selected state — stronger visual weight

**Current:** Selected card has a coloured border but the unselected card looks nearly identical.  
**Improvement:** Unselected cards use reduced opacity (`opacity-60`) so selected card dominates visually. No layout change needed.

```javascript
function onModelChange() {
  const selected = document.querySelector('input[name="model_type"]:checked').value;
  document.getElementById('label-ensemble').style.opacity = selected === 'ensemble' ? '1' : '0.55';
  document.getElementById('label-base').style.opacity     = selected === 'base'     ? '1' : '0.55';
  // ... existing border class swap unchanged ...
}
```

---

### 3.3 Run Again button — visual prominence

**Current:** Outlined teal border blends into the white card.  
**Improvement:** Make it a **filled teal** button (matching the main submit button) so it reads as a primary action, not a secondary one. Add the spinning icon state from Section 1.4.

```html
<button onclick="runAssessment()" id="btn-run-again"
  class="w-full flex items-center justify-center gap-2 px-4 py-3
         rounded-xl bg-teal-600 hover:bg-teal-700 active:bg-teal-800
         text-white text-sm font-semibold transition-all duration-200 shadow-sm">
  <i id="run-again-icon" data-lucide="refresh-cw" class="w-4 h-4 transition-transform duration-500"></i>
  Run Again
</button>
```

---

### 3.4 Upload area drag-over feedback

**Current:** No visual change when dragging a file over the drop zone.  
**Improvement:** Add a `dragover` highlight state.

```javascript
// Add to existing drag event listeners:
dropZone.addEventListener('dragenter', () => {
  dropZone.classList.add('border-teal-400', 'bg-teal-50', 'scale-[1.01]');
});
dropZone.addEventListener('dragleave', () => {
  dropZone.classList.remove('border-teal-400', 'bg-teal-50', 'scale-[1.01]');
});
```

```css
/* ensure transition on drop zone */
.drop-zone { transition: all 0.2s ease; }
```

---

### 3.5 Uncertainty warning — visual urgency

**Current:** Low-confidence results look the same as high-confidence ones.  
**Improvement:** When `result.uncertainty === true`, add an amber warning banner inside the result card.

```html
<!-- Add inside result card, hidden by default -->
<div id="uncertainty-banner"
  class="hidden flex items-center gap-2 px-3 py-2 rounded-lg
         bg-amber-50 border border-amber-300 text-amber-800 text-xs font-medium mt-3">
  <i data-lucide="triangle-alert" class="w-4 h-4 flex-shrink-0"></i>
  <span>Moderate confidence — manual review recommended.</span>
</div>
```

```javascript
document.getElementById('uncertainty-banner').classList.toggle('hidden', !result.uncertainty);
```

---

### 3.6 Grad-CAM legend — colour coded dots

**Current:** Plain bullet dots with no colour context matching the actual heatmap.  
**Improvement:** Replace text bullets with actual gradient swatches that mirror the JET colormap.

```html
<div class="flex items-center gap-4 mt-3 text-xs text-slate-600">
  <div class="flex items-center gap-1.5">
    <span class="w-16 h-2 rounded-full"
      style="background: linear-gradient(to right, #00f, #0ff, #0f0, #ff0, #f00)"></span>
    <span>Low → High importance</span>
  </div>
</div>
```

---

## Priority Implementation Order

| Priority | Improvement | Effort | Impact |
|----------|-------------|--------|--------|
| 🔴 High | 3.1 Severity colour system | Low | High — immediate UX clarity |
| 🔴 High | 2.2 Confidence bar animation | Low | High — feels alive |
| 🔴 High | 3.3 Run Again filled button | Very low | Medium — discoverability |
| 🟡 Medium | 2.3 Staggered probability bars | Low | Medium — polish |
| 🟡 Medium | 1.1 Replace emoji icons | Low | Medium — professionalism |
| 🟡 Medium | 2.6 Grad-CAM skeleton | Medium | Medium — no blank wait |
| 🟡 Medium | 3.4 Drag-over feedback | Low | Medium — UX delight |
| 🟢 Low | 2.1 Result card entrance | Low | Low — subtle polish |
| 🟢 Low | 2.4 Badge pulse on high confidence | Low | Low — delight |
| 🟢 Low | 3.6 Grad-CAM gradient legend | Very low | Low — accuracy |
| 🟢 Low | 1.2 Toggle eye icon | Very low | Low — clarity |
| 🟢 Low | 3.5 Uncertainty warning banner | Low | Medium — safety |
