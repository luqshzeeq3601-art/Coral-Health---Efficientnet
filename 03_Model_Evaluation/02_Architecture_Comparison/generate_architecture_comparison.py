from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import seaborn as sns


CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
EFFNETB0_SINGLE_PARAMS = 4_053_414
EFFNETB0_ENSEMBLE_SIZE = 5
EFFNETB0_ENSEMBLE_PARAMS = EFFNETB0_SINGLE_PARAMS * EFFNETB0_ENSEMBLE_SIZE

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]

EFFNET_REPORT_PATH = PROJECT_ROOT / "03_Model_Evaluation" / "01_EfficientNetB0_Evaluation" / "classification_report_ensemble.txt"
EFFNET_CM_PATH = PROJECT_ROOT / "03_Model_Evaluation" / "01_EfficientNetB0_Evaluation" / "confusion_matrix_ensemble.json"
RESNET_SUMMARY_PATH = PROJECT_ROOT / "02_Modelling" / "resnet50_coral" / "outputs" / "run_summary_resnet50.json"
RESNET_CM_PATH = PROJECT_ROOT / "02_Modelling" / "resnet50_coral" / "outputs" / "confusion_matrix_resnet50.json"
CONVNEXT_SUMMARY_PATH = PROJECT_ROOT / "02_Modelling" / "convnexttiny_coral" / "outputs" / "run_summary_convnexttiny.json"
CONVNEXT_CM_PATH = PROJECT_ROOT / "02_Modelling" / "convnexttiny_coral" / "outputs" / "confusion_matrix_convnexttiny.json"


def read_json(path: Path) -> Dict:
    if not path.exists():
        raise FileNotFoundError(f"Required source file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Required source file not found: {path}")


def metrics_from_confusion_matrix(cm: np.ndarray) -> Dict[str, object]:
    support = cm.sum(axis=1)
    predicted = cm.sum(axis=0)
    tp = np.diag(cm)

    precision = np.divide(tp, predicted, out=np.zeros_like(tp, dtype=float), where=predicted != 0)
    recall = np.divide(tp, support, out=np.zeros_like(tp, dtype=float), where=support != 0)
    f1 = np.divide(2 * precision * recall, precision + recall, out=np.zeros_like(tp, dtype=float), where=(precision + recall) != 0)

    total = int(cm.sum())
    correct = int(tp.sum())
    accuracy = correct / total if total else 0.0
    total_errors = total - correct
    weights = support / total if total else np.zeros_like(support, dtype=float)

    per_class = {}
    for idx, cls_name in enumerate(CLASS_NAMES):
        per_class[cls_name] = {
            "precision": float(precision[idx]),
            "recall": float(recall[idx]),
            "f1": float(f1[idx]),
            "support": int(support[idx]),
        }

    return {
        "accuracy": float(accuracy),
        "accuracy_percent": float(accuracy * 100),
        "macro_precision": float(np.mean(precision)),
        "macro_recall": float(np.mean(recall)),
        "macro_f1": float(np.mean(f1)),
        "weighted_precision": float(np.sum(precision * weights)),
        "weighted_recall": float(np.sum(recall * weights)),
        "weighted_f1": float(np.sum(f1 * weights)),
        "total_errors": int(total_errors),
        "test_samples": int(total),
        "per_class": per_class,
    }


def validate_class_order(payload: Dict, model_name: str) -> None:
    order = payload.get("class_order")
    if order != CLASS_NAMES:
        raise ValueError(f"{model_name} class order mismatch: expected {CLASS_NAMES}, got {order}")


def build_model_record(name: str, model_type: str, params: int, cm_payload: Dict, protocol: str) -> Dict[str, object]:
    validate_class_order(cm_payload, name)
    cm = np.array(cm_payload["confusion_matrix"], dtype=int)
    metrics = metrics_from_confusion_matrix(cm)
    if metrics["test_samples"] != 159:
        raise ValueError(f"{name} test size mismatch: expected 159, got {metrics['test_samples']}")

    return {
        "model": name,
        "model_type": model_type,
        "protocol": protocol,
        "parameters": int(params),
        "parameters_m": float(params / 1_000_000),
        "confusion_matrix": cm.tolist(),
        **metrics,
    }


def load_comparison_data() -> List[Dict[str, object]]:
    require_file(EFFNET_REPORT_PATH)

    effnet_cm = read_json(EFFNET_CM_PATH)
    resnet_summary = read_json(RESNET_SUMMARY_PATH)
    resnet_cm = read_json(RESNET_CM_PATH)
    convnext_summary = read_json(CONVNEXT_SUMMARY_PATH)
    convnext_cm = read_json(CONVNEXT_CM_PATH)

    records = [
        build_model_record(
            name="EfficientNetB0 Ensemble",
            model_type="5-seed SWA ensemble",
            params=EFFNETB0_ENSEMBLE_PARAMS,
            cm_payload=effnet_cm,
            protocol=effnet_cm.get("protocol", "224px canonical benchmark"),
        ),
        build_model_record(
            name="ResNet50 Single",
            model_type="Single robust SWA model",
            params=int(resnet_summary["total_params"]),
            cm_payload=resnet_cm,
            protocol=resnet_cm.get("protocol", "224px single-scale, no TTA"),
        ),
        build_model_record(
            name="ConvNeXtTiny Single",
            model_type="Single robust SWA model",
            params=int(convnext_summary["total_params"]),
            cm_payload=convnext_cm,
            protocol=convnext_cm.get("protocol", "224px single-scale, no TTA"),
        ),
    ]
    return records


def write_summary_csv(records: List[Dict[str, object]]) -> None:
    path = SCRIPT_DIR / "architecture_comparison_summary.csv"
    fieldnames = [
        "model",
        "model_type",
        "parameters",
        "parameters_m",
        "accuracy_percent",
        "macro_f1",
        "weighted_f1",
        "total_errors",
        "healthy_f1",
        "bleached_f1",
        "dead_f1",
        "test_samples",
        "protocol",
    ]

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow({
                "model": record["model"],
                "model_type": record["model_type"],
                "parameters": record["parameters"],
                "parameters_m": f"{record['parameters_m']:.4f}",
                "accuracy_percent": f"{record['accuracy_percent']:.4f}",
                "macro_f1": f"{record['macro_f1']:.6f}",
                "weighted_f1": f"{record['weighted_f1']:.6f}",
                "total_errors": record["total_errors"],
                "healthy_f1": f"{record['per_class']['Healthy']['f1']:.6f}",
                "bleached_f1": f"{record['per_class']['Bleached']['f1']:.6f}",
                "dead_f1": f"{record['per_class']['Dead']['f1']:.6f}",
                "test_samples": record["test_samples"],
                "protocol": record["protocol"],
            })


def write_summary_json(records: List[Dict[str, object]]) -> None:
    payload = {
        "title": "Three-Model Architecture Comparison",
        "class_order": CLASS_NAMES,
        "note": "EfficientNetB0 parameter count uses total 5-model ensemble parameters.",
        "source_files": {
            "efficientnetb0_report": str(EFFNET_REPORT_PATH.relative_to(PROJECT_ROOT)),
            "efficientnetb0_confusion_matrix": str(EFFNET_CM_PATH.relative_to(PROJECT_ROOT)),
            "resnet50_summary": str(RESNET_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "resnet50_confusion_matrix": str(RESNET_CM_PATH.relative_to(PROJECT_ROOT)),
            "convnexttiny_summary": str(CONVNEXT_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "convnexttiny_confusion_matrix": str(CONVNEXT_CM_PATH.relative_to(PROJECT_ROOT)),
        },
        "models": records,
    }
    (SCRIPT_DIR / "architecture_comparison_summary.json").write_text(json.dumps(payload, indent=4), encoding="utf-8")


def write_notes(records: List[Dict[str, object]]) -> None:
    best_accuracy_value = max(r["accuracy_percent"] for r in records)
    best_accuracy_models = [
        r["model"] for r in records if abs(r["accuracy_percent"] - best_accuracy_value) < 1e-9
    ]
    best_macro = max(records, key=lambda r: r["macro_f1"])
    largest = max(records, key=lambda r: r["parameters"])

    rows = []
    for r in records:
        rows.append(
            f"| {r['model']} | {r['model_type']} | {r['parameters_m']:.2f}M | "
            f"{r['accuracy_percent']:.2f}% | {r['macro_f1']:.4f} | "
            f"{r['per_class']['Dead']['f1']:.4f} | {r['total_errors']} |"
        )

    content = f"""# Architecture Comparison Notes

This comparison uses the same 159-image held-out test set and class order: `Healthy`, `Bleached`, `Dead`.

| Model | Type | Parameters | Accuracy | Macro F1 | Dead F1 | Errors |
|---|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

## Interpretation

- Best accuracy: `{", ".join(best_accuracy_models)}` tied at `{best_accuracy_value:.2f}%`.
- Best macro F1: `{best_macro['model']}` at `{best_macro['macro_f1']:.4f}`.
- Largest model: `{largest['model']}` with `{largest['parameters_m']:.2f}M` parameters.
- EfficientNetB0 uses `4,053,414 x 5 = 20,267,070` parameters on the parameter axis because the current benchmark is a 5-model ensemble.
- ResNet50 matches EfficientNetB0 accuracy but has weaker `Dead` F1, so accuracy alone is not enough to describe robustness.
- ConvNeXtTiny has the largest parameter count, but its accuracy is lower than EfficientNetB0 and ResNet50 on this test split.
"""
    (SCRIPT_DIR / "architecture_comparison_notes.md").write_text(content, encoding="utf-8")


def plot_accuracy_vs_parameters(records: List[Dict[str, object]]) -> None:
    colors = ["#008B7A", "#D71920", "#1F5CCB"]
    light_rows = ["#EAF8F6", "#FCEBEC", "#EAF1FF"]
    markers = ["o", "s", "^"]
    callout_offsets = [(0.15, 0.26), (0.25, 0.27), (0.15, 0.27)]
    status_labels = ["Best balance", "Accuracy tie", "Largest parameter count"]

    fig = plt.figure(figsize=(16, 10), facecolor="white")
    gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[4.6, 1.45], hspace=0.18)
    ax = fig.add_subplot(gs[0])
    ax_table = fig.add_subplot(gs[1])

    fig.text(
        0.5,
        0.965,
        "Model Size vs Test Accuracy",
        ha="center",
        va="top",
        fontsize=25,
        fontweight="bold",
        color="#14213D",
    )

    for idx, record in enumerate(records):
        x = record["parameters_m"]
        y = record["accuracy_percent"]

        ax.scatter(
            x + 0.03,
            y - 0.025,
            s=560,
            color="black",
            alpha=0.12,
            marker=markers[idx],
            linewidths=0,
            zorder=2,
        )
        ax.scatter(
            x,
            y,
            s=420,
            color=colors[idx],
            marker=markers[idx],
            edgecolors="white",
            linewidths=2.8,
            zorder=4,
        )

        dx, dy = callout_offsets[idx]
        callout_x = x + dx
        callout_y = y + dy
        ax.annotate(
            f"{record['model']}\n"
            f"{record['parameters_m']:.2f}M params\n"
            f"{record['accuracy_percent']:.2f}% acc.",
            xy=(x, y),
            xytext=(callout_x, callout_y),
            ha="center",
            va="center",
            fontsize=11,
            color=colors[idx],
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.55,rounding_size=0.18",
                "fc": "white",
                "ec": colors[idx],
                "lw": 1.3,
            },
            arrowprops={
                "arrowstyle": "-|>",
                "color": colors[idx],
                "lw": 1.0,
                "linestyle": (0, (2, 3)),
                "shrinkA": 4,
                "shrinkB": 7,
            },
            zorder=5,
        )
        ax.text(
            x,
            y - 0.16,
            status_labels[idx],
            ha="center",
            va="center",
            fontsize=11,
            color=colors[idx],
            fontweight="bold",
        )

    ax.set_xlim(18, 30)
    ax.set_ylim(97.0, 98.4)
    ax.set_xticks(np.arange(18, 31, 2))
    ax.set_yticks(np.arange(97.0, 98.41, 0.2))
    ax.set_xlabel("Number of Parameters (Millions)", fontsize=15, fontweight="bold", color="#14213D", labelpad=9)
    ax.set_ylabel("Test Accuracy (%)", fontsize=15, fontweight="bold", color="#14213D", labelpad=12)
    ax.grid(True, linestyle="--", linewidth=0.9, alpha=0.3, color="#8D99AE")
    ax.tick_params(axis="both", labelsize=12, colors="#14213D")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#14213D")
    ax.spines["bottom"].set_color("#14213D")
    ax.spines["left"].set_linewidth(1.4)
    ax.spines["bottom"].set_linewidth(1.4)
    ax_table.axis("off")
    columns = ["Model", "Parameters (M)", "Test Accuracy (%)", "Precision (Macro)", "Recall (Macro)", "F1-Score (Macro)", "Errors"]
    table_data = []
    for record in records:
        table_data.append([
            record["model"],
            f"{record['parameters_m']:.2f}",
            f"{record['accuracy_percent']:.2f}",
            f"{record['macro_precision']:.2f}",
            f"{record['macro_recall']:.2f}",
            f"{record['macro_f1']:.2f}",
            str(record["total_errors"]),
        ])

    table = ax_table.table(
        cellText=table_data,
        colLabels=columns,
        cellLoc="center",
        loc="center",
        colWidths=[0.27, 0.13, 0.15, 0.15, 0.14, 0.15, 0.08],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1.0, 1.55)

    for col in range(len(columns)):
        table[0, col].set_facecolor("#14213D")
        table[0, col].set_edgecolor("white")
        table[0, col].set_text_props(color="white", fontweight="bold")

    for row_idx in range(1, len(table_data) + 1):
        row_color = light_rows[row_idx - 1]
        text_color = colors[row_idx - 1]
        for col in range(len(columns)):
            table[row_idx, col].set_facecolor(row_color)
            table[row_idx, col].set_edgecolor("white")
            if col in {0, 1, 2}:
                table[row_idx, col].set_text_props(color=text_color, fontweight="bold")

    fig.text(
        0.5,
        0.018,
        "Note: EfficientNetB0 parameters use the full 5-model ensemble total (4.05M x 5). "
        "All results use the same 159-image held-out test split.",
        ha="center",
        fontsize=10.5,
        color="#4F5D75",
    )
    plt.savefig(SCRIPT_DIR / "01_accuracy_vs_parameters.png", dpi=180, bbox_inches="tight")
    plt.close()


def plot_per_class_f1(records: List[Dict[str, object]]) -> None:
    x = np.arange(len(CLASS_NAMES))
    width = 0.21
    colors = ["#008B7A", "#EF3340", "#1F5CCB"]
    panel_colors = ["#E6F5F2", "#FFF3E4", "#FCE8EA"]
    legend_labels = ["EfficientNetB0 Ensemble", "ResNet50 Single", "ConvNeXtTiny Single"]

    fig = plt.figure(figsize=(16, 10), facecolor="white")
    gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[4.8, 0.9], hspace=0.18)
    ax = fig.add_subplot(gs[0])
    ax_insights = fig.add_subplot(gs[1])

    fig.text(
        0.5,
        0.965,
        "Per-Class F1-Score Comparison",
        ha="center",
        va="top",
        fontsize=27,
        fontweight="bold",
        color="#14213D",
    )
    fig.text(
        0.5,
        0.918,
        "Coral Reef Health Classification (BHD Dataset)",
        ha="center",
        va="top",
        fontsize=16,
        color="#4F5D75",
        style="italic",
    )
    fig.text(
        0.5,
        0.872,
        "Higher F1-score indicates better balance between precision and recall for each class.",
        ha="center",
        va="center",
        fontsize=11,
        color="#14213D",
        bbox={
            "boxstyle": "round,pad=0.55,rounding_size=0.16",
            "fc": "#F8FAFC",
            "ec": "#CBD5E1",
            "lw": 0.9,
        },
    )

    for cls_idx, panel_color in enumerate(panel_colors):
        panel = FancyBboxPatch(
            (cls_idx - 0.47, 0.802),
            0.94,
            0.238,
            boxstyle="round,pad=0.02,rounding_size=0.045",
            facecolor=panel_color,
            edgecolor="none",
            alpha=0.48,
            zorder=0,
        )
        ax.add_patch(panel)

    for idx, record in enumerate(records):
        f1_values = [record["per_class"][cls]["f1"] for cls in CLASS_NAMES]
        offsets = x + (idx - 1) * width
        ax.bar(
            offsets + 0.018,
            [value - 0.002 for value in f1_values],
            width,
            color="#000000",
            alpha=0.08,
            linewidth=0,
            zorder=1,
        )
        bars = ax.bar(
            offsets,
            f1_values,
            width,
            label=legend_labels[idx],
            color=colors[idx],
            edgecolor="white",
            linewidth=1.4,
            zorder=3,
        )
        for bar, value in zip(bars, f1_values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + 0.006,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=9,
                color=colors[idx],
                fontweight="bold",
            )

    ax.set_xlabel("Class", fontsize=15, fontweight="bold", color="#14213D", labelpad=8)
    ax.set_ylabel("F1-Score", fontsize=15, fontweight="bold", color="#14213D", labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(CLASS_NAMES, fontsize=12, fontweight="bold")
    for tick, color in zip(ax.get_xticklabels(), colors):
        tick.set_color(color)
    ax.set_ylim(0.80, 1.05)
    ax.set_yticks(np.arange(0.80, 1.051, 0.05))
    ax.grid(axis="y", linestyle="--", alpha=0.35, color="#94A3B8")
    ax.tick_params(axis="y", labelsize=11, colors="#14213D")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#14213D")
    ax.spines["bottom"].set_color("#14213D")
    ax.legend(
        loc="upper right",
        bbox_to_anchor=(0.985, 0.985),
        frameon=True,
        facecolor="white",
        edgecolor="#CBD5E1",
        framealpha=0.96,
        fontsize=10.5,
        borderpad=0.75,
        labelspacing=0.6,
    )

    ax_insights.axis("off")
    insight_box = FancyBboxPatch(
        (0.02, 0.15),
        0.96,
        0.72,
        boxstyle="round,pad=0.02,rounding_size=0.035",
        transform=ax_insights.transAxes,
        facecolor="#F8FAFC",
        edgecolor="#D5DEE8",
        linewidth=0.8,
    )
    ax_insights.add_patch(insight_box)
    ax_insights.text(0.07, 0.52, "Key Insights", transform=ax_insights.transAxes, fontsize=12, fontweight="bold", color="#1F5CCB", va="center")
    ax_insights.text(0.23, 0.52, "ResNet50 is strongest for Healthy.", transform=ax_insights.transAxes, fontsize=10.5, color="#14213D", va="center")
    ax_insights.text(0.49, 0.52, "All models are consistent on Bleached.", transform=ax_insights.transAxes, fontsize=10.5, color="#14213D", va="center")
    ax_insights.text(0.75, 0.52, "EffNetB0 and ConvNeXtTiny lead on Dead.", transform=ax_insights.transAxes, fontsize=10.5, color="#14213D", va="center")
    for xpos in [0.19, 0.45, 0.71]:
        ax_insights.plot([xpos, xpos], [0.3, 0.73], transform=ax_insights.transAxes, color="#CBD5E1", linewidth=1)

    plt.subplots_adjust(top=0.80, bottom=0.08, left=0.08, right=0.965)
    plt.savefig(SCRIPT_DIR / "02_per_class_f1_comparison.png", dpi=180, bbox_inches="tight")
    plt.close()


def plot_confusion_matrices(records: List[Dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), facecolor="white")
    vmax = max(max(max(row) for row in record["confusion_matrix"]) for record in records)

    for ax, record in zip(axes, records):
        sns.heatmap(
            np.array(record["confusion_matrix"]),
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=CLASS_NAMES,
            yticklabels=CLASS_NAMES,
            vmin=0,
            vmax=vmax,
            cbar=False,
            ax=ax,
            annot_kws={"size": 13},
        )
        ax.set_title(f"{record['model']}\nErrors: {record['total_errors']}", fontsize=12, fontweight="bold")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")

    fig.suptitle("Confusion Matrix Comparison", fontsize=16, fontweight="bold", y=1.03)
    plt.tight_layout()
    plt.savefig(SCRIPT_DIR / "03_confusion_matrix_three_models.png", dpi=180, bbox_inches="tight")
    plt.close()


def plot_summary_table(records: List[Dict[str, object]]) -> None:
    columns = ["Model", "Type", "Params", "Accuracy", "Macro F1", "Weighted F1", "Errors"]
    table_data = [
        [
            r["model"],
            r["model_type"],
            f"{r['parameters_m']:.2f}M",
            f"{r['accuracy_percent']:.2f}%",
            f"{r['macro_f1']:.4f}",
            f"{r['weighted_f1']:.4f}",
            str(r["total_errors"]),
        ]
        for r in records
    ]

    fig, ax = plt.subplots(figsize=(14, 4.2), facecolor="white")
    ax.axis("off")
    ax.set_title("Architecture Comparison Summary", fontsize=16, fontweight="bold", pad=18)

    table = ax.table(cellText=table_data, colLabels=columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.0, 1.75)

    for col in range(len(columns)):
        table[0, col].set_facecolor("#2F5597")
        table[0, col].set_text_props(color="white", fontweight="bold")
    for row in range(1, len(table_data) + 1):
        for col in range(len(columns)):
            table[row, col].set_facecolor("#EAF2F8" if row % 2 else "#F7F9FA")

    plt.tight_layout()
    plt.savefig(SCRIPT_DIR / "04_accuracy_macro_f1_table.png", dpi=180, bbox_inches="tight")
    plt.close()


def main() -> None:
    records = load_comparison_data()
    write_summary_csv(records)
    write_summary_json(records)
    write_notes(records)
    plot_accuracy_vs_parameters(records)
    plot_per_class_f1(records)
    plot_confusion_matrices(records)
    plot_summary_table(records)
    print(f"Architecture comparison outputs saved to: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
