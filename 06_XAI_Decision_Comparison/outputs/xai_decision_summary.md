# XAI Decision Comparison Summary

Generated: 2026-04-24 22:10:46

This evidence pack compares the baseline EfficientNetB0 model against the current V4 Robust EfficientNetB0 ensemble on curated held-out test images.

Grad-CAM is used as post-prediction explainability evidence. It does not change the prediction or confidence score. The heatmap shows which regions most supported the predicted class for each model.

## How to Read the Panels

- Baseline EffNetB0 prediction only: the base model decision without visual explanation.
- Baseline EffNetB0 Grad-CAM: the image regions supporting the baseline predicted class.
- V4 Robust EffNetB0 prediction only: the current ensemble decision without visual explanation.
- V4 Robust EffNetB0 Grad-CAM: the averaged visual evidence from the current ensemble.

## Selected Cases

- `Healthy/93.png` (healthy_representative_correct): true `Healthy`; Baseline EffNetB0 predicted `Healthy` at 96.1% (correct); V4 Robust EffNetB0 predicted `Healthy` at 92.3% (correct).
- `Bleached/104.png` (bleached_representative_correct): true `Bleached`; Baseline EffNetB0 predicted `Bleached` at 98.1% (correct); V4 Robust EffNetB0 predicted `Bleached` at 99.4% (correct).
- `Dead/29.png` (dead_representative_correct): true `Dead`; Baseline EffNetB0 predicted `Dead` at 70.3% (correct); V4 Robust EffNetB0 predicted `Dead` at 99.4% (correct).
- `Dead/82.png` (baseline_wrong_current_correct): true `Dead`; Baseline EffNetB0 predicted `Bleached` at 53.1% (wrong); V4 Robust EffNetB0 predicted `Dead` at 97.7% (correct).
- `Bleached/708.png` (current_uncertain): true `Bleached`; Baseline EffNetB0 predicted `Dead` at 54.5% (wrong); V4 Robust EffNetB0 predicted `Bleached` at 42.1% (correct).
- `Bleached/492.png` (current_wrong): true `Bleached`; Baseline EffNetB0 predicted `Healthy` at 67.7% (wrong); V4 Robust EffNetB0 predicted `Healthy` at 54.3% (wrong).

## Thesis Interpretation

Use these panels to explain how the model reached its coral-health decision. A useful defence statement is: the classification output tells us what the model decided, while Grad-CAM helps inspect whether the decision is visually grounded in coral-relevant regions instead of background artifacts.

The uncertainty reference threshold used for selecting challenging examples is 75.0% current-model confidence.

Do not claim that Grad-CAM improves benchmark accuracy. It supports interpretability and trust analysis after the model has already made a decision.
