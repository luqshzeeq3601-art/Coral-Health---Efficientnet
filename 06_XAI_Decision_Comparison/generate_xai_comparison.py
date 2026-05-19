import argparse
import csv
import gc
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import matplotlib
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


IMG_SIZE = 224
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
CURRENT_SEEDS = [42, 43, 44, 45, 46]
DEFAULT_UNCERTAIN_THRESHOLD = 75.0
BASELINE_DISPLAY_NAME = "Baseline EffNetB0"
CURRENT_DISPLAY_NAME = "V4 Robust EffNetB0"

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATASET_DIR = PROJECT_ROOT / "Dataset"
SPLIT_INFO_PATH = PROJECT_ROOT / "05_Baseline_Model" / "split_info_v3.json"
BASELINE_MODEL_PATH = (
    PROJECT_ROOT / "05_Baseline_Model" / "models" / "efficientnetb0_baseline.weights.h5"
)
CURRENT_MODEL_DIR = PROJECT_ROOT / "02_Modelling" / "efficientnetb0_coral" / "models"
OUTPUT_DIR = SCRIPT_DIR / "outputs"
PANELS_DIR = OUTPUT_DIR / "panels"


def build_baseline_model() -> tf.keras.Model:
    base_model = EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    base_model.trainable = False
    return Sequential(
        [
            Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
            base_model,
            GlobalAveragePooling2D(),
            Dense(3, activation="softmax"),
        ]
    )


def build_current_model() -> tf.keras.Model:
    base_model = EfficientNetB0(
        include_top=False,
        weights="imagenet",
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


def prepare_output_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    for child in PANELS_DIR.iterdir():
        if child.is_file() or child.is_symlink():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)


def resolve_dataset_path(relative_name: str) -> Path:
    normalized = relative_name.replace("\\", "/")
    candidate = DATASET_DIR / normalized
    if candidate.exists():
        return candidate

    parts = normalized.split("/")
    if len(parts) >= 2:
        case_fallback = DATASET_DIR / parts[0].capitalize() / Path(*parts[1:])
        if case_fallback.exists():
            return case_fallback

    raise FileNotFoundError(f"Dataset file not found for split entry: {relative_name}")


def load_test_split() -> Tuple[np.ndarray, np.ndarray, List[str], List[Path]]:
    if not SPLIT_INFO_PATH.exists():
        raise FileNotFoundError(f"Missing test split file: {SPLIT_INFO_PATH}")

    with SPLIT_INFO_PATH.open("r", encoding="utf-8") as f:
        split_info = json.load(f)

    images: List[np.ndarray] = []
    labels: List[int] = []
    rel_paths: List[str] = []
    abs_paths: List[Path] = []

    for relative_name in split_info["test_files"]:
        label_name = relative_name.replace("\\", "/").split("/")[0]
        if label_name not in CLASS_NAMES:
            raise ValueError(f"Unknown class in split entry: {relative_name}")

        path = resolve_dataset_path(relative_name)
        img_bgr = cv2.imread(str(path))
        if img_bgr is None:
            raise RuntimeError(f"Could not read image: {path}")

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
        images.append(img_rgb.astype("float32"))
        labels.append(CLASS_NAMES.index(label_name))
        rel_paths.append(relative_name.replace("\\", "/"))
        abs_paths.append(path)

    return (
        np.asarray(images, dtype="float32"),
        np.asarray(labels, dtype=np.int32),
        rel_paths,
        abs_paths,
    )


def load_baseline() -> tf.keras.Model:
    if not BASELINE_MODEL_PATH.exists():
        raise FileNotFoundError(f"Baseline weights not found: {BASELINE_MODEL_PATH}")
    model = build_baseline_model()
    model.load_weights(str(BASELINE_MODEL_PATH))
    return model


def load_current_models() -> List[tf.keras.Model]:
    models: List[tf.keras.Model] = []
    for seed in CURRENT_SEEDS:
        path = CURRENT_MODEL_DIR / f"efficientnetb0_v4robust_seed{seed}_swa.h5"
        if not path.exists():
            raise FileNotFoundError(f"Current model weights not found: {path}")
        model = build_current_model()
        model.load_weights(str(path))
        models.append(model)
    return models


def predict_current_ensemble(models: List[tf.keras.Model], x_test: np.ndarray) -> np.ndarray:
    probs = [model.predict(x_test, batch_size=16, verbose=0) for model in models]
    return np.mean(probs, axis=0)


def find_efficientnet(model: tf.keras.Model) -> Optional[tf.keras.Model]:
    for layer in model.layers:
        if "efficientnet" in layer.name.lower():
            return layer
    return None


def find_target_layer(efficientnet: tf.keras.Model, layer_name: str) -> Optional[tf.keras.layers.Layer]:
    try:
        return efficientnet.get_layer(layer_name)
    except Exception:
        for layer in reversed(efficientnet.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer
    return None


def make_gradcam_heatmap(
    image: np.ndarray,
    model: tf.keras.Model,
    class_idx: int,
    layer_name: str = "top_conv",
) -> np.ndarray:
    efficientnet = find_efficientnet(model)
    if efficientnet is None:
        return np.zeros((IMG_SIZE, IMG_SIZE), dtype="float32")

    target_layer = find_target_layer(efficientnet, layer_name)
    if target_layer is None:
        return np.zeros((IMG_SIZE, IMG_SIZE), dtype="float32")

    img_batch = tf.cast(np.expand_dims(image, axis=0), tf.float32)
    grad_model_part1 = tf.keras.models.Model(
        inputs=efficientnet.input,
        outputs=target_layer.output,
    )

    try:
        top_bn = efficientnet.get_layer("top_bn")
        top_activation = efficientnet.get_layer("top_activation")
        has_top_layers = True
    except Exception:
        top_bn = None
        top_activation = None
        has_top_layers = False

    eff_index = -1
    for idx, layer in enumerate(model.layers):
        if layer == efficientnet:
            eff_index = idx
            break

    with tf.GradientTape() as tape:
        conv_outputs = grad_model_part1(img_batch, training=False)
        tape.watch(conv_outputs)

        x = conv_outputs
        if has_top_layers:
            x = top_bn(x, training=False)
            x = top_activation(x)

        if eff_index != -1:
            for layer in model.layers[eff_index + 1 :]:
                try:
                    x = layer(x, training=False)
                except TypeError:
                    x = layer(x)

        loss = x[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)
    if grads is None:
        return np.zeros((IMG_SIZE, IMG_SIZE), dtype="float32")

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out = conv_outputs[0]
    heatmap = conv_out @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.nn.relu(heatmap).numpy()
    heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)

    max_value = float(np.max(heatmap))
    if max_value > 0:
        heatmap = heatmap / max_value
    return heatmap.astype("float32")


def make_current_ensemble_heatmap(
    image: np.ndarray,
    models: List[tf.keras.Model],
    class_idx: int,
) -> np.ndarray:
    heatmaps = [make_gradcam_heatmap(image, model, class_idx) for model in models]
    avg_heatmap = np.mean(heatmaps, axis=0)
    max_value = float(np.max(avg_heatmap))
    if max_value > 0:
        avg_heatmap = avg_heatmap / max_value
    return avg_heatmap.astype("float32")


def create_overlay(image: np.ndarray, heatmap: np.ndarray, alpha: float = 0.42) -> np.ndarray:
    img_uint8 = np.clip(image, 0, 255).astype(np.uint8)
    heatmap_uint8 = np.uint8(255 * np.clip(heatmap, 0, 1))
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    return cv2.addWeighted(img_uint8, 1.0 - alpha, heatmap_colored, alpha, 0)


def fmt_conf(probability: float) -> str:
    return f"{probability * 100:.1f}%"


def slugify(value: str) -> str:
    value = value.replace("/", "_").replace("\\", "_")
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    return value.strip("_")


def build_result_rows(
    y_true: np.ndarray,
    rel_paths: List[str],
    baseline_probs: np.ndarray,
    current_probs: np.ndarray,
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    baseline_preds = np.argmax(baseline_probs, axis=1)
    current_preds = np.argmax(current_probs, axis=1)

    for idx, rel_path in enumerate(rel_paths):
        true_idx = int(y_true[idx])
        baseline_idx = int(baseline_preds[idx])
        current_idx = int(current_preds[idx])
        rows.append(
            {
                "index": idx,
                "image": rel_path,
                "true_idx": true_idx,
                "true_label": CLASS_NAMES[true_idx],
                "baseline_idx": baseline_idx,
                "baseline_prediction": CLASS_NAMES[baseline_idx],
                "baseline_confidence": float(baseline_probs[idx][baseline_idx]),
                "baseline_correct": baseline_idx == true_idx,
                "current_idx": current_idx,
                "current_prediction": CLASS_NAMES[current_idx],
                "current_confidence": float(current_probs[idx][current_idx]),
                "current_correct": current_idx == true_idx,
            }
        )
    return rows


def choose_one(
    rows: List[Dict[str, object]],
    used_indexes: set,
    predicate,
    sort_key,
) -> Optional[Dict[str, object]]:
    candidates = [row for row in rows if row["index"] not in used_indexes and predicate(row)]
    if not candidates:
        return None
    return sorted(candidates, key=sort_key, reverse=True)[0]


def select_curated_rows(
    rows: List[Dict[str, object]],
    uncertain_threshold: float,
    max_challenges: int,
) -> List[Dict[str, object]]:
    selected: List[Dict[str, object]] = []
    used_indexes = set()

    for class_idx, class_name in enumerate(CLASS_NAMES):
        representative = choose_one(
            rows,
            used_indexes,
            lambda row, cls=class_idx: (
                row["true_idx"] == cls
                and row["baseline_correct"]
                and row["current_correct"]
            ),
            lambda row: row["baseline_confidence"] + row["current_confidence"],
        )
        if representative is None:
            representative = choose_one(
                rows,
                used_indexes,
                lambda row, cls=class_idx: row["true_idx"] == cls and row["current_correct"],
                lambda row: row["current_confidence"],
            )
        if representative is None:
            representative = choose_one(
                rows,
                used_indexes,
                lambda row, cls=class_idx: row["true_idx"] == cls,
                lambda row: row["current_confidence"],
            )

        if representative is not None:
            representative = dict(representative)
            representative["case_type"] = f"{class_name.lower()}_representative_correct"
            selected.append(representative)
            used_indexes.add(representative["index"])

    challenge_specs = [
        (
            "baseline_wrong_current_correct",
            lambda row: (not row["baseline_correct"]) and row["current_correct"],
            lambda row: row["current_confidence"],
        ),
        (
            "current_uncertain",
            lambda row: row["current_confidence"] * 100.0 < uncertain_threshold,
            lambda row: -row["current_confidence"],
        ),
        (
            "current_wrong",
            lambda row: not row["current_correct"],
            lambda row: row["current_confidence"],
        ),
    ]

    for case_type, predicate, sort_key in challenge_specs:
        if len(selected) >= len(CLASS_NAMES) + max_challenges:
            break
        challenge = choose_one(rows, used_indexes, predicate, sort_key)
        if challenge is None:
            continue
        challenge = dict(challenge)
        challenge["case_type"] = case_type
        selected.append(challenge)
        used_indexes.add(challenge["index"])

    return selected


def panel_title(row: Dict[str, object], model_name: str, is_current: bool) -> str:
    pred_key = "current_prediction" if is_current else "baseline_prediction"
    conf_key = "current_confidence" if is_current else "baseline_confidence"
    correct_key = "current_correct" if is_current else "baseline_correct"
    status = "Correct" if row[correct_key] else "Wrong"
    return f"{model_name}\nPred: {row[pred_key]} ({fmt_conf(row[conf_key])}) | {status}"


def gradcam_title(row: Dict[str, object], model_name: str, is_current: bool) -> str:
    pred_key = "current_prediction" if is_current else "baseline_prediction"
    return f"{model_name} + Grad-CAM\nExplains: {row[pred_key]}"


def save_four_panel(
    row: Dict[str, object],
    image: np.ndarray,
    baseline_heatmap: np.ndarray,
    current_heatmap: np.ndarray,
    output_path: Path,
) -> None:
    baseline_overlay = create_overlay(image, baseline_heatmap)
    current_overlay = create_overlay(image, current_heatmap)
    img_uint8 = np.clip(image, 0, 255).astype(np.uint8)

    fig, axes = plt.subplots(1, 4, figsize=(17, 5), facecolor="white")
    panels = [
        (img_uint8, panel_title(row, BASELINE_DISPLAY_NAME, False)),
        (baseline_overlay, gradcam_title(row, BASELINE_DISPLAY_NAME, False)),
        (img_uint8, panel_title(row, CURRENT_DISPLAY_NAME, True)),
        (current_overlay, gradcam_title(row, CURRENT_DISPLAY_NAME, True)),
    ]

    for ax, (panel_img, title) in zip(axes, panels):
        ax.imshow(panel_img)
        ax.set_title(title, fontsize=10.5, fontweight="bold", pad=9)
        ax.axis("off")

    fig.suptitle(
        f"XAI Decision Comparison | True: {row['true_label']} | Image: {row['image']}",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    fig.text(
        0.5,
        0.02,
        "Grad-CAM is post-prediction evidence: it highlights image regions that supported each model's predicted class.",
        ha="center",
        fontsize=9.5,
        color="#2C3E50",
    )
    plt.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def load_font(size: int) -> ImageFont.ImageFont:
    for font_name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            pass
    return ImageFont.load_default()


def create_contact_sheet(panel_paths: List[Path], output_path: Path) -> None:
    if not panel_paths:
        return

    title_font = load_font(28)
    caption_font = load_font(18)
    target_width = 1800
    top_margin = 90
    gap = 28
    side_margin = 34
    bottom_margin = 34

    resized_panels: List[Image.Image] = []
    for path in panel_paths:
        img = Image.open(path).convert("RGB")
        scale = target_width / img.width
        resized = img.resize((target_width, int(img.height * scale)), Image.LANCZOS)
        resized_panels.append(resized)

    total_height = top_margin + bottom_margin + sum(img.height for img in resized_panels)
    total_height += gap * (len(resized_panels) - 1)
    sheet = Image.new("RGB", (target_width + side_margin * 2, total_height), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text(
        (side_margin, 24),
        f"XAI Decision Comparison: {BASELINE_DISPLAY_NAME} vs {CURRENT_DISPLAY_NAME}",
        fill="#1F2A44",
        font=title_font,
    )
    draw.text(
        (side_margin, 60),
        "Prediction-only panels show the decision; Grad-CAM panels show supporting visual evidence.",
        fill="#4B5563",
        font=caption_font,
    )

    y = top_margin
    for img in resized_panels:
        sheet.paste(img, (side_margin, y))
        y += img.height + gap

    sheet.save(output_path)


def write_results_csv(rows: List[Dict[str, object]], output_path: Path) -> None:
    fields = [
        "rank",
        "case_type",
        "image",
        "true_label",
        "baseline_prediction",
        "baseline_confidence_percent",
        "baseline_correct",
        "current_prediction",
        "current_confidence_percent",
        "current_correct",
        "baseline_gradcam_max",
        "current_gradcam_max",
        "panel_file",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            writer.writerow(
                {
                    "rank": rank,
                    "case_type": row["case_type"],
                    "image": row["image"],
                    "true_label": row["true_label"],
                    "baseline_prediction": row["baseline_prediction"],
                    "baseline_confidence_percent": f"{row['baseline_confidence'] * 100:.4f}",
                    "baseline_correct": row["baseline_correct"],
                    "current_prediction": row["current_prediction"],
                    "current_confidence_percent": f"{row['current_confidence'] * 100:.4f}",
                    "current_correct": row["current_correct"],
                    "baseline_gradcam_max": f"{row['baseline_gradcam_max']:.6f}",
                    "current_gradcam_max": f"{row['current_gradcam_max']:.6f}",
                    "panel_file": row["panel_file"],
                }
            )


def write_summary(rows: List[Dict[str, object]], output_path: Path, threshold: float) -> None:
    lines = [
        "# XAI Decision Comparison Summary",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "This evidence pack compares the baseline EfficientNetB0 model against the current V4 Robust EfficientNetB0 ensemble on curated held-out test images.",
        "",
        "Grad-CAM is used as post-prediction explainability evidence. It does not change the prediction or confidence score. The heatmap shows which regions most supported the predicted class for each model.",
        "",
        "## How to Read the Panels",
        "",
        f"- {BASELINE_DISPLAY_NAME} prediction only: the base model decision without visual explanation.",
        f"- {BASELINE_DISPLAY_NAME} Grad-CAM: the image regions supporting the baseline predicted class.",
        f"- {CURRENT_DISPLAY_NAME} prediction only: the current ensemble decision without visual explanation.",
        f"- {CURRENT_DISPLAY_NAME} Grad-CAM: the averaged visual evidence from the current ensemble.",
        "",
        "## Selected Cases",
        "",
    ]

    for row in rows:
        baseline_status = "correct" if row["baseline_correct"] else "wrong"
        current_status = "correct" if row["current_correct"] else "wrong"
        lines.append(
            "- "
            f"`{row['image']}` ({row['case_type']}): true `{row['true_label']}`; "
            f"{BASELINE_DISPLAY_NAME} predicted `{row['baseline_prediction']}` at {fmt_conf(row['baseline_confidence'])} ({baseline_status}); "
            f"{CURRENT_DISPLAY_NAME} predicted `{row['current_prediction']}` at {fmt_conf(row['current_confidence'])} ({current_status})."
        )

    lines.extend(
        [
            "",
            "## Thesis Interpretation",
            "",
            "Use these panels to explain how the model reached its coral-health decision. A useful defence statement is: the classification output tells us what the model decided, while Grad-CAM helps inspect whether the decision is visually grounded in coral-relevant regions instead of background artifacts.",
            "",
            f"The uncertainty reference threshold used for selecting challenging examples is {threshold:.1f}% current-model confidence.",
            "",
            "Do not claim that Grad-CAM improves benchmark accuracy. It supports interpretability and trust analysis after the model has already made a decision.",
        ]
    )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_generated_rows(rows: List[Dict[str, object]]) -> None:
    labels = {row["true_label"] for row in rows}
    missing = [name for name in CLASS_NAMES if name not in labels]
    if missing:
        raise RuntimeError(f"Curated output missing required true labels: {missing}")

    empty_baseline = [row["image"] for row in rows if row["baseline_gradcam_max"] <= 0]
    empty_current = [row["image"] for row in rows if row["current_gradcam_max"] <= 0]
    if empty_baseline or empty_current:
        raise RuntimeError(
            "One or more Grad-CAM overlays were empty. "
            f"Baseline empty: {empty_baseline}; current empty: {empty_current}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate defence-ready baseline/current XAI comparison panels."
    )
    parser.add_argument(
        "--uncertain-threshold",
        type=float,
        default=DEFAULT_UNCERTAIN_THRESHOLD,
        help="Current-model confidence percentage used to select uncertain examples.",
    )
    parser.add_argument(
        "--max-challenges",
        type=int,
        default=3,
        help="Maximum challenging examples to add after the three class representatives.",
    )
    args = parser.parse_args()

    prepare_output_dirs()

    print("=" * 72)
    print("XAI Decision Comparison: Baseline vs Current EfficientNetB0")
    print("=" * 72)
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Output dir:   {OUTPUT_DIR}")

    print("\nLoading held-out test split...")
    x_test, y_true, rel_paths, abs_paths = load_test_split()
    print(f"  Loaded {len(x_test)} test images from {SPLIT_INFO_PATH}")

    print("\nLoading baseline model...")
    baseline_model = load_baseline()
    print(f"  Loaded: {BASELINE_MODEL_PATH.name}")

    print("\nLoading current V4 Robust ensemble...")
    current_models = load_current_models()
    print(f"  Loaded {len(current_models)} current-model checkpoints")

    print("\nRunning predictions...")
    baseline_probs = baseline_model.predict(x_test, batch_size=16, verbose=0)
    current_probs = predict_current_ensemble(current_models, x_test)
    rows = build_result_rows(y_true, rel_paths, baseline_probs, current_probs)

    selected_rows = select_curated_rows(
        rows,
        uncertain_threshold=args.uncertain_threshold,
        max_challenges=args.max_challenges,
    )
    print(f"  Selected {len(selected_rows)} curated examples")

    print("\nGenerating Grad-CAM panels...")
    panel_paths: List[Path] = []
    enriched_rows: List[Dict[str, object]] = []
    for rank, row in enumerate(selected_rows, start=1):
        image = x_test[int(row["index"])]
        baseline_heatmap = make_gradcam_heatmap(
            image,
            baseline_model,
            int(row["baseline_idx"]),
        )
        current_heatmap = make_current_ensemble_heatmap(
            image,
            current_models,
            int(row["current_idx"]),
        )

        image_id = Path(str(row["image"]).replace("\\", "/")).with_suffix("")
        panel_name = f"{rank:02d}_{row['case_type']}_{slugify(str(image_id))}.png"
        panel_path = PANELS_DIR / panel_name

        row = dict(row)
        row["source_path"] = str(abs_paths[int(row["index"])])
        row["baseline_gradcam_max"] = float(np.max(baseline_heatmap))
        row["current_gradcam_max"] = float(np.max(current_heatmap))
        row["panel_file"] = f"panels/{panel_name}"

        save_four_panel(row, image, baseline_heatmap, current_heatmap, panel_path)
        panel_paths.append(panel_path)
        enriched_rows.append(row)
        print(f"  Saved panel: {panel_name}")

    validate_generated_rows(enriched_rows)

    print("\nWriting CSV, contact sheet, and summary...")
    write_results_csv(enriched_rows, OUTPUT_DIR / "xai_decision_results.csv")
    create_contact_sheet(panel_paths, OUTPUT_DIR / "xai_decision_contact_sheet.png")
    write_summary(
        enriched_rows,
        OUTPUT_DIR / "xai_decision_summary.md",
        threshold=args.uncertain_threshold,
    )

    print("\nGenerated files:")
    print(f"  {PANELS_DIR}")
    print(f"  {OUTPUT_DIR / 'xai_decision_contact_sheet.png'}")
    print(f"  {OUTPUT_DIR / 'xai_decision_results.csv'}")
    print(f"  {OUTPUT_DIR / 'xai_decision_summary.md'}")
    print("\nDone.")

    del baseline_model
    for model in current_models:
        del model
    tf.keras.backend.clear_session()
    gc.collect()


if __name__ == "__main__":
    main()
