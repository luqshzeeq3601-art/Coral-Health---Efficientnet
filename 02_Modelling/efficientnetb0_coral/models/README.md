# `models/` - Current Robust Ensemble Model Artifacts

This folder contains the current EfficientNetB0 Robust Ensemble checkpoints,
training-native weight exports, and calibration files used by the modelling
pipeline and web application.

---

## Files

| File | Description |
|---|---|
| `efficientnetb0_v4robust_seed42.h5` | Legacy final epoch checkpoint snapshot retained for seed 42 |
| `efficientnetb0_v4robust_seed42.weights.h5` | Final epoch weights export for seed 42 |
| `efficientnetb0_v4robust_seed42_swa.h5` | SWA deployment checkpoint for seed 42 |
| `efficientnetb0_v4robust_seed42_swa.weights.h5` | Latest SWA weights export for seed 42 |
| `efficientnetb0_v4robust_seed43.weights.h5` | Final epoch weights export for seed 43 |
| `efficientnetb0_v4robust_seed43_swa.h5` | SWA deployment checkpoint for seed 43 |
| `efficientnetb0_v4robust_seed43_swa.weights.h5` | Latest SWA weights export for seed 43 |
| `efficientnetb0_v4robust_seed44.weights.h5` | Final epoch weights export for seed 44 |
| `efficientnetb0_v4robust_seed44_swa.h5` | SWA deployment checkpoint for seed 44 |
| `efficientnetb0_v4robust_seed44_swa.weights.h5` | Latest SWA weights export for seed 44 |
| `efficientnetb0_v4robust_seed45.weights.h5` | Final epoch weights export for seed 45 |
| `efficientnetb0_v4robust_seed45_swa.h5` | SWA deployment checkpoint for seed 45 |
| `efficientnetb0_v4robust_seed45_swa.weights.h5` | Latest SWA weights export for seed 45 |
| `efficientnetb0_v4robust_seed46.weights.h5` | Final epoch weights export for seed 46 |
| `efficientnetb0_v4robust_seed46_swa.h5` | SWA deployment checkpoint for seed 46 |
| `efficientnetb0_v4robust_seed46_swa.weights.h5` | Latest SWA weights export for seed 46 |
| `temperature.txt` | Temperature scaling value used for probability calibration |

The current folder does not contain non-SWA plain `.h5` checkpoints for seeds
43-46; those seeds are represented by their `.weights.h5` exports and SWA
deployment checkpoints.

---

## Which Files Are Used?

The current web application and audit flow load the deployment checkpoints:
`efficientnetb0_v4robust_seed{42..46}_swa.h5`

The `.weights.h5` files are the latest training-native exports saved by the
current training pipeline and are useful for reloading weights into the same
architecture during retraining, evaluation, or artifact regeneration.

---

## Keep These Files

Do not remove the `_swa.h5` deployment checkpoints or `temperature.txt`, since
they are required by the current inference pipeline. The `.weights.h5` files
should also be kept if you want reproducible retraining and replotting from the
latest training run.
