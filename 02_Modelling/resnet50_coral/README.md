# ResNet50 Coral Robust Model

This folder is a separate experiment for training a ResNet50 robust single model
against the same coral-health dataset and split used by the current
EfficientNetB0 robust ensemble.

## Purpose

The current benchmark is the 5-seed EfficientNetB0 robust ensemble. ResNet50 is
trained here as a larger single-model comparison:

| Model | Parameter Count |
|---|---:|
| EfficientNetB0 single model | ~4.05M |
| EfficientNetB0 5-seed ensemble | ~20.27M total |
| ResNet50 single model | ~23.59M |

## Training Setup

- Architecture: `ResNet50(include_top=False, weights="imagenet")`
- Input size: `224 x 224`
- Seed: `42`
- Epochs: `30`
- Batch size: `8`
- Label smoothing: `0.05`
- Initial learning rate: `8e-5`
- SWA: last `5` epochs
- Split: `05_Baseline_Model/split_info_v3.json`
- Dataset: `Dataset/`

The script keeps all generated files inside this folder and does not write into
the existing EfficientNetB0 model directory.

## GPU Temperature Control

`train_resnet50_robust.py` uses `nvidia-smi` through a Keras callback:

- Max temperature: `80C`
- Resume temperature: `70C`
- Cooldown interval: `30s`
- Log file: `outputs/gpu_temperature_log.csv`

The script only pauses training when needed. It does not change system-level GPU
settings, fan curves, clocks, or power limits.

## Run

From the project root:

```powershell
.venv\Scripts\python.exe 02_Modelling\resnet50_coral\train_resnet50_robust.py
```

## Expected Outputs

- `models/resnet50_robust_seed42.weights.h5`
- `models/resnet50_robust_seed42_swa.weights.h5`
- `outputs/classification_report_resnet50.txt`
- `outputs/confusion_matrix_resnet50.png`
- `outputs/confusion_matrix_resnet50.json`
- `outputs/training_history_resnet50.png`
- `outputs/training_history_resnet50.json`
- `outputs/gpu_temperature_log.csv`
- `outputs/run_summary_resnet50.json`
