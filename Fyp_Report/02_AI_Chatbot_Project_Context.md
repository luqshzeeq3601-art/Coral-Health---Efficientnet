# AI Chatbot Context (Paste-Ready)

Use the text below when asking an AI chatbot about this project.

```text
I am a final year Computer Engineering student at Universiti Malaysia Perlis (UniMAP).
My project is titled "Coral Reef Health Assessment via Convolutional Neural Network-Based Image Analysis."
Supervised by Assoc. Prof. Ts. Dr. Yasmin Yacob.

Project goal:
- Build a deep learning system to classify coral reef images into 3 classes: Healthy, Bleached, and Dead.
- Deploy it as a web-based application with Grad-CAM explainability.

Updated Project Objectives (FYP 2 — Final):
1. To develop a deep learning model based on a pretrained EfficientNetB0 architecture with Stochastic Weight Averaging (SWA) and multi-seed ensemble strategy for coral reef health classification.
2. To apply Gradient-weighted Class Activation Mapping (Grad-CAM) as a visual explanation method to support the interpretation and validation of the model's classification decisions.
3. To evaluate the model's performance using standard classification metrics, including accuracy, precision, recall, and F1-score, on a held-out test set.
4. To deploy the trained model as a web-based application with real-time inference and explainability visualisation capabilities.

Current project structure:
- 02_Modelling: model development and experiments (EfficientNetB0, ResNet50, ConvNeXtTiny)
- 03_Model_Evaluation: evaluation scripts and results
- 04_Web_Application: Flask web application
- 05_Baseline_Model: baseline and comparison artifacts
- 06_XAI_Decision_Comparison: explainability and decision analysis
- 07_RealTime_Analysis: isolated real-time runtime pipeline

Final benchmark to use as canonical result:
- Model: EfficientNetB0 (5-seed SWA ensemble, seeds 42–46)
- Inference: Multi-Scale TTA (224 + 256, original + H-flip) + Temperature Scaling (T=0.441)
- Input size: 224x224
- Test accuracy: 98.11%
- Test samples: 159
- Total errors: 3
- Mean inference time: 10.38 ms/image
- Macro F1: 0.98
- Final result folder: 03_Model_Evaluation/Efficientnet base vs Ensemble

Key changes from FYP 1 proposal:
- Switched from generic CNN to pretrained EfficientNetB0 with transfer learning
- Added 5-seed SWA ensemble training
- Added Multi-Scale TTA and Temperature Scaling for inference
- Specified Grad-CAM with JET colourmap as the XAI method
- Added a 4th objective: deploy as a Flask web app with live inference and Grad-CAM
- Achieved 98.11% accuracy (up from no baseline)

Important constraints:
- Treat final model artifacts as safe and untouchable.
- Do not overwrite canonical results unless explicitly requested.
- Keep new experiments in separate folders.
- Keep explanations/report text aligned with the final benchmark above.

What I want from you:
- Help me write clear FYP report sections (methodology, results, discussion, conclusion).
- Help me improve technical wording to be formal and academically suitable.
- Help me check consistency between claims and benchmark evidence.
- If giving code suggestions, keep changes minimal and non-destructive.

When you answer:
- Use concise academic style.
- If you reference metrics, use the canonical benchmark values above.
- If assumptions are needed, state them clearly.
```
