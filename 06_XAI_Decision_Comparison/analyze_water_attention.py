import argparse
import csv
import gc
import json
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import cv2
import matplotlib
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


IMG_SIZE = 224
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
DEFAULT_SEEDS = [42, 43, 44, 45, 46]
CAM_MODES = ["vanilla", "eigen", "aug_eigen"]
COUNTERFACTUAL_DROP_THRESHOLD = 10.0

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATASET_DIR = PROJECT_ROOT / "Dataset"
SPLIT_INFO_PATH = PROJECT_ROOT / "05_Baseline_Model" / "split_info_v3.json"
MODEL_DIR = PROJECT_ROOT / "02_Modelling" / "efficientnetb0_coral" / "models"
OUTPUT_DIR = SCRIPT_DIR / "outputs" / "water_attention_audit"
PANELS_DIR = OUTPUT_DIR / "panels"

MASK_PRESETS: Dict[str, Dict[str, int]] = {
    "default": {
        "h_min": 75,
        "h_max": 135,
        "s_min": 20,
        "v_min": 35,
        "blue_delta": 8,
        "green_delta": 2,
    },
    "strict_blue": {
        "h_min": 85,
        "h_max": 125,
        "s_min": 40,
        "v_min": 45,
        "blue_delta": 15,
        "green_delta": 5,
    },
    "broad_cyan": {
        "h_min": 65,
        "h_max": 145,
        "s_min": 15,
        "v_min": 30,
        "blue_delta": 2,
        "green_delta": 0,
    },
    "high_saturation": {
        "h_min": 75,
        "h_max": 135,
        "s_min": 55,
        "v_min": 45,
        "blue_delta": 8,
        "green_delta": 2,
    },
}


def parse_seed_list(raw: str) -> List[int]:
    seeds = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if not seeds:
        raise ValueError("At least one seed is required")
    return seeds


def build_current_model() -> tf.keras.Model:
    """Canonical Chapter 4 loader for the 98.11% benchmark."""
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


def load_test_split(max_images: int = 0) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    with SPLIT_INFO_PATH.open("r", encoding="utf-8") as f:
        split_info = json.load(f)

    images: List[np.ndarray] = []
    labels: List[int] = []
    rel_paths: List[str] = []
    test_files = split_info["test_files"]
    if max_images > 0:
        test_files = test_files[:max_images]

    for relative_name in test_files:
        normalized = relative_name.replace("\\", "/")
        label_name = normalized.split("/")[0]
        if label_name not in CLASS_NAMES:
            raise ValueError(f"Unknown class in split entry: {relative_name}")

        path = resolve_dataset_path(normalized)
        img_bgr = cv2.imread(str(path))
        if img_bgr is None:
            raise RuntimeError(f"Could not read image: {path}")

        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)
        images.append(img_rgb.astype("float32"))
        labels.append(CLASS_NAMES.index(label_name))
        rel_paths.append(normalized)

    return (
        np.asarray(images, dtype="float32"),
        np.asarray(labels, dtype=np.int32),
        rel_paths,
    )


def load_model_for_seed(seed: int) -> tf.keras.Model:
    path = MODEL_DIR / f"efficientnetb0_v4robust_seed{seed}_swa.h5"
    if not path.exists():
        fallback = MODEL_DIR / f"efficientnetb0_v4robust_seed{seed}_swa.weights.h5"
        if fallback.exists():
            path = fallback
    if not path.exists():
        raise FileNotFoundError(f"Current model weights not found for seed {seed}: {path}")

    model = build_current_model()
    model.load_weights(str(path))
    return model


def find_efficientnet(model: tf.keras.Model) -> tf.keras.Model:
    for layer in model.layers:
        if "efficientnet" in layer.name.lower():
            return layer
    raise RuntimeError("EfficientNet layer not found")


def find_target_layer(efficientnet: tf.keras.Model, layer_name: str = "top_conv") -> tf.keras.layers.Layer:
    try:
        return efficientnet.get_layer(layer_name)
    except Exception:
        for layer in reversed(efficientnet.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer
    raise RuntimeError("No convolution layer found for Grad-CAM")


def normalize_heatmap(heatmap: np.ndarray) -> np.ndarray:
    heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
    max_value = float(np.max(heatmap))
    if max_value > 0:
        heatmap = heatmap / max_value
    return heatmap.astype("float32")


def compute_gradcam_vanilla_and_eigen(
    image: np.ndarray,
    model: tf.keras.Model,
    class_idx: int,
) -> Tuple[np.ndarray, np.ndarray]:
    efficientnet = find_efficientnet(model)
    target_layer = find_target_layer(efficientnet)
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
        empty = np.zeros((IMG_SIZE, IMG_SIZE), dtype="float32")
        return empty, empty

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out_tf = conv_outputs[0]

    vanilla = conv_out_tf @ pooled_grads[..., tf.newaxis]
    vanilla = tf.squeeze(vanilla)
    vanilla = tf.nn.relu(vanilla).numpy()

    weights = pooled_grads.numpy()
    conv_np = conv_out_tf.numpy()
    standard_heatmap = np.sum(conv_np * weights, axis=-1)
    weighted_activations = conv_np * weights[np.newaxis, np.newaxis, :]
    h, w, c = weighted_activations.shape
    reshaped = weighted_activations.reshape(h * w, c)
    u, s, _ = np.linalg.svd(reshaped, full_matrices=False)
    eigen = (u[:, 0] * s[0]).reshape(h, w)
    if float(np.sum(eigen * standard_heatmap)) < 0:
        eigen = -eigen
    eigen = np.maximum(eigen, 0)

    return normalize_heatmap(vanilla), normalize_heatmap(eigen)


def compute_aug_eigen_heatmap(image: np.ndarray, model: tf.keras.Model, class_idx: int) -> np.ndarray:
    heatmaps: List[np.ndarray] = []
    for flip in [False, True]:
        for brightness in [1.0, 1.1, 0.9]:
            augmented = np.clip(image.copy() * brightness, 0, 255)
            if flip:
                augmented = np.flip(augmented, axis=1).copy()
            _, eigen = compute_gradcam_vanilla_and_eigen(augmented, model, class_idx)
            if flip:
                eigen = np.flip(eigen, axis=1).copy()
            heatmaps.append(eigen)

    avg = np.mean(heatmaps, axis=0)
    max_value = float(np.max(avg))
    if max_value > 0:
        avg = avg / max_value
    return avg.astype("float32")


def sea_water_colour_mask(image_rgb: np.ndarray, preset: Optional[Dict[str, int]] = None) -> np.ndarray:
    """Approximate blue/cyan sea-water coloured pixels.

    This is a colour heuristic, not a ground-truth segmentation mask.
    """
    cfg = preset or MASK_PRESETS["default"]
    image_u8 = np.clip(image_rgb, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(image_u8, cv2.COLOR_RGB2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    r = image_u8[:, :, 0].astype(np.int16)
    g = image_u8[:, :, 1].astype(np.int16)
    b = image_u8[:, :, 2].astype(np.int16)

    cyan_blue_hue = (h >= cfg["h_min"]) & (h <= cfg["h_max"])
    visible_colour = (s >= cfg["s_min"]) & (v >= cfg["v_min"])
    red_suppressed = (b >= r + cfg["blue_delta"]) & (g >= r + cfg["green_delta"])
    mask = cyan_blue_hue & visible_colour & red_suppressed

    mask_u8 = mask.astype(np.uint8) * 255
    kernel = np.ones((3, 3), dtype=np.uint8)
    mask_u8 = cv2.morphologyEx(mask_u8, cv2.MORPH_OPEN, kernel)
    mask_u8 = cv2.morphologyEx(mask_u8, cv2.MORPH_CLOSE, kernel)
    return mask_u8 > 0


def measure_attention_with_mask(heatmap: np.ndarray, water: np.ndarray) -> Dict[str, float]:
    total_pixels = float(water.size)
    water_pixels = float(np.sum(water))
    water_area_fraction = water_pixels / total_pixels if total_pixels else 0.0

    heatmap_sum = float(np.sum(heatmap))
    if heatmap_sum <= 0:
        water_attention_mass = 0.0
        top20_water_fraction = 0.0
        top10_water_fraction = 0.0
    else:
        water_attention_mass = float(np.sum(heatmap[water])) / heatmap_sum
        top20_threshold = float(np.quantile(heatmap, 0.80))
        top10_threshold = float(np.quantile(heatmap, 0.90))
        top20 = heatmap >= top20_threshold
        top10 = heatmap >= top10_threshold
        top20_water_fraction = float(np.mean(water[top20])) if np.any(top20) else 0.0
        top10_water_fraction = float(np.mean(water[top10])) if np.any(top10) else 0.0

    nonwater = ~water
    water_density = float(np.mean(heatmap[water])) if np.any(water) else 0.0
    nonwater_density = float(np.mean(heatmap[nonwater])) if np.any(nonwater) else 0.0
    density_ratio = water_density / nonwater_density if nonwater_density > 0 else 0.0
    enrichment = water_attention_mass / water_area_fraction if water_area_fraction > 0 else 0.0

    return {
        "water_area_fraction": water_area_fraction,
        "water_attention_mass": water_attention_mass,
        "water_attention_enrichment": enrichment,
        "water_density": water_density,
        "nonwater_density": nonwater_density,
        "water_density_ratio": density_ratio,
        "top20_water_fraction": top20_water_fraction,
        "top10_water_fraction": top10_water_fraction,
    }


def measure_attention(image: np.ndarray, heatmap: np.ndarray, mask_name: str = "default") -> Dict[str, float]:
    return measure_attention_with_mask(heatmap, sea_water_colour_mask(image, MASK_PRESETS[mask_name]))


def create_overlay(image: np.ndarray, heatmap: np.ndarray, alpha: float = 0.40) -> np.ndarray:
    image_u8 = np.clip(image, 0, 255).astype(np.uint8)
    heatmap_u8 = np.uint8(255 * np.clip(heatmap, 0, 1))
    coloured = cv2.applyColorMap(heatmap_u8, cv2.COLORMAP_JET)
    coloured = cv2.cvtColor(coloured, cv2.COLOR_BGR2RGB)
    return cv2.addWeighted(image_u8, 1.0 - alpha, coloured, alpha, 0)


def neutralize_water(image: np.ndarray, water: np.ndarray) -> np.ndarray:
    output = np.clip(image, 0, 255).astype(np.float32).copy()
    nonwater = ~water
    if np.any(nonwater):
        fill = np.median(output[nonwater], axis=0)
    else:
        fill = np.asarray([128.0, 128.0, 128.0], dtype=np.float32)
    output[water] = fill
    return output


def shift_water_colour(image: np.ndarray, water: np.ndarray) -> np.ndarray:
    image_u8 = np.clip(image, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(image_u8, cv2.COLOR_RGB2HSV).astype(np.int16)
    hsv[:, :, 0][water] = (hsv[:, :, 0][water] + 45) % 180
    hsv[:, :, 1][water] = np.clip(hsv[:, :, 1][water] * 0.65, 0, 255)
    shifted = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    return shifted.astype("float32")


def summarize(values: Iterable[float]) -> Dict[str, float]:
    arr = np.asarray(list(values), dtype="float64")
    if arr.size == 0:
        return {"mean": 0.0, "median": 0.0, "p75": 0.0, "max": 0.0}
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "p75": float(np.quantile(arr, 0.75)),
        "max": float(np.max(arr)),
    }


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def fmt_float(value: float) -> str:
    return f"{value:.3f}"


def classify_row(row: Dict[str, object]) -> None:
    row["majority_attention_on_water"] = bool(float(row["water_attention_mass"]) >= 0.50)
    row["top20_majority_water"] = bool(float(row["top20_water_fraction"]) >= 0.50)
    row["area_adjusted_water_bias"] = bool(float(row["water_attention_enrichment"]) > 1.0)


def build_rows(
    images: np.ndarray,
    y_true: np.ndarray,
    rel_paths: List[str],
    ensemble_probs: np.ndarray,
    heatmaps: np.ndarray,
    cam_mode: str,
    mask_name: str = "default",
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    y_pred = np.argmax(ensemble_probs, axis=1)
    confidence = np.max(ensemble_probs, axis=1)

    for idx, (image, heatmap) in enumerate(zip(images, heatmaps)):
        metrics = measure_attention(image, heatmap, mask_name=mask_name)
        row: Dict[str, object] = {
            "index": idx,
            "image": rel_paths[idx],
            "true_label": CLASS_NAMES[int(y_true[idx])],
            "predicted_label": CLASS_NAMES[int(y_pred[idx])],
            "confidence_percent": float(confidence[idx] * 100.0),
            "correct": bool(int(y_pred[idx]) == int(y_true[idx])),
            "cam_mode": cam_mode,
            "mask_name": mask_name,
            **metrics,
        }
        classify_row(row)
        rows.append(row)
    return rows


def summarize_rows(rows: List[Dict[str, object]]) -> Dict[str, object]:
    total = len(rows)
    correct = sum(1 for row in rows if row["correct"])
    majority = sum(1 for row in rows if row["majority_attention_on_water"])
    top20_majority = sum(1 for row in rows if row["top20_majority_water"])
    adjusted_bias = sum(1 for row in rows if row["area_adjusted_water_bias"])
    water_area = summarize(float(row["water_area_fraction"]) for row in rows)
    water_mass = summarize(float(row["water_attention_mass"]) for row in rows)
    enrichment = summarize(float(row["water_attention_enrichment"]) for row in rows)
    top20 = summarize(float(row["top20_water_fraction"]) for row in rows)

    by_class: Dict[str, Dict[str, float]] = {}
    for class_name in CLASS_NAMES:
        subset = [row for row in rows if row["predicted_label"] == class_name]
        if not subset:
            continue
        by_class[class_name] = {
            "count": len(subset),
            "majority_attention_on_water": sum(
                1 for row in subset if row["majority_attention_on_water"]
            )
            / len(subset),
            "area_adjusted_water_bias": sum(
                1 for row in subset if row["area_adjusted_water_bias"]
            )
            / len(subset),
            "median_water_attention_mass": float(
                np.median([float(row["water_attention_mass"]) for row in subset])
            ),
            "median_enrichment": float(
                np.median([float(row["water_attention_enrichment"]) for row in subset])
            ),
        }

    return {
        "test_images": total,
        "correct_predictions": correct,
        "accuracy": correct / total if total else 0.0,
        "probability_majority_cam_attention_on_water": majority / total if total else 0.0,
        "probability_top20_cam_pixels_majority_water": top20_majority / total if total else 0.0,
        "probability_area_adjusted_water_bias": adjusted_bias / total if total else 0.0,
        "water_area_fraction": water_area,
        "water_attention_mass": water_mass,
        "water_attention_enrichment": enrichment,
        "top20_water_fraction": top20,
        "by_predicted_class": by_class,
    }


def row_for_csv(row: Dict[str, object], include_mode: bool = False) -> Dict[str, object]:
    fields = {
        "index": row["index"],
        "image": row["image"],
        "true_label": row["true_label"],
        "predicted_label": row["predicted_label"],
        "confidence_percent": row["confidence_percent"],
        "correct": row["correct"],
        "water_area_fraction": row["water_area_fraction"],
        "water_attention_mass": row["water_attention_mass"],
        "water_attention_enrichment": row["water_attention_enrichment"],
        "water_density_ratio": row["water_density_ratio"],
        "top20_water_fraction": row["top20_water_fraction"],
        "top10_water_fraction": row["top10_water_fraction"],
        "majority_attention_on_water": row["majority_attention_on_water"],
        "top20_majority_water": row["top20_majority_water"],
        "area_adjusted_water_bias": row["area_adjusted_water_bias"],
    }
    if include_mode:
        fields = {"cam_mode": row["cam_mode"], "mask_name": row["mask_name"], **fields}
    return fields


def write_dicts_csv(path: Path, rows: List[Dict[str, object]], fieldnames: Optional[List[str]] = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def create_masked_datasets(images: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    masked: List[np.ndarray] = []
    shifted: List[np.ndarray] = []
    for image in images:
        water = sea_water_colour_mask(image, MASK_PRESETS["default"])
        masked.append(neutralize_water(image, water))
        shifted.append(shift_water_colour(image, water))
    return np.asarray(masked, dtype="float32"), np.asarray(shifted, dtype="float32")


def build_counterfactual_rows(
    y_true: np.ndarray,
    rel_paths: List[str],
    base_probs: np.ndarray,
    masked_probs: np.ndarray,
    shifted_probs: np.ndarray,
    vanilla_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    vanilla_by_index = {int(row["index"]): row for row in vanilla_rows}
    for idx, rel_path in enumerate(rel_paths):
        target_idx = int(np.argmax(base_probs[idx]))
        base_conf = float(base_probs[idx][target_idx] * 100.0)
        masked_target_conf = float(masked_probs[idx][target_idx] * 100.0)
        shifted_target_conf = float(shifted_probs[idx][target_idx] * 100.0)
        masked_pred_idx = int(np.argmax(masked_probs[idx]))
        shifted_pred_idx = int(np.argmax(shifted_probs[idx]))
        masked_drop = base_conf - masked_target_conf
        shifted_drop = base_conf - shifted_target_conf
        largest_drop = max(masked_drop, shifted_drop)
        label_changed = masked_pred_idx != target_idx or shifted_pred_idx != target_idx
        row = {
            "index": idx,
            "image": rel_path,
            "true_label": CLASS_NAMES[int(y_true[idx])],
            "original_prediction": CLASS_NAMES[target_idx],
            "original_confidence_percent": base_conf,
            "water_masked_prediction": CLASS_NAMES[masked_pred_idx],
            "water_masked_target_confidence_percent": masked_target_conf,
            "water_masked_confidence_drop_pp": masked_drop,
            "water_shifted_prediction": CLASS_NAMES[shifted_pred_idx],
            "water_shifted_target_confidence_percent": shifted_target_conf,
            "water_shifted_confidence_drop_pp": shifted_drop,
            "largest_confidence_drop_pp": largest_drop,
            "prediction_changed_after_counterfactual": label_changed,
            "counterfactual_sensitive": bool(
                label_changed or largest_drop >= COUNTERFACTUAL_DROP_THRESHOLD
            ),
            "water_attention_mass": vanilla_by_index[idx]["water_attention_mass"],
            "water_attention_enrichment": vanilla_by_index[idx]["water_attention_enrichment"],
        }
        rows.append(row)
    return rows


def counterfactual_summary(rows: List[Dict[str, object]]) -> Dict[str, object]:
    total = len(rows)
    sensitive = sum(1 for row in rows if row["counterfactual_sensitive"])
    changed = sum(1 for row in rows if row["prediction_changed_after_counterfactual"])
    masked_drops = summarize(float(row["water_masked_confidence_drop_pp"]) for row in rows)
    shifted_drops = summarize(float(row["water_shifted_confidence_drop_pp"]) for row in rows)
    largest_drops = summarize(float(row["largest_confidence_drop_pp"]) for row in rows)
    by_prediction: Dict[str, Dict[str, float]] = {}
    for class_name in CLASS_NAMES:
        subset = [row for row in rows if row["original_prediction"] == class_name]
        if not subset:
            continue
        by_prediction[class_name] = {
            "count": len(subset),
            "counterfactual_sensitive": sum(
                1 for row in subset if row["counterfactual_sensitive"]
            )
            / len(subset),
            "prediction_changed_after_counterfactual": sum(
                1 for row in subset if row["prediction_changed_after_counterfactual"]
            )
            / len(subset),
            "median_largest_confidence_drop_pp": float(
                np.median([float(row["largest_confidence_drop_pp"]) for row in subset])
            ),
        }
    return {
        "test_images": total,
        "probability_counterfactual_sensitive": sensitive / total if total else 0.0,
        "probability_prediction_changed": changed / total if total else 0.0,
        "masked_confidence_drop_pp": masked_drops,
        "shifted_confidence_drop_pp": shifted_drops,
        "largest_confidence_drop_pp": largest_drops,
        "by_original_prediction": by_prediction,
    }


def build_mask_sensitivity(
    images: np.ndarray,
    heatmaps_by_mode: Dict[str, np.ndarray],
    mode_rows: Dict[str, List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    summaries: List[Dict[str, object]] = []
    base_meta = {
        mode: {
            int(row["index"]): {
                "true_label": row["true_label"],
                "predicted_label": row["predicted_label"],
                "confidence_percent": row["confidence_percent"],
                "correct": row["correct"],
            }
            for row in rows
        }
        for mode, rows in mode_rows.items()
    }
    for mode, heatmaps in heatmaps_by_mode.items():
        for mask_name, preset in MASK_PRESETS.items():
            rows: List[Dict[str, object]] = []
            for idx, (image, heatmap) in enumerate(zip(images, heatmaps)):
                metrics = measure_attention_with_mask(heatmap, sea_water_colour_mask(image, preset))
                row: Dict[str, object] = {
                    "index": idx,
                    "cam_mode": mode,
                    "mask_name": mask_name,
                    **base_meta[mode][idx],
                    **metrics,
                }
                classify_row(row)
                rows.append(row)
            summary = summarize_rows(rows)
            bleached = summary["by_predicted_class"].get("Bleached", {})
            summaries.append(
                {
                    "cam_mode": mode,
                    "mask_name": mask_name,
                    "majority_water_cam_percent": summary[
                        "probability_majority_cam_attention_on_water"
                    ]
                    * 100.0,
                    "top20_majority_water_percent": summary[
                        "probability_top20_cam_pixels_majority_water"
                    ]
                    * 100.0,
                    "area_adjusted_water_bias_percent": summary[
                        "probability_area_adjusted_water_bias"
                    ]
                    * 100.0,
                    "median_water_area_percent": summary["water_area_fraction"]["median"] * 100.0,
                    "median_water_cam_mass_percent": summary["water_attention_mass"]["median"] * 100.0,
                    "bleached_majority_water_cam_percent": float(
                        bleached.get("majority_attention_on_water", 0.0)
                    )
                    * 100.0,
                    "bleached_median_water_cam_mass_percent": float(
                        bleached.get("median_water_attention_mass", 0.0)
                    )
                    * 100.0,
                    "median_enrichment": summary["water_attention_enrichment"]["median"],
                }
            )
    return summaries


def save_attention_panel(
    rows: List[Dict[str, object]],
    images: np.ndarray,
    heatmaps: np.ndarray,
    filename: str,
    title: str,
) -> None:
    if not rows:
        return
    cols = min(3, len(rows))
    row_count = int(np.ceil(len(rows) / cols))
    fig, axes = plt.subplots(row_count, cols, figsize=(5 * cols, 4.8 * row_count), facecolor="white")
    axes_arr = np.asarray(axes).reshape(-1)
    for ax, row in zip(axes_arr, rows):
        idx = int(row["index"])
        overlay = create_overlay(images[idx], heatmaps[idx])
        ax.imshow(overlay)
        ax.set_title(
            f"{row['image']}\n"
            f"pred {row['predicted_label']} {float(row['confidence_percent']):.1f}% | "
            f"water CAM {float(row['water_attention_mass']):.2f} | "
            f"enrich {float(row['water_attention_enrichment']):.2f}",
            fontsize=9,
        )
        ax.axis("off")
    for ax in axes_arr[len(rows) :]:
        ax.axis("off")
    fig.suptitle(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(PANELS_DIR / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_mode_comparison_panel(
    risky_rows: List[Dict[str, object]],
    images: np.ndarray,
    heatmaps_by_mode: Dict[str, np.ndarray],
) -> None:
    if not risky_rows:
        return
    selected = risky_rows[:3]
    available_modes = list(heatmaps_by_mode.keys())
    fig, axes = plt.subplots(
        len(selected),
        len(available_modes) + 1,
        figsize=(4 * (len(available_modes) + 1), 4.3 * len(selected)),
        facecolor="white",
    )
    axes_arr = np.asarray(axes)
    for row_idx, row in enumerate(selected):
        idx = int(row["index"])
        axes_arr[row_idx, 0].imshow(np.clip(images[idx], 0, 255).astype(np.uint8))
        axes_arr[row_idx, 0].set_title(f"{row['image']}\nOriginal", fontsize=9)
        axes_arr[row_idx, 0].axis("off")
        for mode_idx, mode in enumerate(available_modes, start=1):
            overlay = create_overlay(images[idx], heatmaps_by_mode[mode][idx])
            axes_arr[row_idx, mode_idx].imshow(overlay)
            axes_arr[row_idx, mode_idx].set_title(mode.replace("_", "+"), fontsize=9)
            axes_arr[row_idx, mode_idx].axis("off")
    fig.suptitle("CAM Mode Comparison on Highest Water-Attention Cases", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(PANELS_DIR / "cam_mode_comparison_examples.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def save_counterfactual_panel(
    rows: List[Dict[str, object]],
    images: np.ndarray,
    masked_images: np.ndarray,
    shifted_images: np.ndarray,
    heatmaps: np.ndarray,
) -> None:
    if not rows:
        return
    selected = rows[:4]
    fig, axes = plt.subplots(len(selected), 4, figsize=(16, 4.0 * len(selected)), facecolor="white")
    axes_arr = np.asarray(axes)
    for row_idx, row in enumerate(selected):
        idx = int(row["index"])
        views = [
            (np.clip(images[idx], 0, 255).astype(np.uint8), "Original"),
            (create_overlay(images[idx], heatmaps[idx]), "Vanilla CAM"),
            (np.clip(masked_images[idx], 0, 255).astype(np.uint8), "Water masked"),
            (np.clip(shifted_images[idx], 0, 255).astype(np.uint8), "Water shifted"),
        ]
        for col_idx, (img, title) in enumerate(views):
            axes_arr[row_idx, col_idx].imshow(img)
            if col_idx == 0:
                title = (
                    f"{row['image']}\n"
                    f"drop {float(row['largest_confidence_drop_pp']):.1f} pp | {title}"
                )
            axes_arr[row_idx, col_idx].set_title(title, fontsize=9)
            axes_arr[row_idx, col_idx].axis("off")
    fig.suptitle("Counterfactual Water-Region Perturbation Examples", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(PANELS_DIR / "counterfactual_water_region_examples.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def prepare_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PANELS_DIR.mkdir(parents=True, exist_ok=True)
    for name in [
        "highest_water_attention.png",
        "lowest_water_attention.png",
        "highest_area_adjusted_water_bias.png",
        "cam_mode_comparison_examples.png",
        "counterfactual_water_region_examples.png",
    ]:
        path = PANELS_DIR / name
        if path.exists():
            path.unlink()


def write_summary_files(
    seeds: List[int],
    mode_summaries: Dict[str, Dict[str, object]],
    mask_sensitivity: List[Dict[str, object]],
    counter_rows: List[Dict[str, object]],
    counter_summary: Dict[str, object],
    mode_rows: Dict[str, List[Dict[str, object]]],
) -> None:
    vanilla = mode_summaries["vanilla"]
    by_class = vanilla["by_predicted_class"]
    bleached = by_class.get("Bleached", {})
    risky = sorted(
        mode_rows["vanilla"],
        key=lambda row: float(row["water_attention_mass"]),
        reverse=True,
    )[:8]
    counter_risky = sorted(
        counter_rows,
        key=lambda row: float(row["largest_confidence_drop_pp"]),
        reverse=True,
    )[:8]

    summary_payload = {
        "seeds": seeds,
        "model_artifacts": "02_Modelling/efficientnetb0_coral/models/efficientnetb0_v4robust_seed{seed}_swa.h5",
        "canonical_accuracy_check": vanilla["accuracy"],
        "cam_mode_summaries": mode_summaries,
        "mask_sensitivity_summary": mask_sensitivity,
        "counterfactual_summary": counter_summary,
        "acceptance_targets_for_future_model": {
            "overall_majority_water_cam_below": 0.25,
            "bleached_majority_water_cam_below": 0.35,
            "accuracy_near_current_benchmark": 0.9811,
        },
    }
    with (OUTPUT_DIR / "water_attention_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary_payload, f, indent=2)

    lines = [
        "# Sea-Water Colour Attention Evidence Pack",
        "",
        "This evidence pack tests whether the current canonical EfficientNetB0 ensemble depends on blue/cyan sea-water coloured regions. It does not modify or retrain any model.",
        "",
        "Important limitation: water regions are detected by HSV/RGB colour heuristics, not human-labelled segmentation masks. Treat the results as shortcut-risk evidence, not definitive pixel-level ground truth.",
        "",
        "## Canonical Check",
        "",
        f"- Model: 5-seed SWA EfficientNetB0 ensemble, seeds `{', '.join(str(seed) for seed in seeds)}`.",
        "- Checkpoints: `02_Modelling/efficientnetb0_coral/models/efficientnetb0_v4robust_seed{seed}_swa.h5`.",
        "- Architecture loader: canonical Chapter 4 path from `02_Modelling/efficientnetb0_coral/replot_evaluation.py`.",
        f"- Accuracy reproduced by this audit: **{pct(float(vanilla['accuracy']))}** ({int(vanilla['correct_predictions'])}/{int(vanilla['test_images'])}).",
        "",
        "## CAM Mode Comparison",
        "",
        "| CAM mode | Overall majority water CAM | Bleached majority water CAM | Area-adjusted water bias | Median water CAM mass |",
        "|---|---:|---:|---:|---:|",
    ]
    for mode in mode_summaries:
        summary = mode_summaries[mode]
        class_summary = summary["by_predicted_class"].get("Bleached", {})
        lines.append(
            f"| {mode.replace('_', '+')} | "
            f"{pct(float(summary['probability_majority_cam_attention_on_water']))} | "
            f"{pct(float(class_summary.get('majority_attention_on_water', 0.0)))} | "
            f"{pct(float(summary['probability_area_adjusted_water_bias']))} | "
            f"{pct(float(summary['water_attention_mass']['median']))} |"
        )

    lines.extend(
        [
            "",
            "## Mask Sensitivity",
            "",
            "| Mask preset | CAM mode | Overall majority water CAM | Bleached majority water CAM | Median water area | Median enrichment |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in mask_sensitivity:
        if row["cam_mode"] != "vanilla":
            continue
        lines.append(
            f"| {row['mask_name']} | {row['cam_mode']} | "
            f"{float(row['majority_water_cam_percent']):.2f}% | "
            f"{float(row['bleached_majority_water_cam_percent']):.2f}% | "
            f"{float(row['median_water_area_percent']):.2f}% | "
            f"{float(row['median_enrichment']):.3f}x |"
        )

    lines.extend(
        [
            "",
            "## Counterfactual Water-Region Tests",
            "",
            "Water-colour pixels were either neutralized to the image's non-water median colour or hue-shifted/desaturated. Sensitivity means the predicted label changed or the original predicted class dropped by at least 10 percentage points.",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Counterfactual-sensitive images | {pct(float(counter_summary['probability_counterfactual_sensitive']))} |",
            f"| Prediction changed after water perturbation | {pct(float(counter_summary['probability_prediction_changed']))} |",
            f"| Median largest confidence drop | {float(counter_summary['largest_confidence_drop_pp']['median']):.2f} pp |",
            f"| 75th percentile largest confidence drop | {float(counter_summary['largest_confidence_drop_pp']['p75']):.2f} pp |",
            "",
            "| Original prediction | Count | Counterfactual sensitive | Label changed | Median largest drop |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for class_name, data in counter_summary["by_original_prediction"].items():
        lines.append(
            f"| {class_name} | {int(data['count'])} | "
            f"{pct(float(data['counterfactual_sensitive']))} | "
            f"{pct(float(data['prediction_changed_after_counterfactual']))} | "
            f"{float(data['median_largest_confidence_drop_pp']):.2f} pp |"
        )

    lines.extend(
        [
            "",
            "## Highest Water-Attention Examples",
            "",
            "| Image | True | Predicted | Confidence | Water CAM mass | Enrichment |",
            "|---|---|---|---:|---:|---:|",
        ]
    )
    for row in risky:
        lines.append(
            f"| {row['image']} | {row['true_label']} | {row['predicted_label']} | "
            f"{float(row['confidence_percent']):.2f}% | "
            f"{pct(float(row['water_attention_mass']))} | "
            f"{fmt_float(float(row['water_attention_enrichment']))}x |"
        )

    lines.extend(
        [
            "",
            "## Largest Counterfactual Drops",
            "",
            "| Image | Original prediction | Original confidence | Mask drop | Shift drop | Label changed |",
            "|---|---|---:|---:|---:|---|",
        ]
    )
    for row in counter_risky:
        lines.append(
            f"| {row['image']} | {row['original_prediction']} | "
            f"{float(row['original_confidence_percent']):.2f}% | "
            f"{float(row['water_masked_confidence_drop_pp']):.2f} pp | "
            f"{float(row['water_shifted_confidence_drop_pp']):.2f} pp | "
            f"{row['prediction_changed_after_counterfactual']} |"
        )

    bleached_majority = float(bleached.get("majority_attention_on_water", 0.0))
    overall_majority = float(vanilla["probability_majority_cam_attention_on_water"])
    lines.extend(
        [
            "",
            "## Thesis-Ready Conclusion",
            "",
        ]
    )
    if bleached_majority >= 0.50:
        lines.append(
            "The audit confirms a moderate shortcut risk concentrated in Bleached predictions: overall water-dominant CAM is not the majority pattern, but Bleached predictions frequently place CAM mass on sea-water coloured regions."
        )
    elif overall_majority >= 0.25:
        lines.append(
            "The audit shows moderate background-colour sensitivity overall, but the risk is not dominant enough to claim that the model mainly detects sea water instead of coral."
        )
    else:
        lines.append(
            "The audit does not show strong sea-water-colour reliance under these heuristics, though segmentation-mask validation would still be stronger evidence."
        )
    lines.append(
        "Recommended report wording: Grad-CAM supports that most predictions remain coral-relevant, while the Bleached class has measurable water-colour shortcut risk that should be addressed in a future isolated water-robust training experiment."
    )

    lines.extend(
        [
            "",
            "## Generated Files",
            "",
            "- `water_attention_metrics.csv`: baseline vanilla/default-mask per-image metrics.",
            "- `water_attention_metrics_by_mode.csv`: per-image metrics for vanilla, eigen, and aug+eigen CAM.",
            "- `cam_mode_comparison.csv`: summary table across CAM modes.",
            "- `mask_sensitivity_summary.csv`: sensitivity of results to water-mask thresholds.",
            "- `counterfactual_results.csv`: prediction/confidence changes after water-region perturbation.",
            "- `water_attention_summary.json`: machine-readable evidence pack.",
            "- `panels/`: report-ready example figures.",
        ]
    )

    markdown = "\n".join(lines) + "\n"
    (OUTPUT_DIR / "water_attention_summary.md").write_text(markdown, encoding="utf-8")
    (OUTPUT_DIR / "water_attention_evidence_pack.md").write_text(markdown, encoding="utf-8")


def write_outputs(
    seeds: List[int],
    images: np.ndarray,
    masked_images: np.ndarray,
    shifted_images: np.ndarray,
    heatmaps_by_mode: Dict[str, np.ndarray],
    mode_rows: Dict[str, List[Dict[str, object]]],
    mode_summaries: Dict[str, Dict[str, object]],
    mask_sensitivity: List[Dict[str, object]],
    counter_rows: List[Dict[str, object]],
    counter_summary: Dict[str, object],
) -> None:
    vanilla_rows = mode_rows["vanilla"]
    write_dicts_csv(
        OUTPUT_DIR / "water_attention_metrics.csv",
        [row_for_csv(row) for row in vanilla_rows],
    )
    write_dicts_csv(
        OUTPUT_DIR / "water_attention_metrics_by_mode.csv",
        [row_for_csv(row, include_mode=True) for rows in mode_rows.values() for row in rows],
    )

    mode_summary_rows = []
    for mode, summary in mode_summaries.items():
        bleached = summary["by_predicted_class"].get("Bleached", {})
        mode_summary_rows.append(
            {
                "cam_mode": mode,
                "accuracy_percent": summary["accuracy"] * 100.0,
                "majority_water_cam_percent": summary[
                    "probability_majority_cam_attention_on_water"
                ]
                * 100.0,
                "top20_majority_water_percent": summary[
                    "probability_top20_cam_pixels_majority_water"
                ]
                * 100.0,
                "area_adjusted_water_bias_percent": summary[
                    "probability_area_adjusted_water_bias"
                ]
                * 100.0,
                "median_water_cam_mass_percent": summary["water_attention_mass"]["median"] * 100.0,
                "median_enrichment": summary["water_attention_enrichment"]["median"],
                "bleached_majority_water_cam_percent": float(
                    bleached.get("majority_attention_on_water", 0.0)
                )
                * 100.0,
                "bleached_median_water_cam_mass_percent": float(
                    bleached.get("median_water_attention_mass", 0.0)
                )
                * 100.0,
            }
        )
    write_dicts_csv(OUTPUT_DIR / "cam_mode_comparison.csv", mode_summary_rows)
    write_dicts_csv(OUTPUT_DIR / "mask_sensitivity_summary.csv", mask_sensitivity)
    write_dicts_csv(OUTPUT_DIR / "counterfactual_results.csv", counter_rows)

    risky = sorted(vanilla_rows, key=lambda row: float(row["water_attention_mass"]), reverse=True)
    low = sorted(vanilla_rows, key=lambda row: float(row["water_attention_mass"]))
    enriched = sorted(vanilla_rows, key=lambda row: float(row["water_attention_enrichment"]), reverse=True)
    save_attention_panel(
        risky[:6],
        images,
        heatmaps_by_mode["vanilla"],
        "highest_water_attention.png",
        "Highest CAM Mass on Sea-Water Colour",
    )
    save_attention_panel(
        low[:6],
        images,
        heatmaps_by_mode["vanilla"],
        "lowest_water_attention.png",
        "Lowest CAM Mass on Sea-Water Colour",
    )
    save_attention_panel(
        enriched[:6],
        images,
        heatmaps_by_mode["vanilla"],
        "highest_area_adjusted_water_bias.png",
        "Highest Area-Adjusted Water Bias",
    )
    save_mode_comparison_panel(risky, images, heatmaps_by_mode)
    counter_risky = sorted(
        counter_rows,
        key=lambda row: float(row["largest_confidence_drop_pp"]),
        reverse=True,
    )
    save_counterfactual_panel(
        counter_risky,
        images,
        masked_images,
        shifted_images,
        heatmaps_by_mode["vanilla"],
    )
    write_summary_files(
        seeds=seeds,
        mode_summaries=mode_summaries,
        mask_sensitivity=mask_sensitivity,
        counter_rows=counter_rows,
        counter_summary=counter_summary,
        mode_rows=mode_rows,
    )


def run(args: argparse.Namespace) -> None:
    seeds = parse_seed_list(args.seeds)
    cam_modes = [mode for mode in CAM_MODES if mode != "aug_eigen" or not args.skip_aug_eigen]
    if "vanilla" not in cam_modes:
        cam_modes.insert(0, "vanilla")

    prepare_output_dir()
    images, y_true, rel_paths = load_test_split(args.max_images)
    masked_images, shifted_images = create_masked_datasets(images)

    print(f"Loaded {len(images)} test images")
    print(f"Using seeds: {seeds}")
    print(f"CAM modes: {', '.join(cam_modes)}")

    ensemble_probs = np.zeros((len(images), len(CLASS_NAMES)), dtype="float64")
    masked_probs = np.zeros_like(ensemble_probs)
    shifted_probs = np.zeros_like(ensemble_probs)
    heatmaps_by_mode: Dict[str, np.ndarray] = {
        mode: np.zeros((len(images), IMG_SIZE, IMG_SIZE), dtype="float32")
        for mode in cam_modes
    }

    loaded_predictions: Dict[int, np.ndarray] = {}
    for seed in seeds:
        print(f"Loading seed {seed} for prediction...")
        model = load_model_for_seed(seed)
        probs = model.predict(images, batch_size=args.batch_size, verbose=0)
        ensemble_probs += probs / len(seeds)
        masked_probs += model.predict(masked_images, batch_size=args.batch_size, verbose=0) / len(seeds)
        shifted_probs += model.predict(shifted_images, batch_size=args.batch_size, verbose=0) / len(seeds)
        loaded_predictions[seed] = np.argmax(probs, axis=1)
        tf.keras.backend.clear_session()
        del model
        gc.collect()

    target_classes = np.argmax(ensemble_probs, axis=1)

    for seed in seeds:
        print(f"Loading seed {seed} for Grad-CAM evidence...")
        model = load_model_for_seed(seed)
        for idx, image in enumerate(images):
            if idx and idx % 25 == 0:
                print(f"  Seed {seed}: Grad-CAM {idx}/{len(images)}")
            if args.explain_each_model_prediction:
                class_idx = int(loaded_predictions[seed][idx])
            else:
                class_idx = int(target_classes[idx])

            vanilla, eigen = compute_gradcam_vanilla_and_eigen(image, model, class_idx)
            if "vanilla" in heatmaps_by_mode:
                heatmaps_by_mode["vanilla"][idx] += vanilla / len(seeds)
            if "eigen" in heatmaps_by_mode:
                heatmaps_by_mode["eigen"][idx] += eigen / len(seeds)
            if "aug_eigen" in heatmaps_by_mode:
                aug = compute_aug_eigen_heatmap(image, model, class_idx)
                heatmaps_by_mode["aug_eigen"][idx] += aug / len(seeds)

        tf.keras.backend.clear_session()
        del model
        gc.collect()

    for mode, heatmaps in heatmaps_by_mode.items():
        heatmap_max = np.max(heatmaps, axis=(1, 2), keepdims=True)
        heatmaps_by_mode[mode] = np.divide(
            heatmaps,
            heatmap_max,
            out=np.zeros_like(heatmaps),
            where=heatmap_max > 0,
        )

    mode_rows = {
        mode: build_rows(images, y_true, rel_paths, ensemble_probs, heatmaps, mode)
        for mode, heatmaps in heatmaps_by_mode.items()
    }
    mode_summaries = {mode: summarize_rows(rows) for mode, rows in mode_rows.items()}
    mask_sensitivity = build_mask_sensitivity(images, heatmaps_by_mode, mode_rows)
    counter_rows = build_counterfactual_rows(
        y_true,
        rel_paths,
        ensemble_probs,
        masked_probs,
        shifted_probs,
        mode_rows["vanilla"],
    )
    counter_summary = counterfactual_summary(counter_rows)

    write_outputs(
        seeds=seeds,
        images=images,
        masked_images=masked_images,
        shifted_images=shifted_images,
        heatmaps_by_mode=heatmaps_by_mode,
        mode_rows=mode_rows,
        mode_summaries=mode_summaries,
        mask_sensitivity=mask_sensitivity,
        counter_rows=counter_rows,
        counter_summary=counter_summary,
    )

    print(f"Saved baseline CSV: {OUTPUT_DIR / 'water_attention_metrics.csv'}")
    print(f"Saved evidence report: {OUTPUT_DIR / 'water_attention_summary.md'}")
    print(f"Saved panels: {PANELS_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a water-colour shortcut-risk evidence pack for the current coral model."
    )
    parser.add_argument("--seeds", default=",".join(str(seed) for seed in DEFAULT_SEEDS))
    parser.add_argument("--max-images", type=int, default=0, help="Limit images for smoke testing. 0 means all.")
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument(
        "--skip-aug-eigen",
        action="store_true",
        help="Skip aug+eigen Grad-CAM to reduce runtime during smoke tests.",
    )
    parser.add_argument(
        "--explain-each-model-prediction",
        action="store_true",
        help="Explain each seed's own prediction before averaging heatmaps. Default explains final ensemble class.",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
