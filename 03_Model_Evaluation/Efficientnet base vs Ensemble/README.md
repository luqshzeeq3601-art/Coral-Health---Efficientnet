# Chapter 4 Final Results

This folder contains clean Chapter 4-ready evaluation outputs generated from stored benchmark results.

## Final Benchmark Used

| Item | Value |
|---|---:|
| Model | Final Model |
| Architecture | EfficientNetB0 |
| Input size | 224 x 224 |
| Final test accuracy | 98.11% |
| Test samples | 159 |
| Total errors | 3 |
| Mean inference time | 10.38 ms/image |

No retraining was performed, model weights were not changed, and prediction values were not modified.

## Generated Files

| File | Description |
|---|---|
| `01_training_validation_accuracy.png` | Training and validation accuracy curve. |
| `02_training_validation_loss.png` | Training and validation loss curve. |
| `03_accuracy_gap_per_epoch.png` | Accuracy gap per epoch in percentage points. |
| `04_loss_gap_per_epoch.png` | Loss gap per epoch in decimal loss units. |
| `03_train_validation_gap_values.csv` | Numeric source values for the two gap figures. |
| `05_final_confusion_matrix.png` | Final confusion matrix. |
| `05_final_confusion_matrix.json` | Confusion matrix metadata and values. |
| `06_final_classification_report_table.png` | Final classification report as a table image. |
| `06_final_classification_report.csv` | Classification report values. |
| `03_Efficientnet base vs Ensemble.png` | Baseline Model vs Final Model comparison table. |
| `03_Efficientnet base vs Ensemble.csv` | Comparison table values. |
| `08_gradcam_panel_healthy_bleached_dead.png` | Final Grad-CAM examples for Healthy, Bleached, and Dead. |
| `09_gradcam_wrong_prediction_bleached_492.png` | Grad-CAM panel for one wrong prediction. |
| `10_final_inference_time_summary_table.png` | Final inference-time summary table. |
| `10_final_inference_time_summary.csv` | Inference-time summary values. |
| `00_source_manifest.json` | Source traceability and generation notes. |

## Gap Definition

The gap figures use `Training - Validation`.

- Accuracy gap is shown in percentage points.
- Loss gap is shown in decimal loss units.
- A zero reference line is included in both figures.
