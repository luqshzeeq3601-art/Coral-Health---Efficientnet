# XAI Decision Comparison

This folder creates a defence-ready evidence pack for comparing:

- Baseline EffNetB0
- V4 Robust EffNetB0 ensemble

The generated panels show the model decision with and without Grad-CAM evidence. Grad-CAM is not a separate model and does not change the prediction. It is an explainability layer that shows which image regions supported the predicted coral-health class.

## Run

From the project root:

```powershell
python 06_XAI_Decision_Comparison\generate_xai_comparison.py
```

The script uses:

- `05_Baseline_Model/models/efficientnetb0_baseline.weights.h5`
- `02_Modelling/efficientnetb0_coral/models/efficientnetb0_v4robust_seed{42..46}_swa.h5`
- `05_Baseline_Model/split_info_v3.json`
- `Dataset/`

## Outputs

Generated files are written to `06_XAI_Decision_Comparison/outputs/`:

- `panels/*.png`: one four-panel visual per selected coral image.
- `xai_decision_contact_sheet.png`: combined overview for slides or thesis use.
- `xai_decision_results.csv`: predictions, confidence values, correctness, and panel filenames.
- `xai_decision_summary.md`: short interpretation notes for explaining the XAI evidence.

Each panel contains:

1. Baseline prediction only
2. Baseline Grad-CAM evidence
3. V4 Robust EffNetB0 prediction only
4. V4 Robust EffNetB0 Grad-CAM evidence

## Interpretation

Use the output to explain how the model made its decision on coral images:

- The prediction-only view answers what class the model chose.
- The Grad-CAM view helps inspect where the model looked.
- A good explanation focuses on whether highlighted regions align with coral tissue, bleaching areas, dead coral texture, or irrelevant background.

Do not claim that Grad-CAM improves accuracy. It supports explainability and trust analysis after the model has already produced a prediction.

## Optional Arguments

```powershell
python 06_XAI_Decision_Comparison\generate_xai_comparison.py --uncertain-threshold 75 --max-challenges 3
```

- `--uncertain-threshold`: confidence percentage used when selecting uncertain current-model examples.
- `--max-challenges`: number of challenging examples to add after the three class representatives.
