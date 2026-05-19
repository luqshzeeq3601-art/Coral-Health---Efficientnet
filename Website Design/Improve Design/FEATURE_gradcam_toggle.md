# Feature: Grad-CAM Toggle — Enable / Disable Explainability

**Feature ID:** FEAT-02  
**Stack:** Flask (Python) · Vanilla JS · TailwindCSS CDN · Lucide Icons  
**Change type:** Additive only — the existing Grad-CAM block is wrapped, not rewritten  

---

## Overview

Adds an on/off switch for Grad-CAM heatmap generation. When **OFF**, the existing `compute_gradcam()` block is skipped entirely and `gradcam` in the response is `null`. The existing result card already reads `result.gradcam` — we only add a null-check to the existing render logic.

| State | Behaviour | `gradcam` in response | Latency saved |
|-------|-----------|----------------------|--------------|
| **ON** (default) | Existing Grad-CAM block runs normally | `{heatmap, overlay}` | — |
| **OFF** | Block skipped | `null` | ~2–4 ms |

---

## Backend — `app.py`

### Step 1 — Read `gradcam_enabled` at the top of `/api/predict` (~line 958)

Add **one line** directly after the existing `debug_mode =` line (and after the `model_type` lines from FEAT-01 if already applied):

```python
        debug_mode   = request.args.get('debug') == '1' or True   # ← already exists
        model_type   = request.form.get('model_type', 'ensemble')  # ← FEAT-01 (if applied)
        use_ensemble = (model_type == 'ensemble')                  # ← FEAT-01 (if applied)

        # ── FEAT-02: Grad-CAM toggle ──
        gradcam_enabled = request.form.get('gradcam_enabled', 'true').lower() == 'true'
        # ─────────────────────────────
```

---

### Step 2 — Wrap the existing Grad-CAM block with `if gradcam_enabled:`

Find the existing block that starts at **~line 1042**:

```python
        # Explainability (Ensemble Grad-CAM Average)
        img_for_gradcam = img_resized.astype('float32')
        gradcam_data = {}
        try:
            ...
        except Exception as e:
            ...
            gradcam_data = {'error': str(e)}
```

Change **only** these two lines — everything inside the `try/except` stays identical:

```python
        # Explainability (Ensemble Grad-CAM Average)
        img_for_gradcam = img_resized.astype('float32')

        # ── FEAT-02: wrap with toggle ─────────────────────────────────
        gradcam_data = None                       # ← was `{}`, now None when disabled

        if gradcam_enabled:                       # ← new wrapper line
            try:
                # ═══════════════════════════════════════════════════════
                # ALL EXISTING Grad-CAM code goes here — UNCHANGED
                # (ensemble_heatmaps loop, avg_heatmap, create_overlay,
                #  heatmap_to_base64, numpy_to_base64, gradcam_data = {...})
                # ═══════════════════════════════════════════════════════
                pass   # ← remove this, keep your existing try body

            except Exception as e:
                print(f"Explainability Error: {e}")
                gradcam_data = {'error': str(e)}   # ← existing except body unchanged
        # ── end FEAT-02 ──────────────────────────────────────────────
```

> **Only two things change:** `gradcam_data = {}` becomes `gradcam_data = None`, and the existing try/except is indented one level inside `if gradcam_enabled:`. The `result` dict already uses `'gradcam': gradcam_data` — no change needed there.

---

## Frontend — HTML Template

> All classes use **TailwindCSS CDN utilities** matching the existing design.  
> Paste the toggle block **inside the existing upload card**, below the model selection (FEAT-01) and above the file input.

### HTML — Toggle Switch

```html
<!-- ── FEAT-02: Grad-CAM Toggle ── -->
<div class="mb-5">
  <p class="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3">Explainability</p>

  <div class="flex items-center justify-between p-3 rounded-xl border border-slate-200 bg-white">
    <div>
      <p class="text-sm font-semibold text-slate-800">Grad-CAM Heatmap</p>
      <p class="text-xs text-slate-500 mt-0.5">Visualize attention regions</p>
    </div>

    <!-- Toggle switch (pure CSS, no external dependency) -->
    <label class="relative inline-flex items-center cursor-pointer">
      <input type="checkbox" id="gradcam-toggle" checked class="sr-only peer"
             onchange="onGradcamChange(this.checked)">
      <div class="w-10 h-5 bg-slate-200 rounded-full peer
                  peer-checked:bg-teal-500
                  after:content-[''] after:absolute after:top-0.5 after:left-0.5
                  after:bg-white after:rounded-full after:h-4 after:w-4
                  after:transition-all peer-checked:after:translate-x-5"></div>
    </label>
  </div>

  <!-- Hint — shown/hidden by JS -->
  <div id="gradcam-hint-on"
    class="mt-2 px-3 py-2 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-700">
    <span class="font-medium">Grad-CAM Active</span> — adds ~2–4 ms latency. Highlights regions influencing the prediction.
  </div>
  <div id="gradcam-hint-off"
    class="mt-2 px-3 py-2 rounded-lg bg-slate-100 border border-slate-200 text-xs text-slate-500 hidden">
    Grad-CAM disabled. Only classification output will be shown.
  </div>
</div>
<!-- ── end FEAT-02 ── -->
```

---

### JavaScript — `onGradcamChange()` and `FormData` append

Add this function **alongside existing JS** — no existing function is modified:

```javascript
// ── FEAT-02: Grad-CAM Toggle ──────────────────────────────────────
function onGradcamChange(enabled) {
  document.getElementById('gradcam-hint-on').classList.toggle('hidden', !enabled);
  document.getElementById('gradcam-hint-off').classList.toggle('hidden', enabled);
}
// ── end FEAT-02 ──────────────────────────────────────────────────
```

In your **existing** submit/fetch function, add **one line** before `fetch()`:

```javascript
// Add inside your existing FormData block — one new line only:
formData.append('gradcam_enabled', document.getElementById('gradcam-toggle').checked);
```

---

### JavaScript — Null-check in existing render function

Find where your **existing** render function reads `result.gradcam`. Add a null-check around the existing Grad-CAM display block:

```javascript
// ── FEAT-02: wrap existing gradcam render with null-check ─────────
if (result.gradcam && !result.gradcam.error) {
  // ── existing code that renders gradcam images goes here unchanged ──
  document.getElementById('img-original').src = 'data:image/png;base64,' + result.original_image;
  document.getElementById('img-overlay').src  = 'data:image/png;base64,' + result.gradcam.overlay;
  document.getElementById('img-heatmap').src  = 'data:image/png;base64,' + result.gradcam.heatmap;
  document.getElementById('gradcam-section').classList.remove('hidden');

} else if (result.gradcam && result.gradcam.error) {
  // existing error path — unchanged
  document.getElementById('gradcam-section').classList.add('hidden');

} else {
  // ── FEAT-02: gradcam is null (user disabled it) ──
  document.getElementById('gradcam-section').classList.add('hidden');
  document.getElementById('gradcam-disabled-msg').classList.remove('hidden');
}
// ─────────────────────────────────────────────────────────────────
```

Add the disabled message element **once** in your HTML, right below the existing `gradcam-section` div:

```html
<!-- One new element below existing gradcam-section — hidden by default -->
<p id="gradcam-disabled-msg"
   class="hidden text-center text-sm text-slate-400 py-4">
  Grad-CAM is disabled. Enable it above to visualize attention regions.
</p>
```

Make sure to hide the message again when a new prediction starts:

```javascript
// Add one line inside your existing "loading / reset" block:
document.getElementById('gradcam-disabled-msg').classList.add('hidden');
```

---

## Behaviour Matrix

| `model_type` | `gradcam_enabled` | Grad-CAM runs on | `gradcam` in response |
|---|---|---|---|
| `ensemble` | `true` | 5 models → averaged heatmap | `{heatmap, overlay}` |
| `base` | `true` | seed-42 model only | `{heatmap, overlay}` |
| `ensemble` | `false` | skipped | `null` |
| `base` | `false` | skipped | `null` |

---

## Testing Checklist

- [ ] Page loads with toggle **ON** (teal), hint-on visible, hint-off hidden
- [ ] Toggle OFF → hint swaps, POST sends `gradcam_enabled=false`
- [ ] Toggle ON → POST sends `gradcam_enabled=true`
- [ ] Backend skips `compute_gradcam()` when flag is `false`
- [ ] Response `gradcam` is `null` when disabled
- [ ] Grad-CAM section hidden when `gradcam` is `null`; disabled message shown
- [ ] Grad-CAM section visible and images render when `gradcam` is present
- [ ] All existing result fields (`prediction`, `confidence`, `probabilities`, `status`) unaffected
- [ ] No `hidden` class left on `gradcam-disabled-msg` between consecutive submissions
