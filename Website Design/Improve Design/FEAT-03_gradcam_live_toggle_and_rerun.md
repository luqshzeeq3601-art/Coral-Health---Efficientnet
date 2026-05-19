# Feature: Grad-CAM Live Toggle + Re-run Assessment Button

**Feature ID:** FEAT-03  
**Stack:** Flask (Python) · Vanilla JS · TailwindCSS CDN · Lucide Icons  
**Change type:** Frontend-only for toggle behaviour · Additive only  

---

## Problems Being Solved

| # | Problem | Solution |
|---|---------|----------|
| 1 | Grad-CAM only shows after run — toggle has no live effect | Toggle immediately shows/hides heatmap; flipping ON after a no-Grad-CAM run auto re-runs to fetch it |
| 2 | Must delete image and re-upload to run again | "Run Again" button re-submits same in-memory image with current settings |

---

## Improvement 1 — Grad-CAM Live Toggle

### Behaviour by situation

| Situation | Toggle flipped ON | Toggle flipped OFF |
|-----------|------------------|--------------------|
| No result yet | Placeholder shown | Placeholder hidden, disabled msg shown |
| Result exists, Grad-CAM was ON | Heatmap renders **instantly** (no re-run) | Heatmap hides instantly |
| Result exists, Grad-CAM was OFF | **Auto re-runs** assessment with `gradcam_enabled=true` | Disabled msg shown |

### Key principle

Two JS variables track state between runs:

| Variable | Type | Holds |
|----------|------|-------|
| `lastGradcam` | `object \| null` | Last `{heatmap, overlay}` from backend |
| `lastOriginal` | `string \| null` | Last `original_image` base64 — also signals a result exists |

---

### Backend — No Changes Required

`/api/predict` already reads `gradcam_enabled` from `request.form`. Re-running with toggle ON sends `gradcam_enabled=true` automatically.

---

### Frontend — HTML Changes

#### 1. Ensure IDs exist on Grad-CAM section elements

Add `id` attributes to your existing Grad-CAM elements if not already present — **do not change class or structure**:

```html
<!-- existing Grad-CAM wrapper — add id only -->
<div id="gradcam-section" class="... your existing classes ...">
  <figure id="gradcam-fig-original"> ... </figure>
  <figure id="gradcam-fig-overlay">  ... </figure>
  <figure id="gradcam-fig-heatmap">  ... </figure>
</div>

<!-- NEW: placeholder — shown when toggle ON but no result yet -->
<div id="gradcam-placeholder"
  class="hidden mt-4 p-4 rounded-xl border-2 border-dashed border-slate-200 text-center text-sm text-slate-400">
  <i data-lucide="eye" class="inline w-4 h-4 mr-1"></i>
  Grad-CAM will appear here after running the assessment.
</div>

<!-- NEW: disabled message — shown when toggle OFF -->
<p id="gradcam-disabled-msg"
  class="hidden text-center text-sm text-slate-400 py-4">
  Grad-CAM is disabled. Enable it above to visualize attention regions.
</p>

<!-- NEW: auto re-run notice — shown briefly while re-running for Grad-CAM -->
<p id="gradcam-rerun-msg"
  class="hidden text-center text-sm text-teal-600 py-2 animate-pulse">
  <i data-lucide="loader" class="inline w-3 h-3 mr-1"></i>
  Fetching Grad-CAM — re-running assessment...
</p>
```

---

### Frontend — JavaScript Changes

#### 2. Add state variables at the top of your existing JS scope

```javascript
// ── FEAT-03: state variables ──
let lastGradcam  = null;   // {heatmap, overlay} from last run, or null
let lastOriginal = null;   // original_image base64 — also signals a result exists
// ─────────────────────────────
```

---

#### 3. `onGradcamChange()` — full version with auto re-run fix

> Replace any earlier version of this function entirely.

```javascript
// ── FEAT-03: Grad-CAM live toggle ────────────────────────────────
function onGradcamChange(enabled) {
  // swap hint text
  document.getElementById('gradcam-hint-on').classList.toggle('hidden', !enabled);
  document.getElementById('gradcam-hint-off').classList.toggle('hidden', enabled);

  const section     = document.getElementById('gradcam-section');
  const placeholder = document.getElementById('gradcam-placeholder');
  const disabledMsg = document.getElementById('gradcam-disabled-msg');
  const rerunMsg    = document.getElementById('gradcam-rerun-msg');

  // ── Toggle OFF ────────────────────────────────────────────────
  if (!enabled) {
    section.classList.add('hidden');
    placeholder.classList.add('hidden');
    rerunMsg.classList.add('hidden');
    disabledMsg.classList.remove('hidden');
    return;
  }

  // ── Toggle ON ─────────────────────────────────────────────────
  disabledMsg.classList.add('hidden');

  if (lastGradcam && lastGradcam.heatmap && lastGradcam.overlay) {
    // Case 1: Grad-CAM result already stored — show instantly, no re-run
    renderGradcam(lastGradcam, lastOriginal);
    section.classList.remove('hidden');
    placeholder.classList.add('hidden');
    rerunMsg.classList.add('hidden');

  } else if (lastOriginal) {
    // Case 2: A result exists but Grad-CAM was OFF during that run
    // → auto re-run with gradcam_enabled=true to fetch the heatmap
    rerunMsg.classList.remove('hidden');
    placeholder.classList.add('hidden');
    section.classList.add('hidden');
    runAssessment();   // toggle is now ON → formData will send gradcam_enabled=true

  } else {
    // Case 3: No result yet — show placeholder
    section.classList.add('hidden');
    rerunMsg.classList.add('hidden');
    placeholder.classList.remove('hidden');
  }
}
// ── end FEAT-03 toggle ───────────────────────────────────────────
```

---

#### 4. `renderGradcam()` helper

```javascript
// ── FEAT-03: Grad-CAM render helper ─────────────────────────────
function renderGradcam(gradcam, original) {
  document.getElementById('img-original').src = 'data:image/png;base64,' + original;
  document.getElementById('img-overlay').src  = 'data:image/png;base64,' + gradcam.overlay;
  document.getElementById('img-heatmap').src  = 'data:image/png;base64,' + gradcam.heatmap;
}
// ─────────────────────────────────────────────────────────────────
```

---

#### 5. Update existing `renderResult()` to store state and delegate

```javascript
function renderResult(result) {
  // ... all existing rendering unchanged ...

  // ── FEAT-03: store state ──
  lastGradcam  = result.gradcam        ?? null;
  lastOriginal = result.original_image ?? null;
  // ──────────────────────────

  const section     = document.getElementById('gradcam-section');
  const placeholder = document.getElementById('gradcam-placeholder');
  const disabledMsg = document.getElementById('gradcam-disabled-msg');
  const rerunMsg    = document.getElementById('gradcam-rerun-msg');
  const toggleOn    = document.getElementById('gradcam-toggle').checked;

  // always hide re-run notice once result arrives
  rerunMsg.classList.add('hidden');

  if (!toggleOn) {
    section.classList.add('hidden');
    placeholder.classList.add('hidden');
    disabledMsg.classList.remove('hidden');

  } else if (lastGradcam && !lastGradcam.error) {
    renderGradcam(lastGradcam, lastOriginal);
    section.classList.remove('hidden');
    placeholder.classList.add('hidden');
    disabledMsg.classList.add('hidden');

  } else {
    // gradcam is null or errored
    section.classList.add('hidden');
    placeholder.classList.add('hidden');
    disabledMsg.classList.remove('hidden');
  }
}
```

---

#### 6. Reset state on image remove

```javascript
// Add inside existing remove/reset handler — new lines only:
lastGradcam  = null;
lastOriginal = null;
document.getElementById('gradcam-section').classList.add('hidden');
document.getElementById('gradcam-placeholder').classList.add('hidden');
document.getElementById('gradcam-disabled-msg').classList.add('hidden');
document.getElementById('gradcam-rerun-msg').classList.add('hidden');
document.getElementById('run-again-container').classList.add('hidden');
```

---

---

## Improvement 2 — "Run Again" Button

### Behaviour

- Appears inside result card after the first completed assessment.
- Re-submits `selectedFile` (already in memory) with **current** model + Grad-CAM toggle settings.
- Hidden during loading; reappears after result. No delete/re-upload needed.

### Backend — No Changes Required

---

### Frontend — HTML Changes

Add inside your existing result card, below the probabilities section:

```html
<!-- ── FEAT-03: Run Again button ── -->
<div id="run-again-container" class="hidden mt-4 pt-4 border-t border-slate-100">
  <button onclick="runAssessment()"
    class="w-full flex items-center justify-center gap-2 px-4 py-2.5
           rounded-xl border-2 border-teal-500 text-teal-700 text-sm font-semibold
           bg-white hover:bg-teal-50 active:bg-teal-100 transition-all">
    <i data-lucide="refresh-cw" class="w-4 h-4"></i>
    Run Again
  </button>
  <p class="text-center text-xs text-slate-400 mt-2">
    Reruns with current model &amp; Grad-CAM settings — no need to re-upload.
  </p>
</div>
<!-- ── end FEAT-03 Run Again ── -->
```

---

### Frontend — JavaScript Changes

#### 7. Extract existing submit logic into `runAssessment()`

```javascript
// ── FEAT-03: unified assessment runner ───────────────────────────
async function runAssessment() {
  if (!selectedFile) return;

  setLoadingState(true);   // your existing loading-state function
  document.getElementById('run-again-container').classList.add('hidden');

  const formData = new FormData();
  formData.append('file',            selectedFile);
  formData.append('model_type',      getSelectedModelType());
  formData.append('gradcam_enabled', document.getElementById('gradcam-toggle').checked);

  try {
    const response = await fetch('/api/predict', { method: 'POST', body: formData });
    const result   = await response.json();

    if (result.error) {
      showError(result.error);
    } else {
      renderResult(result);
      document.getElementById('run-again-container').classList.remove('hidden');
    }
  } catch (err) {
    showError('Network error. Check Flask server.');
  } finally {
    setLoadingState(false);
  }
}

function getSelectedModelType() {
  const radio = document.querySelector('input[name="model_type"]:checked');
  return radio ? radio.value : 'ensemble';
}
// ── end FEAT-03 ─────────────────────────────────────────────────
```

#### 8. Update existing submit button to call `runAssessment()`

```html
<!-- change only the onclick value of your existing submit button -->
<button onclick="runAssessment()" ...>
  Run Assessment
</button>
```

---

## Full State Map

| User action | Grad-CAM section | Run Again button |
|-------------|-----------------|-----------------|
| Page load | hidden | hidden |
| Upload image, toggle ON, no result | placeholder visible | hidden |
| Upload image, toggle OFF, no result | disabled msg visible | hidden |
| Assessment running | loading state | hidden |
| Result shown, toggle was ON | heatmap visible | visible |
| Result shown, toggle was OFF | disabled msg visible | visible |
| Toggle OFF → ON, result has Grad-CAM | heatmap appears instantly | visible |
| Toggle OFF → ON, result has **no** Grad-CAM | **auto re-runs**, rerun msg shown | hidden → reappears |
| Toggle ON → OFF, result exists | heatmap hides instantly | visible |
| Click Run Again | re-submits same image | hidden → reappears |
| Remove image | all hidden | hidden |

---

## Testing Checklist

- [ ] Toggle ON before run → placeholder visible
- [ ] Toggle OFF before run → disabled msg visible
- [ ] Run with toggle ON → heatmap renders; Run Again appears
- [ ] Run with toggle OFF → disabled msg; Run Again appears
- [ ] Toggle ON after result with Grad-CAM → heatmap instantly (no network call)
- [ ] Toggle ON after result **without** Grad-CAM → rerun msg shown → heatmap appears after
- [ ] Toggle OFF after result → heatmap hides, disabled msg shows (no network call)
- [ ] Run Again with toggle ON → new heatmap; Run Again reappears
- [ ] Run Again with toggle OFF → no heatmap; disabled msg; Run Again reappears
- [ ] Change model → Run Again → result uses new model
- [ ] Remove image → all state reset, all elements hidden
