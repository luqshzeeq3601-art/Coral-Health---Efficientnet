# ConvNeXtTiny Coral Robust Model

This folder is a separate experiment for training a ConvNeXtTiny robust single
model against the same coral-health dataset and canonical split used by the
current EfficientNetB0 robust ensemble and ResNet50 comparison.

## Purpose

ConvNeXtTiny is trained here as a modern single-model comparison. This run is
kept separate from the existing model folders so generated checkpoints, plots,
reports, and GPU logs do not overwrite other experiments.

| Model | Parameter Count |
|---|---:|
| EfficientNetB0 single model | ~4.05M |
| EfficientNetB0 5-seed ensemble | ~20.27M total |
| ResNet50 single model | ~23.59M |
| ConvNeXtTiny single model | ~27.82M |

## Training Setup

- Architecture: `ConvNeXtTiny(include_top=False, include_preprocessing=True, weights="imagenet")`
- Input size: `224 x 224`
- Input range: raw RGB `0-255`
- Seed: `42`
- Epochs: `30`
- Batch size: `6`
- Label smoothing: `0.05`
- Initial learning rate: `5e-5`
- SWA: last `5` epochs
- Trainable backbone scope: final ConvNeXt stage plus final normalization layer
- Split: `05_Baseline_Model/split_info_v3.json`
- Dataset: `Dataset/`

The script keeps all generated files inside this folder and does not write into
the existing EfficientNetB0 or ResNet50 model directories.

## GPU Temperature Control

`train_convnexttiny_robust.py` uses `nvidia-smi` through a Keras callback:

- Max temperature: `78C`
- Resume temperature: `68C`
- Cooldown interval: `45s`
- Batch check interval: every `10` training batches
- Log file: `outputs/gpu_temperature_log.csv`

The script only pauses training when needed. It does not change system-level GPU
settings, fan curves, clocks, or power limits.

## Run

From the project root:

```powershell
.venv\Scripts\python.exe 02_Modelling\convnexttiny_coral\train_convnexttiny_robust.py
```

## Expected Outputs

- `models/convnexttiny_robust_seed42.weights.h5`
- `models/convnexttiny_robust_seed42_swa.weights.h5`
- `outputs/classification_report_convnexttiny.txt`
- `outputs/confusion_matrix_convnexttiny.png`
- `outputs/confusion_matrix_convnexttiny.json`
- `outputs/training_history_convnexttiny.png`
- `outputs/training_history_convnexttiny.json`
- `outputs/gpu_temperature_log.csv`
- `outputs/run_summary_convnexttiny.json`
