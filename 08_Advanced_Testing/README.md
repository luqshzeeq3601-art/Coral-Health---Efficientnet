# 08_Advanced_Testing

Advanced evaluation suite for the **EfficientNetB0 V4 Robust** coral health classifier.

---

## Folder Structure

```
08_Advanced_Testing/
├── run_all_tests.py                      ← Master launcher (run this first)
│
├── 01_stratified_kfold/
│   ├── run_kfold.py
│   └── outputs/
│       ├── kfold_results.json
│       ├── kfold_report.txt
│       └── kfold_accuracy_plot.png
│
├── 02_robustness_testing/
│   ├── run_robustness.py
│   └── outputs/
│       ├── robustness_results.json
│       ├── robustness_report.txt
│       └── robustness_bar_chart.png
│
└── 03_calibration_analysis/
    ├── run_calibration.py
    └── outputs/
        ├── calibration_results.json
        ├── calibration_report.txt
        └── reliability_diagram.png
```

---

## How to Run

### Option A — Run all tests at once
```powershell
cd c:\Users\ZeeqRyz\Desktop\BASEPROJECT\08_Advanced_Testing
..\.venv\Scripts\python.exe run_all_tests.py
```

### Option B — Run individual tests
```powershell
# K-Fold
..\.venv\Scripts\python.exe 01_stratified_kfold\run_kfold.py

# Robustness
..\.venv\Scripts\python.exe 02_robustness_testing\run_robustness.py

# Calibration
..\.venv\Scripts\python.exe 03_calibration_analysis\run_calibration.py
```

---

## What Each Test Does

### 1. Stratified K-Fold Cross-Validation
- Runs 5-fold stratified CV on the full dataset
- Preserves class ratios in each fold (critical for imbalanced Dead class)
- Reports: mean accuracy ± std dev across folds
- **Purpose**: Proves 98.11% is reliable, not a lucky split

### 2. Robustness Testing
Tests model under 9 realistic underwater imaging degradations:

| Corruption | Simulates |
|---|---|
| Gaussian Noise σ=15/30 | Camera sensor noise |
| Motion Blur k=11 | Camera shake / diver movement |
| JPEG Q=25/10 | Lossy image transmission |
| Brightness 50%/150% | Depth-based lighting changes |
| Color Jitter | Water turbidity / white balance |

**Purpose**: Validates real-world deployment readiness

### 3. Confidence Calibration Analysis
- Computes ECE (Expected Calibration Error) and MCE
- Plots reliability diagram (predicted confidence vs actual accuracy)
- Plots confidence histogram (correct vs wrong predictions)
- **Purpose**: Academic depth — verifies model knows when it doesn't know

---

## Prerequisites
All models must be trained. Required files in `02_Modelling/efficientnetb0_coral/models/`:
- `efficientnetb0_v4robust_seed42_swa.weights.h5`
- `efficientnetb0_v4robust_seed43_swa.weights.h5`
- `efficientnetb0_v4robust_seed44_swa.weights.h5`
- `efficientnetb0_v4robust_seed45_swa.weights.h5`
- `efficientnetb0_v4robust_seed46_swa.weights.h5`
