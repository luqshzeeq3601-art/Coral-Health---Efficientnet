from __future__ import annotations

import json
import os
from collections import OrderedDict
from pathlib import Path

import cv2
import nbformat as nbf
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential


PROJECT_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_PATH = PROJECT_ROOT / "02_Modelling" / "notebooks" / "coral_reef_health_robust_model.ipynb"
DATASET_DIR = PROJECT_ROOT / "Dataset"
MODEL_DIR = PROJECT_ROOT / "02_Modelling" / "efficientnetb0_coral" / "models"
MODEL_BASE_DIR = PROJECT_ROOT / "02_Modelling" / "efficientnetb0_coral"
OUTPUT_DIR = MODEL_BASE_DIR / "outputs"
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
SEEDS = [42, 43, 44, 45, 46]
IMG_SIZE = 224


def collect_file_paths() -> tuple[list[str], np.ndarray, list[str]]:
    file_paths: list[str] = []
    labels: list[int] = []
    filenames: list[str] = []

    for cls_idx, cls_name in enumerate(CLASS_NAMES):
        cls_dir = DATASET_DIR / cls_name
        for fname in sorted(os.listdir(cls_dir)):
            if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            full_path = cls_dir / fname
            file_paths.append(str(full_path))
            labels.append(cls_idx)
            filenames.append(f"{cls_name}/{fname}")

    return file_paths, np.array(labels), filenames


def reconstruct_split(file_paths: list[str], labels: np.ndarray) -> dict[str, np.ndarray]:
    indices = np.arange(len(file_paths))
    train_idx, temp_idx = train_test_split(
        indices, test_size=0.2, random_state=42, stratify=labels
    )
    temp_labels = labels[temp_idx]
    val_idx, test_idx = train_test_split(
        temp_idx, test_size=0.5, random_state=42, stratify=temp_labels
    )
    return {"train": train_idx, "val": val_idx, "test": test_idx}


def count_by_class(labels: np.ndarray, indices: np.ndarray) -> OrderedDict[str, int]:
    counts: OrderedDict[str, int] = OrderedDict()
    for cls_name in CLASS_NAMES:
        counts[cls_name] = 0
    for idx in indices:
        counts[CLASS_NAMES[int(labels[idx])]] += 1
    return counts


def build_model(weights=None) -> Sequential:
    base_model = EfficientNetB0(
        include_top=False,
        weights=weights,
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    base_model.trainable = True
    for layer in base_model.layers[:-100]:
        layer.trainable = False

    return Sequential(
        [
            Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
            base_model,
            GlobalAveragePooling2D(),
            Dropout(0.4),
            Dense(
                3,
                activation="softmax",
                kernel_regularizer=tf.keras.regularizers.l2(0.0002),
            ),
        ]
    )


def load_images(file_paths: list[str], size: int) -> np.ndarray:
    images = []
    for path in file_paths:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (size, size))
        images.append(img.astype("float32"))
    return np.array(images, dtype="float32")


def load_models() -> list[Sequential]:
    models = []
    for seed in SEEDS:
        model = build_model(weights=None)
        model.load_weights(str(MODEL_DIR / f"efficientnetb0_v4robust_seed{seed}_swa.weights.h5"))
        models.append(model)
    return models


def mean_predict(models: list[Sequential], arrays: list[np.ndarray]) -> np.ndarray:
    per_model = []
    for model in models:
        preds = [model.predict(arr, batch_size=16, verbose=0) for arr in arrays]
        per_model.append(np.mean(preds, axis=0))
    return np.mean(per_model, axis=0)


def fmt_pct(value: float) -> str:
    return f"{value:.2f}%"


def table_from_rows(headers: list[str], rows: list[list[str]]) -> str:
    header_row = "| " + " | ".join(headers) + " |"
    sep_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    data_rows = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_row, sep_row, *data_rows])


def main() -> None:
    file_paths, labels, filenames = collect_file_paths()
    split = reconstruct_split(file_paths, labels)

    totals = count_by_class(labels, np.arange(len(labels)))
    split_counts = OrderedDict(
        (
            (split_name, count_by_class(labels, split_indices))
            for split_name, split_indices in split.items()
        )
    )

    test_files = [file_paths[i] for i in split["test"]]
    test_names = [filenames[i] for i in split["test"]]
    y_true = labels[split["test"]]

    sample_files: OrderedDict[str, str] = OrderedDict()
    for cls_name in CLASS_NAMES:
        for fname in test_names:
            if fname.startswith(f"{cls_name}/"):
                sample_files[cls_name] = fname
                break

    X224 = load_images(test_files, 224)
    X224_flip = np.flip(X224, axis=2).copy()
    X256 = load_images(test_files, 256)
    X256_resized = np.array(
        [cv2.resize(img.astype("uint8"), (224, 224)).astype("float32") for img in X256],
        dtype="float32",
    )
    X256_flip_resized = np.array(
        [
            cv2.resize(np.flip(img, axis=1).astype("uint8"), (224, 224)).astype("float32")
            for img in X256
        ],
        dtype="float32",
    )

    models = load_models()

    protocol_arrays = OrderedDict(
        [
            ("224-only ensemble", [X224]),
            ("224 + horizontal flip", [X224, X224_flip]),
            ("224 + 256 scales", [X224, X256_resized]),
            ("224 + 256 scales + flip", [X224, X224_flip, X256_resized, X256_flip_resized]),
        ]
    )
    protocol_probs = OrderedDict(
        (name, mean_predict(models, arrays)) for name, arrays in protocol_arrays.items()
    )
    protocol_acc = OrderedDict(
        (
            name,
            float((np.argmax(probs, axis=1) == y_true).mean() * 100),
        )
        for name, probs in protocol_probs.items()
    )

    canonical_name = "224-only ensemble"
    canonical_probs = protocol_probs[canonical_name]
    canonical_pred = np.argmax(canonical_probs, axis=1)
    canonical_acc = protocol_acc[canonical_name]
    canonical_report = classification_report(
        y_true, canonical_pred, target_names=CLASS_NAMES, output_dict=True
    )

    wrong_cases = []
    all_cases = []
    for fname, true_idx, pred_idx, probs in zip(test_names, y_true, canonical_pred, canonical_probs):
        confidence = float(np.max(probs) * 100)
        row = {
            "filename": fname,
            "true": CLASS_NAMES[int(true_idx)],
            "pred": CLASS_NAMES[int(pred_idx)],
            "confidence": confidence,
            "correct": int(true_idx) == int(pred_idx),
        }
        all_cases.append(row)
        if not row["correct"]:
            wrong_cases.append(row)

    low_conf_correct = sorted(
        (row for row in all_cases if row["correct"]),
        key=lambda row: row["confidence"],
    )[:5]

    temperature_value = (MODEL_DIR / "temperature.txt").read_text(encoding="utf-8").strip()
    history = json.loads((OUTPUT_DIR / "training_history_ensemble.json").read_text(encoding="utf-8"))
    last_epoch = {
        "train_acc": history["avg_train_acc"][-1] * 100,
        "val_acc": history["avg_val_acc"][-1] * 100,
        "train_loss": history["avg_train_loss"][-1],
        "val_loss": history["avg_val_loss"][-1],
    }

    dataset_table = table_from_rows(
        ["Split", "Healthy", "Bleached", "Dead", "Total"],
        [
            [
                split_name.capitalize(),
                str(counts["Healthy"]),
                str(counts["Bleached"]),
                str(counts["Dead"]),
                str(sum(counts.values())),
            ]
            for split_name, counts in split_counts.items()
        ],
    )

    report_table = table_from_rows(
        ["Class", "Precision", "Recall", "F1-score", "Support"],
        [
            [
                cls_name,
                f"{canonical_report[cls_name]['precision']:.2f}",
                f"{canonical_report[cls_name]['recall']:.2f}",
                f"{canonical_report[cls_name]['f1-score']:.2f}",
                str(int(canonical_report[cls_name]["support"])),
            ]
            for cls_name in CLASS_NAMES
        ],
    )

    protocol_table = table_from_rows(
        ["Protocol", "Accuracy", "Use in notebook"],
        [
            ["224-only ensemble", fmt_pct(protocol_acc["224-only ensemble"]), "Canonical benchmark"],
            ["224 + horizontal flip", fmt_pct(protocol_acc["224 + horizontal flip"]), "Exploratory comparison"],
            ["224 + 256 scales", fmt_pct(protocol_acc["224 + 256 scales"]), "Exploratory comparison"],
            [
                "224 + 256 scales + flip",
                fmt_pct(protocol_acc["224 + 256 scales + flip"]),
                "Exploratory comparison",
            ],
        ],
    )

    wrong_table = table_from_rows(
        ["Filename", "True label", "Predicted label", "Confidence"],
        [
            [
                row["filename"],
                row["true"],
                row["pred"],
                fmt_pct(row["confidence"]),
            ]
            for row in wrong_cases
        ],
    )

    low_conf_table = table_from_rows(
        ["Filename", "True label", "Predicted label", "Confidence"],
        [
            [
                row["filename"],
                row["true"],
                row["pred"],
                fmt_pct(row["confidence"]),
            ]
            for row in low_conf_correct
        ],
    )

    total_rows = [
        [cls_name, str(totals[cls_name]), f"{totals[cls_name] / len(labels) * 100:.1f}%"]
        for cls_name in CLASS_NAMES
    ]
    total_rows.append(["TOTAL", str(len(labels)), "100.0%"])
    dataset_total_table = table_from_rows(["Class", "Count", "% of dataset"], total_rows)

    sample_files_json = json.dumps(sample_files, indent=2)

    title_md = f"""# Coral Reef Health Assessment — Robust Ensemble Model
### EfficientNetB0 Transfer Learning + SWA + Benchmark-Verified Academic Notebook

This notebook is the academic-facing modelling summary for the coral reef health classifier used in this project. It keeps the polished result visuals from the original notebook, but also adds the methodological context, benchmark protocol definition, failure analysis, calibration note, and reproducibility details expected in an FYP review or viva.

| Property | Value |
|---|---|
| Task | 3-class coral health classification (`Healthy`, `Bleached`, `Dead`) |
| Dataset | BHD Coral Dataset from Kaggle, 1,582 underwater reef images |
| Backbone | EfficientNetB0 with ImageNet transfer learning |
| Training strategy | 5-seed robust ensemble with SWA |
| Canonical benchmark | **{fmt_pct(canonical_acc)}** on 159 held-out test images |
| Canonical inference protocol | **224x224 single-scale ensemble averaging** |
| Deployment calibration artifact | Temperature scaling `T = {temperature_value}` learned on the validation set |
"""

    setup_md = "## 1. Project Setup & Imports"

    setup_code = """from pathlib import Path
import json
import os
import warnings

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")


def find_project_root(start: Path) -> Path:
    start = start.resolve()
    candidates = [start, *start.parents]
    for candidate in candidates:
        if (candidate / "Dataset").exists() and (candidate / "02_Modelling").exists():
            return candidate
    raise FileNotFoundError("Could not locate the project root from the current working directory.")


PROJECT_ROOT = find_project_root(Path.cwd())
DATASET_DIR = PROJECT_ROOT / "Dataset"
MODEL_BASE_DIR = PROJECT_ROOT / "02_Modelling" / "efficientnetb0_coral"
MODEL_DIR = MODEL_BASE_DIR / "models"
OUTPUT_DIR = MODEL_BASE_DIR / "outputs"
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
SPLIT_INFO_PATH = MODEL_BASE_DIR / "split_info_v3.json"

print("Project root :", PROJECT_ROOT)
print("Dataset dir  :", DATASET_DIR)
print("Model dir    :", MODEL_DIR)
print("Outputs dir  :", OUTPUT_DIR)
print("split_info_v3.json present?", SPLIT_INFO_PATH.exists())
"""

    dataset_md = f"""---
## 2. Dataset Overview

### Dataset provenance
This project uses the **BHD Coral Dataset** from **Kaggle**, which contains real underwater coral imagery labelled into the three health states required by the project objective: `Healthy`, `Bleached`, and `Dead`.

### Why this dataset is appropriate
- It directly matches the problem definition of coral health assessment.
- It includes realistic underwater imaging conditions such as colour cast, blur, lighting variation, and background clutter.
- It provides enough labelled images to support transfer learning and controlled evaluation while still exposing class imbalance, especially for the `Dead` class.

### Full dataset distribution
{dataset_total_table}

### Train / validation / test split used in this notebook
The repo snapshot used for this refresh does **not** currently contain `split_info_v3.json`, so the notebook reconstructs the same deterministic split logic used in `train_v4_robust.py`:

- `train_test_split(..., test_size=0.2, random_state=42, stratify=labels)`
- `train_test_split(..., test_size=0.5, random_state=42, stratify=temp_labels)` for validation vs test

This reproduces the following split counts:

{dataset_table}
"""

    dataset_code = """def collect_file_paths(dataset_dir: Path, class_names):
    file_paths, labels, filenames = [], [], []
    for cls_idx, cls_name in enumerate(class_names):
        cls_dir = dataset_dir / cls_name
        for fname in sorted(os.listdir(cls_dir)):
            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                file_paths.append(str(cls_dir / fname))
                labels.append(cls_idx)
                filenames.append(f"{cls_name}/{fname}")
    return file_paths, np.array(labels), filenames


def reconstruct_split(file_paths, labels):
    indices = np.arange(len(file_paths))
    train_idx, temp_idx = train_test_split(
        indices, test_size=0.2, random_state=42, stratify=labels
    )
    temp_labels = labels[temp_idx]
    val_idx, test_idx = train_test_split(
        temp_idx, test_size=0.5, random_state=42, stratify=temp_labels
    )
    return {"train": train_idx, "val": val_idx, "test": test_idx}


file_paths, labels, filenames = collect_file_paths(DATASET_DIR, CLASS_NAMES)
split = reconstruct_split(file_paths, labels)

totals = pd.DataFrame(
    {
        "Class": CLASS_NAMES,
        "Count": [int(np.sum(labels == idx)) for idx in range(len(CLASS_NAMES))],
    }
)
totals["% of dataset"] = (totals["Count"] / totals["Count"].sum() * 100).round(1)
display(totals)

split_rows = []
for split_name, split_idx in split.items():
    split_rows.append(
        {
            "Split": split_name.capitalize(),
            "Healthy": int(np.sum(labels[split_idx] == 0)),
            "Bleached": int(np.sum(labels[split_idx] == 1)),
            "Dead": int(np.sum(labels[split_idx] == 2)),
            "Total": int(len(split_idx)),
        }
    )
split_df = pd.DataFrame(split_rows)
display(split_df)

fig, ax = plt.subplots(figsize=(7, 4))
colors = ["#2ecc71", "#f39c12", "#e74c3c"]
bars = ax.bar(totals["Class"], totals["Count"], color=colors, edgecolor="white", linewidth=1.5)
for bar, count in zip(bars, totals["Count"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5, str(count), ha="center", va="bottom", fontweight="bold")
ax.set_title("Dataset Class Distribution", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Number of Images")
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
"""

    sample_md = """### Example coral images from the deterministic test split
These are representative examples included so examiners can immediately see the visual distinction between the three target classes before reading the performance metrics."""

    sample_code = f"""sample_files = {sample_files_json}

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
for ax, cls_name in zip(axes, CLASS_NAMES):
    rel_path = sample_files[cls_name]
    img = mpimg.imread(DATASET_DIR / rel_path)
    ax.imshow(img)
    ax.set_title(f"{{cls_name}}\\n{{rel_path}}", fontsize=11, fontweight="bold")
    ax.axis("off")
plt.suptitle("Representative Test Images by Class", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
"""

    model_md = """---
## 3. Model Selection & Architecture

### Why EfficientNetB0?
- It provides a strong accuracy-to-parameter-efficiency trade-off for an FYP-scale image classification task.
- It is small enough for practical retraining and web deployment, yet strong enough to benefit from transfer learning.
- It reduces the risk of overfitting compared with heavier backbones on a moderately sized dataset.
- It integrates cleanly with Grad-CAM and ensemble-style evaluation.

### Final architecture used in the robust model

```text
Input (224x224x3)
       |
EfficientNetB0 backbone (ImageNet pre-trained)
  Layers 0 to -100 : frozen
  Last 100 layers  : fine-tuned
       |
GlobalAveragePooling2D
       |
Dropout(0.4)
       |
Dense(3, softmax) + L2(0.0002)
       |
Output: [P(Healthy), P(Bleached), P(Dead)]
```

### Canonical training hyperparameters
| Hyperparameter | Value |
|---|---|
| Image size | 224 x 224 |
| Epochs | 30 |
| Batch size | 16 |
| Initial learning rate | `8e-5` |
| LR schedule | Cosine decay |
| Label smoothing | `0.05` |
| Dropout | `0.4` |
| L2 regularization | `0.0002` |
| Ensemble seeds | `[42, 43, 44, 45, 46]` |
| Optimizer | Adam |
"""

    model_code = """import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential

IMG_SIZE = 224


def build_model(weights="imagenet"):
    base_model = EfficientNetB0(include_top=False, weights=weights, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = True
    for layer in base_model.layers[:-100]:
        layer.trainable = False
    model = Sequential(
        [
            Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
            base_model,
            GlobalAveragePooling2D(),
            Dropout(0.4),
            Dense(3, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.0002)),
        ]
    )
    return model


model = build_model(weights="imagenet")
trainable_params = sum(int(np.prod(w.shape)) for w in model.trainable_weights)
frozen_params = sum(int(np.prod(w.shape)) for w in model.non_trainable_weights)
print(f"Trainable params : {trainable_params:,}")
print(f"Frozen params    : {frozen_params:,}")
print(f"Total params     : {trainable_params + frozen_params:,}")
model.summary()
"""

    strategy_md = """---
## 4. Training Strategy & Hyperparameter Optimisation

### Robust training techniques actually used
| Technique | Purpose | Final configuration |
|---|---|---|
| 5-seed ensemble | Reduce variance across runs | Seeds `42-46` |
| SWA | Flatter minima and more stable checkpoints | Last 5 epochs averaged |
| Mixup | Reduce over-confidence | `alpha = 0.1` |
| Hard-example oversampling | Emphasise known difficult images | `x20` baseline, `Dead` promoted to `x30` |
| Cosine decay | Smooth learning-rate annealing | `8e-5 -> 0` over 30 epochs |
| Colour / brightness augmentation | Improve underwater robustness | brightness range `[0.8, 1.2]` |
| Label smoothing | Better calibration during training | `0.05` |

### Known hard examples carried forward from earlier runs
The robust pipeline explicitly oversamples images that had been repeatedly misclassified in previous versions. This is academically important because it shows the model was improved through targeted error analysis, not just by reporting a final score.

| Class | Hard-example count |
|---|---|
| Healthy | 2 |
| Bleached | 29 |
| Dead | 15 |

### Before-vs-after optimisation summary
| Parameter | Earlier version | Robust version | Why it changed |
|---|---|---|---|
| Dropout | `0.7` | `0.4` | Reduced underfitting and fixed inverted-looking learning curves |
| L2 regularisation | `0.0005` | `0.0002` | Less aggressive weight penalty |
| Label smoothing | `0.1` | `0.05` | Allowed cleaner confidence growth |
| Initial LR | `5e-5` | `8e-5` | Faster convergence |
| Rotation range | `40°` | `20°` | Fewer border artefacts |
| Vertical flip | `True` | `False` | Coral should not appear upside-down |
| Zoom range | `0.3` | `0.15` | Reduced unrealistic distortion |
| Mixup alpha | `0.2` | `0.1` | Less aggressive blending |
| Dead oversampling | `20x` | `30x` | Improved minority-class reliability |
"""

    training_md = f"""---
## 5. Training Evidence

### Training execution snapshot
The notebook now keeps a single authoritative training-log section instead of the previous duplicated block. The robust run trains `5` seeds using `train_v4_robust.py` and stores the aggregated history in `training_history_ensemble.json`.

Final aggregated epoch values from the stored history:

| Metric | Value |
|---|---|
| Final train accuracy | `{last_epoch["train_acc"]:.2f}%` |
| Final validation accuracy | `{last_epoch["val_acc"]:.2f}%` |
| Final train loss | `{last_epoch["train_loss"]:.4f}` |
| Final validation loss | `{last_epoch["val_loss"]:.4f}` |

### Training history
![Training History](../efficientnetb0_coral/outputs/training_history_ensemble.png)

**Observations**
- Training and validation curves converge smoothly without the unstable pattern seen in earlier versions.
- Validation accuracy remains slightly above training accuracy in parts of the run, which is reasonable here because training-time augmentation and Mixup make the training task harder.
- The final gap is small, which supports the claim that the model is regularised rather than memorising.
"""

    eval_md = f"""---
## 6. Canonical Evaluation Results

### Canonical benchmark definition
The headline number reported in this notebook is the **{fmt_pct(canonical_acc)} canonical benchmark**, defined as:

- 5-seed SWA ensemble
- held-out deterministic 159-image test set
- **224x224 single-scale inference**
- no protocol mixing with flip-only or multi-scale alternatives

This choice keeps the academic narrative consistent with the stored classification report and confusion-matrix artefacts already present in the repo.

### Classification report
{report_table}

| Overall metric | Value |
|---|---|
| Accuracy | **{fmt_pct(canonical_acc)}** |
| Weighted precision | `{canonical_report["weighted avg"]["precision"]:.2f}` |
| Weighted recall | `{canonical_report["weighted avg"]["recall"]:.2f}` |
| Weighted F1-score | `{canonical_report["weighted avg"]["f1-score"]:.2f}` |
| Total test samples | `159` |

### Confusion matrix
![Confusion Matrix](../efficientnetb0_coral/outputs/confusion_matrix_ensemble.png)

**Observations**
- `Healthy` achieves perfect recall (`72/72`).
- `Bleached` is strong overall, but two cases still drift toward `Healthy`.
- `Dead` remains the hardest class in recall because it has the smallest support and one sample still flips to `Bleached`.
"""

    protocol_md = f"""---
## 7. Evaluation Protocol Comparison

One major weakness in the original notebook was that multiple accuracy numbers were quoted across the repo without clearly stating the evaluation protocol. Re-running the current checkpoints shows that the metric changes depending on the inference setup:

{protocol_table}

### Interpretation
- **98.11%** is the academic benchmark used in this notebook because it is the cleanest one-to-one match for the stored report and confusion matrix.
- **98.74%** appears when adding only horizontal-flip ensembling at 224px. This is a valid exploratory result, but it should not replace the canonical number unless every linked artefact is regenerated under that protocol.
- **97.48%** appears whenever the current repo snapshot includes the 256px branch. That means earlier "multi-scale TTA" claims were overstated for the checkpoints currently stored in this workspace.
"""

    calibration_md = f"""---
## 8. Calibration & Confidence Handling

The repo includes a saved temperature-scaling artifact:

| Item | Value |
|---|---|
| File | `02_Modelling/efficientnetb0_coral/models/temperature.txt` |
| Temperature | `{temperature_value}` |
| Calibration set | Validation split only |
| Purpose | Improve probability calibration for deployment confidence outputs |

### Why this matters academically
- Calibration is different from accuracy optimisation.
- A classifier can be accurate but poorly calibrated, especially when softmax probabilities are over-confident.
- This project therefore separates the **headline accuracy benchmark** from the **deployment confidence-calibration step**.

### Practical interpretation
For the written report and viva, the safest statement is:

> The model achieves **{fmt_pct(canonical_acc)}** held-out test accuracy under the canonical 224px ensemble benchmark, while temperature scaling (`T = {temperature_value}`) is retained as a deployment-side method for improving probability reliability.
"""

    failure_md = f"""---
## 9. Failure Analysis

### Misclassified test images under the canonical benchmark
{wrong_table}

### Lowest-confidence correct predictions
{low_conf_table}

### What these errors suggest
- Two errors are `Bleached -> Healthy`, which indicates some borderline bleached cases still resemble normal coral texture and colour strongly enough to confuse the ensemble.
- The remaining error is `Dead -> Bleached`, which is consistent with the ecological reality that severe bleaching and dead coral can share pale, low-texture regions.
- The `Dead` class is still the most fragile class because it is also the smallest class in the entire dataset (`150 / 1,582` images).
"""

    xai_md = """---
## 10. Explainability via Grad-CAM

![Grad-CAM Outputs](../efficientnetb0_coral/outputs/gradcam_outputs.png)

### Why Grad-CAM is included
Grad-CAM gives the project an explainability layer that is especially useful in an FYP defence, because it allows the examiner to ask not only whether the model is correct, but **what image regions drove the prediction**.

### Interpretation
- `Healthy`: attention concentrates on textured live coral tissue rather than just background water.
- `Bleached`: activations emphasise the pale, discoloured regions characteristic of bleaching.
- `Dead`: the model focuses on structurally degraded and algae-dominated regions.

These examples are correctly classified representative samples, so they should be presented as **supporting evidence of interpretability**, not as proof that the model never fails.
"""

    artifacts_md = """---
## 11. Saved Model Files
The deployment artefacts below are useful to mention during the viva because they show the project is not just a one-off notebook result, but a packaged modelling pipeline with saved checkpoints and deployment assets."""

    artifact_code = """if MODEL_DIR.exists():
    model_files = sorted(
        fname for fname in os.listdir(MODEL_DIR)
        if (MODEL_DIR / fname).is_file()
        and fname.lower() not in {"desktop.ini", "readme.md"}
        and fname.endswith((".h5", ".txt", ".npy"))
    )

    rows = []
    for fname in model_files:
        path = MODEL_DIR / fname
        rows.append(
            {
                "Filename": fname,
                "Size (MB)": round(path.stat().st_size / (1024 ** 2), 2),
            }
        )
    display(pd.DataFrame(rows))
else:
    print("Model directory not found:", MODEL_DIR)
"""

    final_md = f"""---
## 12. Reproducibility, Limitations, and Final Takeaways

### Reproducibility details
| Item | Value |
|---|---|
| Python | `3.10.11` |
| Core framework | TensorFlow / Keras |
| Supporting libraries | scikit-learn, OpenCV, NumPy, Pandas, Matplotlib, Seaborn |
| Hardware used in the project | NVIDIA RTX 3070 |
| Random seed for split | `42` |
| Ensemble seeds | `{SEEDS}` |
| Epochs / batch size | `30` / `16` |
| Stored training history | `training_history_ensemble.json` |

### Key limitations
- The dataset comes from a single named source, so external generalisation is still unproven.
- The `Dead` class is much smaller than the other two classes, which limits recall robustness.
- The current workspace snapshot is missing `split_info_v3.json`, so deterministic reconstruction is required for exact split reporting.
- Different inference protocols can yield different headline metrics, so protocol definitions must always be reported alongside accuracy.

### Sensible future work
- Evaluate on an external coral dataset or field-collected images from a different site.
- Report calibration-specific metrics such as ECE or Brier score in addition to accuracy.
- Compare EfficientNetB0 against at least one stronger and one lighter backbone under the same split.
- Expand minority-class coverage for `Dead` coral.
- Add longitudinal or site-level validation if the project moves toward operational reef monitoring.

### Final conclusion
The modelling work is now documented at a much stronger FYP standard: the notebook states the dataset source and split clearly, uses the correct final hyperparameters, explains why EfficientNetB0 was chosen, defines a single canonical benchmark (**{fmt_pct(canonical_acc)}**), documents alternative protocols instead of mixing them, and includes explicit failure analysis, calibration context, limitations, and future work.
"""

    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
        "language_info": {
            "name": "python",
            "version": "3.10.11",
            "mimetype": "text/x-python",
            "codemirror_mode": {"name": "ipython", "version": 3},
            "pygments_lexer": "ipython3",
            "nbconvert_exporter": "python",
            "file_extension": ".py",
        },
    }
    nb.cells = [
        nbf.v4.new_markdown_cell(title_md),
        nbf.v4.new_markdown_cell(setup_md),
        nbf.v4.new_code_cell(setup_code),
        nbf.v4.new_markdown_cell(dataset_md),
        nbf.v4.new_code_cell(dataset_code),
        nbf.v4.new_markdown_cell(sample_md),
        nbf.v4.new_code_cell(sample_code),
        nbf.v4.new_markdown_cell(model_md),
        nbf.v4.new_code_cell(model_code),
        nbf.v4.new_markdown_cell(strategy_md),
        nbf.v4.new_markdown_cell(training_md),
        nbf.v4.new_markdown_cell(eval_md),
        nbf.v4.new_markdown_cell(protocol_md),
        nbf.v4.new_markdown_cell(calibration_md),
        nbf.v4.new_markdown_cell(failure_md),
        nbf.v4.new_markdown_cell(xai_md),
        nbf.v4.new_markdown_cell(artifacts_md),
        nbf.v4.new_code_cell(artifact_code),
        nbf.v4.new_markdown_cell(final_md),
    ]

    NOTEBOOK_PATH.write_text(nbf.writes(nb), encoding="utf-8")
    print(f"Notebook refreshed: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
