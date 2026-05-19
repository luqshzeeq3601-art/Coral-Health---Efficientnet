# Methodology

## 1. Project Overview

This project develops an automated coral reef health classification system using deep learning. The system classifies coral images into three classes:

- Healthy
- Bleached
- Dead

The workflow is organized into modelling, evaluation, explainability, and deployment phases to ensure reproducibility and practical usability.

## 2. Data Preparation

The coral image dataset is strictly separated into training, validation, and test splits prior to any further manipulation to prevent data leakage. During preprocessing:

- **Data Augmentation:** Augmentation techniques (such as rotation and flipping) are applied **exclusively to the training set after the split**. This ensures that the validation and test sets contain only unseen, unmodified original images, maintaining the absolute integrity of the model evaluation.
- Images are resized to the model input resolution.
- Labels are mapped to the three target classes.
- Data loading pipelines are structured for consistent training and evaluation.

For the final benchmark pipeline, the model uses `224 x 224` image input.

## 3. Model Development

Model development is performed in modular experiment folders under `02_Modelling`, including:

- `efficientnetb0_coral`
- `resnet50_coral`
- `convnexttiny_coral`

The final production model is based on **EfficientNetB0** due to its strong accuracy-efficiency tradeoff. Training is done using transfer learning and staged fine-tuning.

## 4. Training Strategy

The training process follows a structured strategy:

- Initialize from pretrained backbone weights.
- Train classification head and then fine-tune deeper layers.
- Use validation monitoring to reduce overfitting.
- Track performance history for accuracy/loss behavior.

The project keeps canonical outputs separated from exploratory runs to protect the final model artifacts.

## 5. Evaluation Protocol

Evaluation is organized under `03_Model_Evaluation`, with final chapter-ready outputs in:

- `03_Model_Evaluation/Efficientnet base vs Ensemble`

The model's performance is rigorously assessed on a held-out test set using standard classification metrics:
- **Accuracy:** The overall correctness of predictions across all classes.
- **Precision, Recall, and F1-Score:** Calculated for each specific class (Healthy, Bleached, Dead) to assess class-specific predictive capability.
- **Aggregated Metrics (Macro & Weighted Averages):** Due to varying support sizes across classes (e.g., 72 Healthy vs. 15 Dead), both macro-averaged and weighted-averaged precision, recall, and F1-scores are utilised to ensure the model is evaluated fairly across minority and majority classes alike.

The final locked benchmark (no retraining) is:

- Architecture: EfficientNetB0
- Input size: `224 x 224`
- Test accuracy: `98.11%`
- Test samples: `159`
- Total errors: `3`
- Mean inference time: `10.38 ms/image`

Evaluation artifacts include confusion matrix, classification report, training-validation curves, Grad-CAM visualizations, and inference-time summary.

## 6. Explainable AI (XAI)

Model interpretability is performed in `06_XAI_Decision_Comparison` using Grad-CAM-based analysis to inspect attention regions and validate whether model focus aligns with coral structures.

This phase supports error analysis and improves confidence in model decision behavior for real-world deployment.

## 7. Deployment Approach

Deployment is implemented as:

- Main Flask web application (`04_Web_Application`)
- Isolated real-time runtime (`07_RealTime_Analysis`)

The isolated runtime design prevents accidental modification of canonical model assets and supports practical camera-based analysis workflows.

## 8. Summary of Methodological Flow

1. Prepare and structure coral image data.
2. Train and compare multiple deep learning architectures.
3. Select final model based on accuracy, robustness, and efficiency.
4. Produce standardized evaluation artifacts for reporting.
5. Validate model behavior with XAI.
6. Deploy in controlled web and real-time environments.

This methodology ensures technical rigor, reproducibility, and alignment with FYP reporting requirements.

