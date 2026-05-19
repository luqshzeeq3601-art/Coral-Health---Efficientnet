# Chapter 4: Results and Discussion

## 4.2 Discussion

### 4.2.1 Data Split and Reliability

The split manifest in [05_Baseline_Model/split_info_v3.json](05_Baseline_Model/split_info_v3.json) shows a balanced validation and test distribution (72 Healthy, 72 Bleached, 15 Dead). This balance stabilizes class comparisons, but the Dead class remains small, so a single error changes recall by about 6.7 percentage points. This explains why Dead recall is the most sensitive metric and should be interpreted with more caution than Healthy and Bleached results.

### 4.2.2 Model Performance and Error Profile

The final EfficientNetB0 ensemble achieves 98.11% accuracy with only three errors. The error pattern is directional: two Bleached samples are predicted as Healthy and one Dead sample is predicted as Bleached. This suggests visual overlap in intermediate bleaching stages, where texture and color can shift toward healthy coral features. The model avoids false Dead predictions (Dead precision = 1.00), which is important for deployment scenarios where false alarms could trigger unnecessary interventions. These outcomes are visible in Figure 4.5 and Figure 4.6.

Figure 4.5: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/05_final_confusion_matrix.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/05_final_confusion_matrix.png)

Figure 4.6: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/06_final_classification_report_table.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/06_final_classification_report_table.png)

### 4.2.3 Generalization and Overfitting Analysis

Training and validation curves show stable convergence, and the accuracy and loss gaps shrink toward zero in later epochs, indicating minimal overfitting. The early negative accuracy gap is consistent with strong augmentation and Mixup during training, which can make training batches harder than the validation set. These behaviors are shown in Figure 4.1 to Figure 4.4.

Figure 4.1: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/01_training_validation_accuracy.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/01_training_validation_accuracy.png)

Figure 4.2: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/02_training_validation_loss.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/02_training_validation_loss.png)

Figure 4.3: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/03_accuracy_gap_per_epoch.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/03_accuracy_gap_per_epoch.png)

Figure 4.4: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/04_loss_gap_per_epoch.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/04_loss_gap_per_epoch.png)

### 4.2.4 Architecture Trade-offs

Although EfficientNetB0 and ResNet50 both reach 98.11% accuracy, macro F1 and Dead F1 separate their robustness. ResNet50 underperforms on the Dead class (F1 0.8966), while EfficientNetB0 sustains higher macro F1 (0.9769). This shows that accuracy alone can hide class-specific weaknesses. ConvNeXtTiny has the largest parameter count but does not exceed the ensemble in accuracy, indicating that capacity without the ensemble effect does not necessarily yield better generalization on this split. The summary values are recorded in [03_Model_Evaluation/02_Architecture_Comparison/architecture_comparison_summary.csv](03_Model_Evaluation/02_Architecture_Comparison/architecture_comparison_summary.csv).

### 4.2.5 Baseline vs Final Model Improvement

The final model improves accuracy by 13.20 percentage points and reduces errors from 24 to 3. Macro F1 increases from 79.19% to 97.69%, indicating that the improvement is consistent across classes rather than concentrated in a single class. This change aligns with the documented optimization steps (regularization, augmentation tuning, and class balancing). The comparison table is shown in Figure 4.7.

Figure 4.7: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/03_Efficientnet base vs Ensemble.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/03_Efficientnet%20base%20vs%20Ensemble.png)

### 4.2.6 Explainable AI Interpretation

Grad-CAM panels show the regions that contribute most to each class prediction, supporting qualitative trust in the model. A separate panel highlights a representative error case to show where attention may be ambiguous. These are shown in Figure 4.8 and Figure 4.9.

Figure 4.8: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/08_gradcam_panel_healthy_bleached_dead.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/08_gradcam_panel_healthy_bleached_dead.png)

Figure 4.9: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/09_gradcam_wrong_prediction_bleached_492.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/09_gradcam_wrong_prediction_bleached_492.png)

### 4.2.7 Computational Performance

Inference time rises from 1.81 ms/image in the baseline to 10.38 ms/image in the final model. This trade-off is expected due to the ensemble and improved accuracy. The absolute latency remains low enough for near-real-time evaluation on desktop-class hardware, but edge deployment may require pruning, quantization, or a single-model alternative. The inference summary is shown in Figure 4.10.

Figure 4.10: <caption to insert>. See [03_Model_Evaluation/Efficientnet base vs Ensemble/10_final_inference_time_summary_table.png](03_Model_Evaluation/Efficientnet%20base%20vs%20Ensemble/10_final_inference_time_summary_table.png)

### 4.2.8 Limitations and Quantified Uncertainty

- Overall accuracy is 98.11% (156/159), with a 95% Wilson confidence interval of 94.60% to 99.36%, reflecting uncertainty from the limited test size.
- Dead recall is 93.33% (14/15), with a 95% Wilson confidence interval of 70.18% to 98.81%, showing high variance due to the small Dead class support.
- Bleached recall is 97.22% (70/72), with a 95% Wilson confidence interval of 90.43% to 99.23%.
- Healthy recall is 100.00% (72/72), with a 95% Wilson confidence interval of 94.93% to 100.00%.
- The final model is an ensemble, which increases deployment cost; a distillation or single-model proxy could balance accuracy and speed.

### 4.2.9 Next Steps

Future work should validate generalization on a new site or acquisition setting, and measure robustness to lighting and turbidity changes to confirm real-world reliability.
