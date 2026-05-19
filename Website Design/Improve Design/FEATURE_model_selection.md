# Feature: Model Selection — Base vs. Ensemble

**Feature ID:** FEAT-01  
**Stack:** Flask (Python) · Vanilla JS · TailwindCSS CDN · Lucide Icons  
**Change type:** Additive only — no existing code is deleted or restructured  

---

## Overview

Adds a radio toggle that lets the user pick **Base** (single seed-42 model) or **Ensemble** (5-seed SWA + TTA) before running inference. The existing `/api/predict` route is extended with one new `form` field; the existing ensemble logic is preserved untouched inside a conditional.

| Mode | Seeds | TTA | Accuracy | Est. latency |
|------|-------|-----|----------|-------------|
| Base | 1 (seed 42) | ✗ | ~94–96% | ~4–5 ms |
| Ensemble | 5 (42–46) | ✓ | **98.11%** | ~10.38 ms |

Default: **Ensemble**.

---

## Backend — `app.py`

### Step 1 — Add `BASE_MODEL` global (after the existing globals, ~line 208)

```python
# Global model store  ← already exists
MODELS = []
LOADED_FOLDS = []
ENSEMBLE_WEIGHTS = None
TEMPERATURE = 1.0

BASE_MODEL = None   # ← ADD THIS LINE ONLY
```

---

### Step 2 — Add `load_base_model()` (paste right after the existing `load_models()` function)

This does **not** touch `load_models()`. It reuses the already-defined `build_model()`.

```python
def load_base_model():
    """Load single EfficientNetB0 (seed 42) for base-model mode."""
    global BASE_MODEL
    model_path = os.path.join(MODEL_DIR, 'efficientnetb0_v4robust_seed42_swa.h5')
    if os.path.exists(model_path):
        try:
            model = build_model()          # reuses existing build_model()
            model.load_weights(model_path)
            model.compile(
                optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            BASE_MODEL = model
            print(f"  [OK] Base model loaded: seed42")
        except Exception as e:
            print(f"  [FAIL] Base model: {e}")
    else:
        print(f"  [SKIP] Base model not found at {model_path}")
```

---

### Step 3 — Call `load_base_model()` at the end of the existing `load_models()`

Add **one line** at the very end of the existing `load_models()` body:

```python
def load_models():
    # ... ALL existing code untouched ...
    load_calibration_artifacts()
    check_metrics_consistency()
    load_base_model()    # ← ADD THIS LINE ONLY
```

---

### Step 4 — Read `model_type` at the top of `/api/predict` (~line 958)

Add two lines immediately after the existing `debug_mode =` line:

```python
        debug_mode = request.args.get('debug') == '1' or True   # ← already exists

        # ── FEAT-01: read model choice from frontend ──
        model_type   = request.form.get('model_type', 'ensemble')
        use_ensemble = (model_type == 'ensemble')
        # ─────────────────────────────────────────────
```

---

### Step 5 — Wrap existing ensemble block + add base branch

Find the line (currently ~line 968):
```python
        if len(MODELS) == 0:
            return jsonify({'error': 'No models loaded. Check server logs.'}), 500
```

Replace that one guard line with the block below. Everything inside `if use_ensemble:` is the existing code moved in **verbatim** — zero changes to its content.

```python
        # ── FEAT-01: guard both paths ────────────────────────────────
        if use_ensemble and len(MODELS) == 0:
            return jsonify({'error': 'No models loaded. Check server logs.'}), 500
        if not use_ensemble and BASE_MODEL is None:
            return jsonify({'error': 'Base model not loaded. Check server logs.'}), 500
        # ─────────────────────────────────────────────────────────────

        if use_ensemble:
            # ═══════════════════════════════════════════════════════════
            # ALL EXISTING TTA + ensemble code goes here — UNCHANGED
            # (TTA_SCALES, tta_crops, tta_batch, per-model loop,
            #  all_preds_tta, avg_preds, temperature_scale_from_probs)
            # ═══════════════════════════════════════════════════════════
            pass   # ← remove this, keep your existing code

        else:
            # ── FEAT-01: Base model path (new) ───────────────────────
            img_float  = img_resized.astype('float32')
            single_pred = BASE_MODEL.predict(
                np.expand_dims(img_float, axis=0), verbose=0
            )[0]
            avg_preds        = temperature_scale_from_probs(single_pred, TEMPERATURE)
            individual_results = []   # no per-fold breakdown for base mode
            debug_preprocessing  = []
            # ─────────────────────────────────────────────────────────

        # The lines below already exist and need no changes:
        final_idx   = int(np.argmax(avg_preds))
        final_conf  = float(avg_preds[final_idx] * 100)
        final_label = CLASS_NAMES[final_idx]
        probabilities = {name: float(avg_preds[i] * 100) for i, name in enumerate(CLASS_NAMES)}
```

---

### Step 6 — Add `model_used` to the existing `result` dict (~line 1124)

Append **one key** to the existing dict — nothing else changes:

```python
        result = {
            'prediction':        final_label,       # unchanged
            'confidence':        final_conf,         # unchanged
            'probabilities':     probabilities,      # unchanged
            'individual_models': individual_results, # unchanged
            'gradcam':           gradcam_data,       # unchanged
            'original_image':    original_b64,       # unchanged
            'status':            current_status,     # unchanged
            'uncertainty':       final_conf < CONFIDENCE_THRESHOLD,  # unchanged
            'notes':             notes,              # unchanged
            # ── FEAT-01: new key ──
            'model_used': (
                'EfficientNetB0 SWA Ensemble (5-seed)'
                if use_ensemble else
                'EfficientNetB0 Base (seed 42)'
            ),
        }
```

---

## Frontend — HTML Template

> All classes below use **TailwindCSS CDN utilities** matching the existing design.  
> Paste this block **inside the existing upload card**, above the file input / submit button.

### HTML — Radio Group

```html
<!-- ── FEAT-01: Model Selection ── -->
<div class="mb-5">
  <p class="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-3">Model</p>
  <div class="grid grid-cols-2 gap-3">

    <!-- Ensemble card -->
    <label id="label-ensemble"
      class="flex flex-col gap-1 p-3 rounded-xl border-2 border-teal-500 bg-teal-50 cursor-pointer transition-all">
      <div class="flex items-center gap-2">
        <input type="radio" name="model_type" value="ensemble" checked
               class="accent-teal-600" onchange="onModelChange()">
        <span class="text-sm font-semibold text-slate-800">Ensemble</span>
      </div>
      <span class="text-xs text-slate-500">5-seed SWA · 98.11%</span>
      <div class="flex gap-1 flex-wrap mt-1">
        <span class="text-[10px] bg-teal-100 text-teal-800 px-1.5 py-0.5 rounded font-medium">SWA</span>
        <span class="text-[10px] bg-teal-100 text-teal-800 px-1.5 py-0.5 rounded font-medium">TTA</span>
      </div>
    </label>

    <!-- Base card -->
    <label id="label-base"
      class="flex flex-col gap-1 p-3 rounded-xl border-2 border-slate-200 bg-white cursor-pointer transition-all hover:border-slate-300">
      <div class="flex items-center gap-2">
        <input type="radio" name="model_type" value="base"
               class="accent-blue-600" onchange="onModelChange()">
        <span class="text-sm font-semibold text-slate-800">Base</span>
      </div>
      <span class="text-xs text-slate-500">Single seed · faster</span>
      <div class="flex gap-1 flex-wrap mt-1">
        <span class="text-[10px] bg-blue-100 text-blue-800 px-1.5 py-0.5 rounded font-medium">EfficientNetB0</span>
      </div>
    </label>

  </div>
</div>
<!-- ── end FEAT-01 ── -->
```

---

### JavaScript — `onModelChange()` and `FormData` append

Add this function **alongside existing JS** — no existing function is modified:

```javascript
// ── FEAT-01: Model Selection ──────────────────────────────────────
function onModelChange() {
  const selected = document.querySelector('input[name="model_type"]:checked').value;

  document.getElementById('label-ensemble').className = selected === 'ensemble'
    ? 'flex flex-col gap-1 p-3 rounded-xl border-2 border-teal-500 bg-teal-50 cursor-pointer transition-all'
    : 'flex flex-col gap-1 p-3 rounded-xl border-2 border-slate-200 bg-white cursor-pointer transition-all hover:border-slate-300';

  document.getElementById('label-base').className = selected === 'base'
    ? 'flex flex-col gap-1 p-3 rounded-xl border-2 border-blue-500 bg-blue-50 cursor-pointer transition-all'
    : 'flex flex-col gap-1 p-3 rounded-xl border-2 border-slate-200 bg-white cursor-pointer transition-all hover:border-slate-300';
}
// ── end FEAT-01 ──────────────────────────────────────────────────
```

In your **existing** submit/fetch function, add **one line** before `fetch()`:

```javascript
// Add inside your existing FormData block — one new line only:
formData.append('model_type', document.querySelector('input[name="model_type"]:checked').value);
```

In your **existing** result-render function, add **one line**:

```javascript
// Add inside your existing renderResult / displayResult function — one new line only:
document.getElementById('model-used-label').textContent = result.model_used ?? '';
```

Add a matching `<span>` near your existing prediction label in the result card HTML:

```html
<!-- Place near your existing prediction/confidence display — one new element only -->
<p id="model-used-label" class="text-xs text-slate-400 mt-0.5"></p>
```

---

## Testing Checklist

- [ ] Page loads with **Ensemble** pre-selected, teal border visible
- [ ] Clicking **Base** → blue border active, teal resets to grey
- [ ] POST body contains correct `model_type` value on submit
- [ ] Base path: `individual_models` is `[]` in response
- [ ] Ensemble path: `individual_models` has 5 entries in response
- [ ] `model_used` text renders in result card
- [ ] All existing fields (`gradcam`, `probabilities`, `status`, `notes`) unchanged
