import csv
import json
import math
import re
import shutil
from pathlib import Path

import matplotlib
import numpy as np
from PIL import Image

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "03_Model_Evaluation" / "Efficientnet base vs Ensemble"

HISTORY_PATH = (
    PROJECT_ROOT
    / "03_Model_Evaluation"
    / "01_EfficientNetB0_Evaluation"
    / "training_history_ensemble.json"
)
CONFUSION_PATH = (
    PROJECT_ROOT
    / "03_Model_Evaluation"
    / "01_EfficientNetB0_Evaluation"
    / "confusion_matrix_ensemble.json"
)
BASELINE_SUMMARY_PATH = PROJECT_ROOT / "05_Baseline_Model" / "outputs" / "baseline_model" / "eval_summary.json"
COMPARISON_SUMMARY_PATH = PROJECT_ROOT / "05_Baseline_Model" / "outputs" / "comparison" / "comparison_summary.txt"
XAI_RESULTS_PATH = PROJECT_ROOT / "06_XAI_Decision_Comparison" / "outputs" / "xai_decision_results.csv"
WRONG_PANEL_PATH = (
    PROJECT_ROOT
    / "06_XAI_Decision_Comparison"
    / "outputs"
    / "panels"
    / "06_current_wrong_Bleached_492.png"
)
DATASET_WRONG_PATH = PROJECT_ROOT / "Dataset" / "Bleached" / "492.png"

CLASS_GRADCAM_PATHS = {
    "Healthy": PROJECT_ROOT
    / "03_Model_Evaluation"
    / "01_EfficientNetB0_Evaluation"
    / "gradcam_all"
    / "Healthy"
    / "CORRECT_93_conf96.png",
    "Bleached": PROJECT_ROOT
    / "03_Model_Evaluation"
    / "01_EfficientNetB0_Evaluation"
    / "gradcam_all"
    / "Bleached"
    / "CORRECT_104_conf99.png",
    "Dead": PROJECT_ROOT
    / "03_Model_Evaluation"
    / "01_EfficientNetB0_Evaluation"
    / "gradcam_all"
    / "Dead"
    / "CORRECT_29_conf99.png",
}

CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
FINAL_MODEL = "Final Model"
BASELINE_MODEL = "Baseline Model"
FINAL_ARCHITECTURE = "EfficientNetB0"
INPUT_SIZE = "224 x 224"
FINAL_ACCURACY = 0.9811320754716981
TEST_SAMPLES = 159
TOTAL_ERRORS = 3

COLORS = {
    "train": "#1f77b4",
    "validation": "#d62728",
    "gap": "#2c7fb8",
    "gap_loss": "#7b3294",
    "final": "#2c7fb8",
    "baseline": "#7f7f7f",
    "grid": "#d9d9d9",
    "header": "#eaf2f8",
    "border": "#4d4d4d",
}


def assert_output_dir_is_safe() -> None:
    resolved_output = OUTPUT_DIR.resolve()
    resolved_root = PROJECT_ROOT.resolve()
    resolved_output.relative_to(resolved_root)
    expected = Path("03_Model_Evaluation") / "Efficientnet base vs Ensemble"
    if OUTPUT_DIR.relative_to(PROJECT_ROOT) != expected:
        raise RuntimeError(f"Refusing to clear unexpected output directory: {OUTPUT_DIR}")


def clear_output_dir() -> None:
    assert_output_dir_is_safe()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for child in OUTPUT_DIR.iterdir():
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def pct(value: float, decimals: int = 2) -> str:
    return f"{value * 100:.{decimals}f}%"


def setup_axes(ax, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_title(title, fontsize=15, weight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, axis="y", color=COLORS["grid"], linewidth=0.8, alpha=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#777777")
    ax.spines["bottom"].set_color("#777777")
    ax.tick_params(labelsize=10)


def save_figure(fig, path: Path) -> None:
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_training_curves(history: dict) -> None:
    epochs = np.arange(1, len(history["avg_train_acc"]) + 1)
    train_acc = np.array(history["avg_train_acc"]) * 100
    val_acc = np.array(history["avg_val_acc"]) * 100
    train_loss = np.array(history["avg_train_loss"])
    val_loss = np.array(history["avg_val_loss"])

    fig, ax = plt.subplots(figsize=(8.2, 5.0), facecolor="white")
    ax.plot(epochs, train_acc, color=COLORS["train"], linewidth=2.2, label="Training")
    ax.plot(epochs, val_acc, color=COLORS["validation"], linewidth=2.2, label="Validation")
    setup_axes(ax, "Training and Validation Accuracy", "Epoch", "Accuracy (%)")
    ax.set_xlim(1, epochs[-1])
    ax.set_ylim(max(55, math.floor(train_acc.min() / 5) * 5), 100)
    ax.legend(frameon=False, loc="lower right", fontsize=10)
    save_figure(fig, OUTPUT_DIR / "01_training_validation_accuracy.png")

    fig, ax = plt.subplots(figsize=(8.2, 5.0), facecolor="white")
    ax.plot(epochs, train_loss, color=COLORS["train"], linewidth=2.2, label="Training")
    ax.plot(epochs, val_loss, color=COLORS["validation"], linewidth=2.2, label="Validation")
    setup_axes(ax, "Training and Validation Loss", "Epoch", "Loss")
    ax.set_xlim(1, epochs[-1])
    ax.set_ylim(0, max(train_loss.max(), val_loss.max()) * 1.08)
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    save_figure(fig, OUTPUT_DIR / "02_training_validation_loss.png")

    accuracy_gap = train_acc - val_acc
    loss_gap = train_loss - val_loss

    fig, ax = plt.subplots(figsize=(8.2, 4.6), facecolor="white")
    ax.axhline(0, color="#333333", linewidth=1.1)
    ax.plot(epochs, accuracy_gap, color=COLORS["gap"], linewidth=2.2)
    setup_axes(ax, "Accuracy Gap per Epoch", "Epoch", "Training - Validation (percentage points)")
    ax.set_xlim(1, epochs[-1])
    limit = max(abs(float(accuracy_gap.min())), abs(float(accuracy_gap.max())))
    ax.set_ylim(-limit * 1.18, limit * 1.18)
    save_figure(fig, OUTPUT_DIR / "03_accuracy_gap_per_epoch.png")

    fig, ax = plt.subplots(figsize=(8.2, 4.6), facecolor="white")
    ax.axhline(0, color="#333333", linewidth=1.1)
    ax.plot(epochs, loss_gap, color=COLORS["gap_loss"], linewidth=2.2)
    setup_axes(ax, "Loss Gap per Epoch", "Epoch", "Training Loss - Validation Loss")
    ax.set_xlim(1, epochs[-1])
    upper = max(abs(float(loss_gap.min())), abs(float(loss_gap.max()))) * 1.18
    ax.set_ylim(-upper, upper)
    save_figure(fig, OUTPUT_DIR / "04_loss_gap_per_epoch.png")

    with (OUTPUT_DIR / "03_train_validation_gap_values.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "epoch",
                "training_accuracy",
                "validation_accuracy",
                "accuracy_gap_percentage_points",
                "training_loss",
                "validation_loss",
                "loss_gap",
            ]
        )
        for i, epoch in enumerate(epochs):
            writer.writerow(
                [
                    int(epoch),
                    f"{train_acc[i] / 100:.6f}",
                    f"{val_acc[i] / 100:.6f}",
                    f"{accuracy_gap[i]:.4f}",
                    f"{train_loss[i]:.6f}",
                    f"{val_loss[i]:.6f}",
                    f"{loss_gap[i]:.6f}",
                ]
            )


def compute_report(cm: np.ndarray) -> list[dict]:
    total = int(cm.sum())
    correct = int(np.trace(cm))
    rows = []
    for idx, label in enumerate(CLASS_NAMES):
        tp = float(cm[idx, idx])
        predicted = float(cm[:, idx].sum())
        actual = float(cm[idx, :].sum())
        precision = tp / predicted if predicted else 0.0
        recall = tp / actual if actual else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        rows.append(
            {
                "class": label,
                "precision": precision,
                "recall": recall,
                "f1_score": f1,
                "support": int(actual),
            }
        )

    accuracy = correct / total
    macro = {
        "class": "Macro Avg",
        "precision": float(np.mean([row["precision"] for row in rows])),
        "recall": float(np.mean([row["recall"] for row in rows])),
        "f1_score": float(np.mean([row["f1_score"] for row in rows])),
        "support": total,
    }
    weighted = {
        "class": "Weighted Avg",
        "precision": float(
            sum(row["precision"] * row["support"] for row in rows) / total
        ),
        "recall": float(sum(row["recall"] * row["support"] for row in rows) / total),
        "f1_score": float(sum(row["f1_score"] * row["support"] for row in rows) / total),
        "support": total,
    }
    rows.append({"class": "Accuracy", "precision": None, "recall": None, "f1_score": accuracy, "support": total})
    rows.append(macro)
    rows.append(weighted)
    return rows


def write_classification_report(report_rows: list[dict]) -> None:
    with (OUTPUT_DIR / "06_final_classification_report.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["class", "precision", "recall", "f1_score", "support"])
        for row in report_rows:
            writer.writerow(
                [
                    row["class"],
                    "" if row["precision"] is None else f"{row['precision']:.4f}",
                    "" if row["recall"] is None else f"{row['recall']:.4f}",
                    f"{row['f1_score']:.4f}",
                    row["support"],
                ]
            )

    table_rows = []
    for row in report_rows:
        table_rows.append(
            [
                row["class"],
                "" if row["precision"] is None else pct(row["precision"], 2),
                "" if row["recall"] is None else pct(row["recall"], 2),
                pct(row["f1_score"], 2),
                f"{row['support']}",
            ]
        )
    render_table_image(
        title="Final Classification Report",
        columns=["Class", "Precision", "Recall", "F1-score", "Support"],
        rows=table_rows,
        output_path=OUTPUT_DIR / "06_final_classification_report_table.png",
        figsize=(7.6, 3.4),
        font_size=8.6,
        col_widths=[0.22, 0.20, 0.20, 0.20, 0.18],
        title_font_size=12.0,
    )


def plot_confusion_matrix(cm: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.8), facecolor="white")
    im = ax.imshow(cm, cmap="Blues", vmin=0)
    ax.set_title("Final Confusion Matrix", fontsize=15, weight="bold", pad=12)
    ax.set_xlabel("Predicted Class", fontsize=11)
    ax.set_ylabel("True Class", fontsize=11)
    ax.set_xticks(np.arange(len(CLASS_NAMES)), labels=CLASS_NAMES)
    ax.set_yticks(np.arange(len(CLASS_NAMES)), labels=CLASS_NAMES)
    ax.tick_params(labelsize=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks(np.arange(-0.5, len(CLASS_NAMES), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(CLASS_NAMES), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    threshold = cm.max() / 2
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            color = "white" if cm[i, j] > threshold else "#222222"
            ax.text(j, i, f"{cm[i, j]}", ha="center", va="center", color=color, fontsize=13, weight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.set_ylabel("Samples", rotation=270, labelpad=15)
    save_figure(fig, OUTPUT_DIR / "05_final_confusion_matrix.png")


def render_table_image(
    title: str,
    columns: list[str],
    rows: list[list[str]],
    output_path: Path,
    figsize=(9.0, 3.8),
    font_size=10.0,
    col_widths: list[float] | None = None,
    title_font_size: float = 12.5,
) -> None:
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    ax.set_position([0.035, 0.055, 0.93, 0.80])
    ax.axis("off")
    fig.suptitle(title, fontsize=title_font_size, weight="bold", y=0.965)
    if col_widths is None:
        col_widths = [1 / len(columns)] * len(columns)
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        bbox=[0.0, 0.0, 1.0, 1.0],
        cellLoc="center",
        colLoc="center",
        colWidths=col_widths,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    for (row_idx, col_idx), cell in table.get_celld().items():
        cell.set_edgecolor("#bfbfbf")
        cell.set_linewidth(0.65)
        cell.PAD = 0.035
        if row_idx == 0:
            cell.set_facecolor(COLORS["header"])
            cell.set_text_props(weight="bold", color="#222222", fontsize=font_size)
        else:
            cell.set_facecolor("white")
            cell.set_text_props(color="#111111", fontsize=font_size)
            if col_idx == 0:
                cell.set_text_props(weight="bold", color="#222222", fontsize=font_size)
    save_figure(fig, output_path)


def parse_inference_times() -> tuple[float, float]:
    text = COMPARISON_SUMMARY_PATH.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"Inference:\s*([0-9.]+)\s*ms/image\s*->\s*([0-9.]+)\s*ms/image", text)
    if not match:
        raise RuntimeError("Could not parse inference times from comparison summary.")
    return float(match.group(1)), float(match.group(2))


def write_baseline_comparison(report_rows: list[dict], baseline_summary: dict, inference_times: tuple[float, float]) -> None:
    baseline_inf, final_inf = inference_times
    final_macro_f1 = next(row for row in report_rows if row["class"] == "Macro Avg")["f1_score"]
    baseline_accuracy = float(baseline_summary["accuracy"])
    baseline_macro_f1 = float(baseline_summary["macro_avg"]["f1"])
    baseline_errors = TEST_SAMPLES - int(round(baseline_accuracy * TEST_SAMPLES))

    rows = [
        ["Architecture", "EfficientNetB0", FINAL_ARCHITECTURE],
        ["Input size", INPUT_SIZE, INPUT_SIZE],
        ["Test accuracy", pct(baseline_accuracy), pct(FINAL_ACCURACY)],
        ["Macro F1-score", pct(baseline_macro_f1), pct(final_macro_f1)],
        ["Total errors", f"{baseline_errors}", f"{TOTAL_ERRORS}"],
        ["Inference time", f"{baseline_inf:.2f} ms/image", f"{final_inf:.2f} ms/image"],
    ]
    with (OUTPUT_DIR / "07_baseline_final_model_comparison.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "baseline_model", "final_model"])
        writer.writerows(rows)

    render_table_image(
        title="Baseline and Final Model Comparison",
        columns=["Metric", BASELINE_MODEL, FINAL_MODEL],
        rows=rows,
        output_path=OUTPUT_DIR / "07_baseline_final_model_comparison_table.png",
        figsize=(7.2, 3.2),
        font_size=8.6,
        col_widths=[0.34, 0.33, 0.33],
        title_font_size=12.0,
    )


def write_inference_summary(inference_times: tuple[float, float]) -> None:
    _, final_inf = inference_times
    total_seconds = final_inf * TEST_SAMPLES / 1000
    rows = [
        ["Model", FINAL_MODEL],
        ["Architecture", FINAL_ARCHITECTURE],
        ["Input size", INPUT_SIZE],
        ["Test samples", f"{TEST_SAMPLES}"],
        ["Final test accuracy", pct(FINAL_ACCURACY)],
        ["Total errors", f"{TOTAL_ERRORS}"],
        ["Mean inference time", f"{final_inf:.2f} ms/image"],
        ["Estimated test-set time", f"{total_seconds:.2f} s"],
    ]
    with (OUTPUT_DIR / "10_final_inference_time_summary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerows(rows)

    render_table_image(
        title="Final Inference Time Summary",
        columns=["Metric", "Value"],
        rows=rows,
        output_path=OUTPUT_DIR / "10_final_inference_time_summary_table.png",
        figsize=(6.2, 3.6),
        font_size=8.6,
        col_widths=[0.54, 0.46],
        title_font_size=12.0,
    )


def crop_main_image(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    arr = np.asarray(rgb)
    non_white = np.any(arr < 245, axis=2)
    row_counts = non_white.sum(axis=1)
    col_counts = non_white.sum(axis=0)
    rows = np.where(row_counts > arr.shape[1] * 0.45)[0]
    cols = np.where(col_counts > arr.shape[0] * 0.45)[0]
    if len(rows) == 0 or len(cols) == 0:
        return rgb
    return rgb.crop((int(cols.min()), int(rows.min()), int(cols.max()) + 1, int(rows.max()) + 1))


def find_column_groups(mask: np.ndarray, min_count: int = 20) -> list[tuple[int, int]]:
    counts = mask.sum(axis=0)
    active = counts > min_count
    groups = []
    start = None
    for idx, value in enumerate(active):
        if value and start is None:
            start = idx
        elif not value and start is not None:
            if idx - start > 80:
                groups.append((start, idx - 1))
            start = None
    if start is not None and len(active) - start > 80:
        groups.append((start, len(active) - 1))
    return groups


def crop_current_panel_images(panel_path: Path) -> tuple[Image.Image, Image.Image]:
    rgb = Image.open(panel_path).convert("RGB")
    arr = np.asarray(rgb)
    y0, y1 = 120, min(arr.shape[0], 725)
    band = arr[y0:y1]
    mask = np.any(band < 245, axis=2)
    groups = find_column_groups(mask, min_count=80)
    if len(groups) < 4:
        raise RuntimeError(f"Could not detect four image panels in {panel_path}")
    current_original_group = groups[2]
    current_overlay_group = groups[3]
    row_counts = mask[:, current_overlay_group[0] : current_overlay_group[1] + 1].sum(axis=1)
    active_rows = np.where(row_counts > 100)[0]
    top = int(active_rows.min()) + y0
    bottom = int(active_rows.max()) + y0 + 1
    current_original = rgb.crop((current_original_group[0], top, current_original_group[1] + 1, bottom))
    current_overlay = rgb.crop((current_overlay_group[0], top, current_overlay_group[1] + 1, bottom))
    return current_original, current_overlay


def image_to_array(image: Image.Image, size=(520, 520)) -> np.ndarray:
    fitted = image.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    return np.asarray(fitted)


def create_gradcam_class_panel() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 4.0), facecolor="white")
    for ax, label in zip(axes, CLASS_NAMES):
        cropped = crop_main_image(Image.open(CLASS_GRADCAM_PATHS[label]))
        ax.imshow(image_to_array(cropped, size=(520, 520)))
        ax.set_title(label, fontsize=12, weight="bold", pad=8)
        ax.axis("off")
    fig.suptitle("Final Grad-CAM Examples", fontsize=15, weight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.92], w_pad=1.0)
    save_figure(fig, OUTPUT_DIR / "08_gradcam_panel_healthy_bleached_dead.png")


def get_wrong_case() -> dict:
    with XAI_RESULTS_PATH.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["case_type"] == "current_wrong" and row["image"] == "Bleached/492.png":
                return row
    return {
        "true_label": "Bleached",
        "current_prediction": "Healthy",
        "current_confidence_percent": "54.2535",
    }


def create_wrong_gradcam_panel() -> None:
    wrong_case = get_wrong_case()
    try:
        original, overlay = crop_current_panel_images(WRONG_PANEL_PATH)
    except Exception:
        original = Image.open(DATASET_WRONG_PATH).convert("RGB")
        overlay = crop_main_image(Image.open(WRONG_PANEL_PATH))

    confidence = float(wrong_case["current_confidence_percent"])
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 4.2), facecolor="white")
    panel_specs = [
        (original, f"True: {wrong_case['true_label']}"),
        (overlay, f"Predicted: {wrong_case['current_prediction']} ({confidence:.1f}%)"),
    ]
    for ax, (img, title) in zip(axes, panel_specs):
        ax.imshow(image_to_array(img, size=(520, 520)))
        ax.set_title(title, fontsize=11.5, weight="bold", pad=8)
        ax.axis("off")
    fig.suptitle("Wrong Prediction Grad-CAM", fontsize=15, weight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.91], w_pad=1.0)
    save_figure(fig, OUTPUT_DIR / "09_gradcam_wrong_prediction_bleached_492.png")


def write_confusion_json(confusion_source: dict, cm: np.ndarray) -> None:
    payload = {
        "model": FINAL_MODEL,
        "architecture": FINAL_ARCHITECTURE,
        "input_size": INPUT_SIZE,
        "accuracy": FINAL_ACCURACY,
        "accuracy_percent": round(FINAL_ACCURACY * 100, 2),
        "test_samples": TEST_SAMPLES,
        "total_errors": TOTAL_ERRORS,
        "class_order": CLASS_NAMES,
        "confusion_matrix": cm.tolist(),
        "source_file": str(CONFUSION_PATH.relative_to(PROJECT_ROOT)),
        "source_protocol": confusion_source.get("protocol", "stored final benchmark"),
    }
    (OUTPUT_DIR / "05_final_confusion_matrix.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def write_readme_and_manifest(inference_times: tuple[float, float]) -> None:
    _, final_inf = inference_times
    manifest = {
        "canonical_benchmark": {
            "model_name": FINAL_MODEL,
            "architecture": FINAL_ARCHITECTURE,
            "input_size": INPUT_SIZE,
            "final_test_accuracy": FINAL_ACCURACY,
            "final_test_accuracy_percent": round(FINAL_ACCURACY * 100, 2),
            "test_samples": TEST_SAMPLES,
            "total_errors": TOTAL_ERRORS,
            "class_order": CLASS_NAMES,
        },
        "source_files": {
            "training_history": str(HISTORY_PATH.relative_to(PROJECT_ROOT)),
            "confusion_matrix": str(CONFUSION_PATH.relative_to(PROJECT_ROOT)),
            "baseline_summary": str(BASELINE_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "comparison_summary": str(COMPARISON_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "gradcam_correct_examples": {
                label: str(path.relative_to(PROJECT_ROOT))
                for label, path in CLASS_GRADCAM_PATHS.items()
            },
            "wrong_prediction_panel": str(WRONG_PANEL_PATH.relative_to(PROJECT_ROOT)),
            "xai_results": str(XAI_RESULTS_PATH.relative_to(PROJECT_ROOT)),
        },
        "generation_notes": [
            "No model training was performed.",
            "No model weights were changed.",
            "No prediction values were modified.",
            "Legacy model labels were normalized to Final Model and Baseline Model in generated figures.",
        ],
    }
    (OUTPUT_DIR / "00_source_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    readme = f"""# Chapter 4 Final Results

This folder contains clean Chapter 4-ready evaluation outputs generated from stored benchmark results.

## Final Benchmark Used

| Item | Value |
|---|---:|
| Model | {FINAL_MODEL} |
| Architecture | {FINAL_ARCHITECTURE} |
| Input size | {INPUT_SIZE} |
| Final test accuracy | {pct(FINAL_ACCURACY)} |
| Test samples | {TEST_SAMPLES} |
| Total errors | {TOTAL_ERRORS} |
| Mean inference time | {final_inf:.2f} ms/image |

No retraining was performed, model weights were not changed, and prediction values were not modified.

## Generated Files

| File | Description |
|---|---|
| `01_training_validation_accuracy.png` | Training and validation accuracy curve. |
| `02_training_validation_loss.png` | Training and validation loss curve. |
| `03_accuracy_gap_per_epoch.png` | Accuracy gap per epoch in percentage points. |
| `04_loss_gap_per_epoch.png` | Loss gap per epoch in decimal loss units. |
| `03_train_validation_gap_values.csv` | Numeric source values for the two gap figures. |
| `05_final_confusion_matrix.png` | Final confusion matrix. |
| `05_final_confusion_matrix.json` | Confusion matrix metadata and values. |
| `06_final_classification_report_table.png` | Final classification report as a table image. |
| `06_final_classification_report.csv` | Classification report values. |
| `07_baseline_final_model_comparison_table.png` | Baseline Model vs Final Model comparison table. |
| `07_baseline_final_model_comparison.csv` | Comparison table values. |
| `08_gradcam_panel_healthy_bleached_dead.png` | Final Grad-CAM examples for Healthy, Bleached, and Dead. |
| `09_gradcam_wrong_prediction_bleached_492.png` | Grad-CAM panel for one wrong prediction. |
| `10_final_inference_time_summary_table.png` | Final inference-time summary table. |
| `10_final_inference_time_summary.csv` | Inference-time summary values. |
| `00_source_manifest.json` | Source traceability and generation notes. |

## Gap Definition

The gap figures use `Training - Validation`.

- Accuracy gap is shown in percentage points.
- Loss gap is shown in decimal loss units.
- A zero reference line is included in both figures.
"""
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    figure_rows = [
        ("01_training_validation_accuracy.png", "Training and Validation Accuracy", "Model Training Results / Learning Curves"),
        ("02_training_validation_loss.png", "Training and Validation Loss", "Model Training Results / Learning Curves"),
        ("03_accuracy_gap_per_epoch.png", "Accuracy Gap per Epoch", "Overfitting and Generalisation Analysis"),
        ("04_loss_gap_per_epoch.png", "Loss Gap per Epoch", "Overfitting and Generalisation Analysis"),
        ("05_final_confusion_matrix.png", "Final Confusion Matrix", "Performance Evaluation"),
        ("06_final_classification_report_table.png", "Final Classification Report", "Performance Evaluation"),
        ("07_baseline_final_model_comparison_table.png", "Baseline and Final Model Comparison", "Baseline Comparison"),
        ("08_gradcam_panel_healthy_bleached_dead.png", "Final Grad-CAM Examples", "Explainable AI Results"),
        ("09_gradcam_wrong_prediction_bleached_492.png", "Wrong Prediction Grad-CAM", "Error Analysis / Explainability Discussion"),
        ("10_final_inference_time_summary_table.png", "Final Inference Time Summary", "Computational Performance / Deployment Discussion"),
    ]
    lines = [
        "# Chapter 4 Figure List",
        "",
        "| File name | Figure title | Suggested Chapter 4 placement |",
        "|---|---|---|",
    ]
    for file_name, title, placement in figure_rows:
        lines.append(f"| `{file_name}` | {title} | {placement} |")
    (OUTPUT_DIR / "chapter4_figure_list.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    clear_output_dir()

    history = load_json(HISTORY_PATH)
    confusion_source = load_json(CONFUSION_PATH)
    baseline_summary = load_json(BASELINE_SUMMARY_PATH)
    cm = np.array(confusion_source["confusion_matrix"], dtype=int)
    report_rows = compute_report(cm)
    inference_times = parse_inference_times()

    if int(cm.sum()) != TEST_SAMPLES:
        raise RuntimeError(f"Unexpected test sample count: {int(cm.sum())}")
    if int(cm.sum() - np.trace(cm)) != TOTAL_ERRORS:
        raise RuntimeError(f"Unexpected error count: {int(cm.sum() - np.trace(cm))}")

    plot_training_curves(history)
    plot_confusion_matrix(cm)
    write_confusion_json(confusion_source, cm)
    write_classification_report(report_rows)
    write_baseline_comparison(report_rows, baseline_summary, inference_times)
    create_gradcam_class_panel()
    create_wrong_gradcam_panel()
    write_inference_summary(inference_times)
    write_readme_and_manifest(inference_times)


if __name__ == "__main__":
    main()
