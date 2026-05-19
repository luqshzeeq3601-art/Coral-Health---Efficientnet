# Chapter 4: Results and Discussion

## 4.1 Results

### 4.1.1 Data Split Manifest

The dataset is partitioned into training, validation, and test splits with a total of 1,582 images. The class distribution is preserved across validation and test, enabling fair class-level comparison. The split definition is recorded in [05_Baseline_Model/split_info_v3.json](05_Baseline_Model/split_info_v3.json).

- Train: 1,265 images (Healthy 569, Bleached 576, Dead 120)
- Validation: 158 images (Healthy 71, Bleached 72, Dead 15)
- Test: 159 images (Healthy 72, Bleached 72, Dead 15)

### 4.1.2 Training and Validation Curves

The learning curves show consistent improvement during training and stable validation behavior.

Figure 4.1: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/01_training_validation_accuracy.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/01_training_validation_accuracy.png)

Figure 4.2: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/02_training_validation_loss.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/02_training_validation_loss.png)

### 4.1.3 Generalization Gap

The gap metrics are computed as training minus validation and are recorded per epoch in [03_Model_Evaluation/Efficientnet base vs Ensemble/03_train_validation_gap_values.csv](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/03_train_validation_gap_values.csv).

- Accuracy gap ranges from -19.31 percentage points at epoch 1 to approximately -0.40 to +0.28 percentage points in the final epochs.
- Loss gap reduces from 0.354 at epoch 1 to about 0.10 by the final epochs.

Figure 4.3: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/03_accuracy_gap_per_epoch.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/03_accuracy_gap_per_epoch.png)

Figure 4.4: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/04_loss_gap_per_epoch.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/04_loss_gap_per_epoch.png)

### 4.1.4 Classification Performance (Test Set)

The final benchmark uses a 5-seed SWA EfficientNetB0 ensemble at 224 x 224 input resolution under a single-scale protocol. The confusion matrix and classification report are presented below.

Figure 4.5: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/05_final_confusion_matrix.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/05_final_confusion_matrix.png)

Figure 4.6: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/06_final_classification_report_table.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/06_final_classification_report_table.png)

Classification report (n=159):

- Healthy: precision 0.9730, recall 1.0000, F1 0.9863 (support 72)
- Bleached: precision 0.9859, recall 0.9722, F1 0.9790 (support 72)
- Dead: precision 1.0000, recall 0.9333, F1 0.9655 (support 15)
- Accuracy: 0.9811
- Macro F1: 0.9769
- Weighted F1: 0.9810

Confusion matrix outcomes (class order: Healthy, Bleached, Dead):

- Healthy: 72 correct
- Bleached: 70 correct, 2 misclassified as Healthy
- Dead: 14 correct, 1 misclassified as Bleached

Per-image confidence values and error listing are recorded in [03_Model_Evaluation/01_EfficientNetB0_Evaluation/detailed_audit_results.md](03_Model_Evaluation/01_EfficientNetB0_Evaluation/detailed_audit_results.md).

### 4.1.5 Architecture Comparison

All models are evaluated on the same 159-image test split. Summary values are recorded in [03_Model_Evaluation/02_Architecture_Comparison/architecture_comparison_summary.csv](03_Model_Evaluation/02_Architecture_Comparison/architecture_comparison_summary.csv).

- EfficientNetB0 Ensemble (20.27M params): accuracy 98.11%, macro F1 0.9769, Dead F1 0.9655, errors 3
- ResNet50 Single (23.59M params): accuracy 98.11%, macro F1 0.9586, Dead F1 0.8966, errors 3
- ConvNeXtTiny Single (27.82M params): accuracy 97.48%, macro F1 0.9724, Dead F1 0.9655, errors 4

### 4.1.6 Baseline vs Final Model

The baseline and final model comparison is summarized in Figure 4.7.

Figure 4.7: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/03_Efficientnet base vs Ensemble.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/03_Efficientnet%20base%20vs%20Ensemble.png)

- Baseline accuracy 84.91% vs final accuracy 98.11%
- Baseline macro F1 79.19% vs final macro F1 97.69%
- Baseline errors 24 vs final errors 3
- Baseline inference time 1.81 ms/image vs final 10.38 ms/image

### 4.1.7 Explainable AI Results (Grad-CAM)

Qualitative Grad-CAM panels provide visual evidence of model attention for each class and for a representative error case.

Figure 4.8: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/08_gradcam_panel_healthy_bleached_dead.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/08_gradcam_panel_healthy_bleached_dead.png)

Figure 4.9: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/09_gradcam_wrong_prediction_bleached_492.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/09_gradcam_wrong_prediction_bleached_492.png)

### 4.1.8 Inference Time Summary

The deployment-oriented inference summary is shown in Figure 4.10.

Figure 4.10: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/10_final_inference_time_summary_table.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/10_final_inference_time_summary_table.png)
