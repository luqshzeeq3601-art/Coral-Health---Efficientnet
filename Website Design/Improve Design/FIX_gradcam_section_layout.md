# Fix: Grad-CAM Section — Layout Overflow + Missing Stage 5

**File:** `design9.html` (or whichever HTML file holds the Grad-CAM section)  
**Change type:** CSS fixes + missing HTML block — additive, no other section touched  

---

## Problems Identified

| # | Problem | Root Cause |
|---|---------|-----------|
| 1 | Stage 5 cut off at right edge | Pipeline container has no overflow handling; 5 stages exceed viewport |
| 2 | No horizontal scroll — content just clips | `overflow: hidden` or no `overflow` set on container |
| 3 | EfficientNetB0 icon larger than others | Icon has `w-12 h-12` while others are `w-8 h-8` — inconsistent |
| 4 | Connector arrows uneven length | Arrows use `flex-1` but stages have different widths |
| 5 | Stage 5 result comparison missing | Was not implemented — only 4 stages rendered |
| 6 | Bottom step cards uneven width | Cards not set to `flex-1` equal distribution |

---

## Fix 1 — Pipeline Container: Prevent Clipping

Find the pipeline wrapper div (the one containing all 5 stage columns).  
Replace its overflow and width classes:

```html
<!-- BEFORE: likely has overflow-hidden or nothing -->
<div class="flex items-start gap-6 ... overflow-hidden">

<!-- AFTER: allow scroll on small screens, fit on large -->
<div class="flex items-start gap-4 w-full overflow-x-auto pb-4
            scrollbar-thin scrollbar-thumb-slate-200 scrollbar-track-transparent">
```

Add this to your `<style>` block for cross-browser scrollbar styling:

```css
/* Grad-CAM pipeline scroll */
.gradcam-pipeline {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  width: 100%;
  overflow-x: auto;
  padding-bottom: 1rem;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.gradcam-pipeline::-webkit-scrollbar {
  height: 4px;
}
.gradcam-pipeline::-webkit-scrollbar-track {
  background: transparent;
}
.gradcam-pipeline::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 9999px;
}
```

Apply `gradcam-pipeline` class to the pipeline wrapper div.

---

## Fix 2 — Stage Cards: Equal Min-Width + Scroll Snap

Each stage card (Input, EfficientNetB0, Gradient Flow, Classifier, Result) must have a fixed min-width so they don't compress on smaller screens:

```html
<!-- Add min-w and scroll-snap to EACH stage column div -->
<div class="flex flex-col items-center min-w-[180px] scroll-snap-align-start">
  <!-- stage content -->
</div>
```

```css
/* Add to <style> block */
.gradcam-stage {
  min-width: 180px;
  scroll-snap-align: start;
  flex-shrink: 0;
}
```

Apply `gradcam-stage` to every stage column div.

---

## Fix 3 — Icon Size Consistency

Find all stage icon containers and normalise to the same size.  
The EfficientNetB0 icon is oversized — reduce it to match others:

```html
<!-- BEFORE: EfficientNetB0 icon likely has larger wrapper -->
<div class="w-12 h-12 rounded-xl bg-teal-100 flex items-center justify-center">
  <i data-lucide="layers" class="w-7 h-7 text-teal-600"></i>
</div>

<!-- AFTER: match all stage icons to same size -->
<div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center">
  <i data-lucide="layers" class="w-5 h-5 text-slate-400"></i>
</div>
```

Active stage icon (highlighted when that step is playing) gets teal:

```javascript
// In your existing stage animation JS, apply active class to icon wrapper:
// active:
iconEl.className = 'w-10 h-10 rounded-xl bg-teal-100 flex items-center justify-center';
iconEl.querySelector('i').className = '... text-teal-600';
// inactive:
iconEl.className = 'w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center';
iconEl.querySelector('i').className = '... text-slate-400';
```

---

## Fix 4 — Connector Arrows: Equal Fixed Width

Replace `flex-1` connectors with fixed-width ones so all gaps are equal:

```html
<!-- BEFORE: flex-1 makes uneven gaps -->
<div class="flex-1 flex items-center justify-center">
  <div class="border-t-2 border-dashed border-slate-200 w-full relative">
    <span class="absolute right-0 top-1/2 -translate-y-1/2 text-slate-300">→</span>
  </div>
</div>

<!-- AFTER: fixed width connector -->
<div class="flex items-center justify-center w-12 flex-shrink-0">
  <div class="flex items-center gap-1">
    <div class="w-8 border-t border-dashed border-slate-300"></div>
    <span class="text-slate-300 text-xs">→</span>
  </div>
</div>
```

---

## Fix 5 — Add Missing Stage 5: Result Comparison

This stage was not implemented. Add it as the 5th column in the pipeline, after the Classifier column and its connector arrow.

### HTML — paste after the Stage 4 (Classifier) connector arrow:

```html
<!-- Connector arrow 4→5 -->
<div class="flex items-center justify-center w-12 flex-shrink-0 mt-16">
  <div class="flex items-center gap-1">
    <div class="w-8 border-t border-dashed border-slate-300"></div>
    <span class="text-slate-300 text-xs">→</span>
  </div>
</div>

<!-- Stage 5: Result Comparison -->
<div class="gradcam-stage flex flex-col items-center" id="stage-5">

  <!-- Icon -->
  <div id="icon-stage-5" class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center mb-2">
    <i data-lucide="image-plus" class="w-5 h-5 text-slate-400"></i>
  </div>

  <!-- Label -->
  <p class="text-[10px] font-bold tracking-widest text-slate-400 uppercase mb-0.5">5. Result</p>
  <p class="text-[10px] text-slate-400 mb-3">Heatmap Output</p>

  <!-- Visual: side-by-side comparison card -->
  <div class="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden w-[220px]">

    <!-- Header -->
    <div class="flex border-b border-slate-100">
      <div class="flex-1 text-center py-1.5 text-[9px] font-semibold text-slate-400 uppercase tracking-wide border-r border-slate-100">
        Without
      </div>
      <div class="flex-1 text-center py-1.5 text-[9px] font-semibold text-teal-600 uppercase tracking-wide">
        With Grad-CAM
      </div>
    </div>

    <!-- Images row -->
    <div class="flex">
      <!-- Without Grad-CAM: greyscale coral -->
      <div class="flex-1 relative overflow-hidden" style="height: 100px;">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Coral_reef_at_palmyra.jpg/640px-Coral_reef_at_palmyra.jpg"
          alt="Coral without Grad-CAM"
          class="w-full h-full object-cover"
          style="filter: grayscale(100%) brightness(0.9);">
        <div class="absolute inset-0 bg-slate-500/10"></div>
      </div>

      <!-- Divider -->
      <div class="w-px bg-slate-200 flex-shrink-0"></div>

      <!-- With Grad-CAM: colour + heatmap overlay -->
      <div class="flex-1 relative overflow-hidden" style="height: 100px;">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Coral_reef_at_palmyra.jpg/640px-Coral_reef_at_palmyra.jpg"
          alt="Coral with Grad-CAM"
          class="w-full h-full object-cover">
        <!-- JET colormap heatmap overlay via CSS radial gradients -->
        <div class="absolute inset-0" style="
          background:
            radial-gradient(ellipse 55% 50% at 60% 35%, rgba(220,38,38,0.72) 0%, transparent 60%),
            radial-gradient(ellipse 45% 40% at 45% 50%, rgba(251,146,60,0.55) 0%, transparent 55%),
            radial-gradient(ellipse 60% 55% at 70% 55%, rgba(250,204,21,0.40) 0%, transparent 60%),
            radial-gradient(ellipse 80% 80% at 50% 50%, rgba(59,130,246,0.15) 0%, transparent 80%);
          mix-blend-mode: multiply;">
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="px-2 py-1.5 flex items-center justify-center gap-3 border-t border-slate-100">
      <div class="flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-red-500 flex-shrink-0"></span>
        <span class="text-[8px] text-slate-500">High</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-yellow-400 flex-shrink-0"></span>
        <span class="text-[8px] text-slate-500">Medium</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-blue-400 flex-shrink-0"></span>
        <span class="text-[8px] text-slate-500">Low</span>
      </div>
    </div>

  </div>
</div>
```

---

## Fix 6 — Bottom Step Cards: Equal Width

Find the 4-card row at the bottom. Ensure each card uses `flex-1` and `min-w-0`:

```html
<!-- Card row wrapper -->
<div class="grid grid-cols-4 gap-4 mt-8">
  <!-- each card uses same width automatically via grid -->
</div>
```

If currently using `flex`, replace with `grid grid-cols-4 gap-4`:

```html
<!-- BEFORE -->
<div class="flex gap-4 mt-8">

<!-- AFTER -->
<div class="grid grid-cols-4 gap-4 mt-8">
```

Each card content stays unchanged — only the wrapper changes from `flex` to `grid`.

---

## Fix 7 — Update Stage Animation JS to Include Stage 5

In your existing animation loop, add stage 5 to the stages array:

```javascript
// BEFORE: only 4 stages
const stages = [1, 2, 3, 4];

// AFTER: include stage 5
const stages = [1, 2, 3, 4, 5];
```

Also update the active icon highlight to handle stage 5:

```javascript
function setActiveStage(n) {
  for (let i = 1; i <= 5; i++) {          // was <= 4
    const icon = document.getElementById(`icon-stage-${i}`);
    const card = document.getElementById(`card-step-${i}`);
    const isActive = i === n;

    // icon wrapper
    icon.className = isActive
      ? 'w-10 h-10 rounded-xl bg-teal-100 flex items-center justify-center mb-2'
      : 'w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center mb-2';

    // card (only 4 step cards — skip if i === 5)
    if (card) {
      card.className = isActive
        ? '... border-teal-400 bg-teal-50 ...'   // your existing active card classes
        : '... border-slate-200 bg-white ...';    // your existing inactive card classes
    }
  }
}
```

---

## Testing Checklist

- [ ] All 5 stages visible without horizontal clipping
- [ ] Thin scrollbar appears only when viewport is narrow
- [ ] All 5 stage icons same size; only active one is teal
- [ ] Connector arrows equal length between all stages
- [ ] Stage 5 shows greyscale vs colour+heatmap side by side
- [ ] Heatmap overlay colours visible (red/orange/yellow/blue)
- [ ] Bottom 4 step cards equal width via grid
- [ ] Animation loop cycles through stages 1→5 then restarts
- [ ] No other section in the HTML is affected
