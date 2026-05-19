# Baseline Model Outputs

This folder contains outputs for the baseline EfficientNetB0 model only.

These files should be used when describing the base model before improvement.
Do not use this folder for the baseline-vs-current-model comparison figures.

Key files:

- `eval_summary.json`: source of baseline metrics
- `classification_report.txt`: text report for baseline precision, recall, and F1
- `confusion_matrix.png`: baseline-only confusion matrix
- `training_history.png`: baseline-only training curve
- `gradcam_outputs.png`: baseline-only Grad-CAM examples

Regenerate with:

```powershell
python 05_Baseline_Model\train_baseline.py
```
