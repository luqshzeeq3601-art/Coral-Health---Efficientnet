# FYP Report — Coral Reef Health Assessment via CNN-Based Image Analysis

**Student:** Muhammad Luqman Haziq bin Mohamad Lofi (221022249)  
**Programme:** Bachelor of Computer Engineering  
**Faculty:** Faculty of Electronic Engineering Technology (FTKE)  
**University:** Universiti Malaysia Perlis (UniMAP)  
**Supervisor:** Assoc. Prof. Ts. Dr. Yasmin Yacob  
**Academic Session:** 2025/2026

---

## Report Structure

| Chapter | Title | File |
|---------|-------|------|
| 1 | Introduction | [Chapter1_Introduction.md](Chapter1_Introduction.md) |
| 2 | Literature Review | *(To be drafted)* |
| 3 | Methodology | [01_Methodology.md](01_Methodology.md) |
| 4 | Results & Discussion | *(To be drafted — figures ready in `Efficientnet base vs Ensemble`)* |
| 5 | Conclusion & Future Work | *(To be drafted)* |

---

## Canonical Benchmark (Locked)

All report chapters must reference the following verified benchmark. No retraining was performed.

| Item | Value |
|------|------:|
| Architecture | EfficientNetB0 (ImageNet pretrained) |
| Ensemble Strategy | 5-seed SWA (seeds 42–46) |
| Inference Strategy | Multi-Scale TTA (224 + 256, original + H-flip) |
| Calibration | Temperature Scaling (T = 0.441) |
| Input Resolution | 224 × 224 × 3 RGB |
| Test Accuracy | **98.11%** |
| Test Samples | 159 |
| Total Errors | 3 |
| Mean Inference Time | 10.38 ms/image |
| Macro F1 | 0.98 |

---

## Updated Project Objectives (FYP 2 — Final)

1. To develop a deep learning model based on a pretrained EfficientNetB0 architecture with Stochastic Weight Averaging (SWA) and multi-seed ensemble strategy for coral reef health classification.
2. To apply Gradient-weighted Class Activation Mapping (Grad-CAM) as a visual explanation method to support the interpretation and validation of the model's classification decisions.
3. To evaluate the model's performance using standard classification metrics, including accuracy, precision, recall, and F1-score, on a held-out test set.
4. To deploy the trained model as a web-based application with real-time inference and explainability visualisation capabilities.

---

## Updated Project Scope (FYP 2 — Final)

- **Dataset:** BHD Coral Dataset sourced from Kaggle, comprising 795 images across three classes — Healthy, Bleached, and Dead.
- **Classification:** Multi-class image classification using a pretrained EfficientNetB0 backbone with transfer learning.
- **Ensemble:** Five independently seeded models (seeds 42–46) trained with Stochastic Weight Averaging (SWA) and combined via prediction averaging.
- **Inference Enhancement:** Multi-Scale Test-Time Augmentation (TTA) at 224 × 224 and 256 × 256 resolutions with horizontal flip, coupled with Temperature Scaling (T = 0.441) for confidence calibration.
- **Explainability:** Grad-CAM visualisation using the JET colourmap to highlight discriminative regions in coral images.
- **Deployment:** A locally hosted Flask web application featuring drag-and-drop image upload, real-time classification, confidence scoring, and Grad-CAM overlay display.
- **Hardware:** Training performed on NVIDIA RTX 3070 GPU with CUDA and cuDNN acceleration.
- **Exclusions:** No real-time video analysis, no live data collection, no private or proprietary datasets, no species-level identification, and no disease diagnosis beyond the defined three-class taxonomy.

---

## Key Changes from FYP 1 Proposal

| Aspect | FYP 1 (Original) | FYP 2 (Updated) |
|--------|------------------|-----------------|
| Model | Generic CNN (unspecified) | EfficientNetB0 (ImageNet pretrained) |
| Training | Single model, single seed | 5-seed SWA ensemble |
| Inference | Standard forward pass | Multi-Scale TTA + Temperature Scaling |
| Explainability | "Visual explanation method" (unspecified) | Grad-CAM with JET colourmap |
| Deployment | Not in scope | Flask web app with live inference & Grad-CAM |
| Objective 4 | Not present | Added: web-based deployment objective |
| Accuracy Target | Not specified | Achieved 98.11% on 159-image test set |

---

*Last Updated: 29 April 2026*
