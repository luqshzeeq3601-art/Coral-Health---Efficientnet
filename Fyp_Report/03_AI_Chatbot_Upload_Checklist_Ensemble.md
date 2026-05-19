# Which Coding Parts to Upload to AI Chatbot (Ensemble-Focused)

## Purpose

This guide lists the **coding files/folders to share with an AI chatbot** when you want help related to the **ensemble coral classification model** and its final benchmark.

Use this together with `02_AI_Chatbot_Project_Context.md` so responses stay aligned with the canonical result.

## Upload First (Core Ensemble-Relevant Code)

1. `03_Model_Evaluation/Efficientnet base vs Ensemble/`
- Upload key outputs that define the final benchmark (`98.11%`, 224x224, 159 test images).
- Include: classification report, confusion matrix JSON, and final error analysis table.

2. `03_Model_Evaluation` scripts used for final evaluation
- Upload the exact Python scripts that generated the Chapter 4 final results.
- This lets the chatbot verify metric logic and avoid mismatched calculations.

3. `02_Modelling/efficientnetb0_coral/`
- Upload model-building, training, and checkpoint-selection scripts that support the final ensemble pipeline.
- Prioritize files that define architecture, training config, and inference/preprocessing settings.

4. `06_XAI_Decision_Comparison` (selected files)
- Upload Grad-CAM or decision-comparison scripts used to explain ensemble behavior.
- Include only files directly referenced by your report claims.

## Optional Upload (If You Need Deployment Help)

1. `04_Web_Application`
- Upload only the inference-related files (loading model, preprocessing, prediction mapping, metric display).
- Useful for chatbot help on consistency between web outputs and final ensemble benchmark.

2. `07_RealTime_Analysis`
- Upload isolated runtime code only if your question is about live camera inference or safety checks.
- Keep this separate from canonical model artifacts.

## Do Not Upload by Default

1. Large binary weights (`.h5`, `.keras`, `.pt`)
- Usually unnecessary for report-writing or code-review support.
- Share file names and paths instead unless the chatbot task explicitly needs weight inspection.

2. Raw dataset images
- Not required for most chatbot tasks and may be large/sensitive.
- Share class counts/split summary instead.

3. Old exploratory logs not used in final Chapter 4 result
- Avoid confusing the chatbot with non-canonical metrics.

## Minimum Safe Package for Ensemble Discussion

If you want a compact upload set, use this minimum package:

1. `Fyp_Report/02_AI_Chatbot_Project_Context.md`
2. `03_Model_Evaluation/Efficientnet base vs Ensemble/` (final artifacts only)
3. Final evaluation scripts from `03_Model_Evaluation`
4. Ensemble-related scripts from `02_Modelling/efficientnetb0_coral/`

This is enough for the chatbot to help with methodology, results, discussion, and consistency checks for the ensemble model.
