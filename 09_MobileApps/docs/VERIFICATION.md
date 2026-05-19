# Verification & Test Checklist

## How to Run

```bash
# Backend
cd 09_MobileApps\backend
uvicorn main:app --port 8000 --host 0.0.0.0

# Flutter on Pixel 6 emulator
cd 09_MobileApps\flutter_app
flutter run
```

---

## Golden Path Tests

### Base Mode (on-device, offline)
- [ ] Turn off Wi-Fi on emulator (Settings → Wi-Fi → off)
- [ ] Select **Base** model in Analysis Screen
- [ ] Upload a **Healthy** coral image from gallery
- [ ] Expected: prediction = "Healthy", confidence > 75%, Grad-CAM overlay visible
- [ ] Upload a **Bleached** coral image
- [ ] Expected: prediction = "Bleached", amber badge
- [ ] Upload a **Dead** coral image
- [ ] Expected: prediction = "Dead", red badge

### Ensemble Mode (API)
- [ ] Start backend (`uvicorn main:app --port 8000 --host 0.0.0.0`)
- [ ] In Settings, set URL = `http://10.0.2.2:8000`, tap "Test Connection" → green OK
- [ ] Select **Ensemble** model in Analysis Screen
- [ ] Run prediction on Healthy, Bleached, Dead images (same as above)
- [ ] Expected: response includes `individual_models` array (5 entries, one per seed)
- [ ] Expected: Grad-CAM overlay is server-rendered (gradient-based)

---

## Edge Case Tests

| Scenario | Expected Behaviour |
|---|---|
| Select a `.pdf` or non-image file | Error snackbar: "Please select an image file" |
| Low-confidence prediction (ambiguous image) | Uncertainty banner appears (confidence < 75%) |
| Ensemble mode with backend offline | Error snackbar: "Cannot reach backend. Switch to Base mode." |
| History: save result, restart app | Entry persists in History Screen |
| History: long-press → delete | Entry removed, list updates immediately |
| Settings: dark mode toggle | App theme switches without restart |

---

## UI Checks

- [ ] Confidence ring animates from 0 to final value on result load
- [ ] Grad-CAM toggle cycles: Original → Overlay → Heatmap → Original
- [ ] Probability bars show all 3 classes summing to ~100%
- [ ] Status badge color matches class (green / amber / red)
- [ ] Home Screen shows last result preview card after first analysis
- [ ] Info Screen cards expand/collapse correctly
- [ ] Settings "Test Connection" shows loading state then result

---

## Performance Targets

| Metric | Target |
|---|---|
| Base mode inference time | < 200 ms on Pixel 6 emulator |
| Ensemble mode API round-trip | < 3 s on local network |
| App cold start | < 2 s |
| Grad-CAM overlay render | < 500 ms |
