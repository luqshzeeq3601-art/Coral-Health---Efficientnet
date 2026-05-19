import io
import json
import os
import sys
from typing import List, Tuple

import cv2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential

matplotlib.use("Agg")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


IMG_SIZE = 224
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
SEEDS = [42, 43, 44, 45, 46]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))
DATASET_DIR = os.path.join(PROJECT_ROOT, "Dataset")
MODEL_DIR = os.path.join(BASE_DIR, "models")
PRIMARY_OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MIRROR_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "03_Model_Evaluation", "01_EfficientNetB0_Evaluation")
OUTPUT_DIRS = [PRIMARY_OUTPUT_DIR, MIRROR_OUTPUT_DIR]


def build_model() -> tf.keras.Model:
    base_model = EfficientNetB0(include_top=False, weights="imagenet", input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = True
    for layer in base_model.layers[:-100]:
        layer.trainable = False

    return Sequential(
        [
            Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
            base_model,
            GlobalAveragePooling2D(),
            Dropout(0.4),
            Dense(3, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.0002)),
        ]
    )


def collect_dataset_entries() -> Tuple[List[str], np.ndarray]:
    file_paths: List[str] = []
    labels: List[int] = []

    for cls_idx, cls_name in enumerate(CLASS_NAMES):
        class_dir = os.path.join(DATASET_DIR, cls_name)
        if not os.path.exists(class_dir):
            class_dir = os.path.join(DATASET_DIR, cls_name.lower())

        if not os.path.exists(class_dir):
            raise FileNotFoundError(f"Dataset class folder not found: {class_dir}")

        for fname in sorted(os.listdir(class_dir)):
            if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            file_paths.append(os.path.join(class_dir, fname))
            labels.append(cls_idx)

    return file_paths, np.array(labels, dtype=np.int32)


def load_test_split() -> Tuple[np.ndarray, np.ndarray]:
    """
    Reconstruct the canonical deterministic split directly from the dataset.

    This avoids relying on stale cached split files that can drift from the
    benchmark artefacts.
    """
    file_paths, labels = collect_dataset_entries()
    indices = np.arange(len(file_paths))

    _, temp_idx = train_test_split(
        indices,
        test_size=0.2,
        random_state=42,
        stratify=labels,
    )
    temp_labels = labels[temp_idx]
    _, test_idx = train_test_split(
        temp_idx,
        test_size=0.5,
        random_state=42,
        stratify=temp_labels,
    )

    images: List[np.ndarray] = []
    y_true: List[int] = []
    for idx in test_idx:
        img_bgr = cv2.imread(file_paths[idx])
        if img_bgr is None:
            raise RuntimeError(f"Could not read image: {file_paths[idx]}")
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_rgb = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
        images.append(img_rgb.astype("float32"))
        y_true.append(int(labels[idx]))

    return np.array(images, dtype="float32"), np.array(y_true, dtype=np.int32)


def load_models() -> List[tf.keras.Model]:
    models: List[tf.keras.Model] = []
    for seed in SEEDS:
        checkpoint_path = os.path.join(MODEL_DIR, f"efficientnetb0_v4robust_seed{seed}_swa.h5")
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Missing deployment checkpoint: {checkpoint_path}")

        model = build_model()
        model.load_weights(checkpoint_path)
        models.append(model)
        print(f"  Loaded deployment checkpoint for seed {seed}")
    return models


def predict_single_scale_ensemble(models: List[tf.keras.Model], x_test: np.ndarray) -> np.ndarray:
    """
    Canonical academic benchmark:
    224x224 single-scale ensemble averaging, no TTA, no deployment calibration.
    """
    all_probs = [model.predict(x_test, verbose=0) for model in models]
    return np.mean(all_probs, axis=0)


def save_report_text(report_text: str, accuracy: float, cm: np.ndarray) -> None:
    payload = (
        "V4 Robust (EfficientNetB0) - 5-Seed SWA Ensemble (224px Canonical Benchmark)\n"
        f"Ensemble Accuracy: {accuracy * 100:.2f}%\n\n"
        f"{report_text}"
    )

    raw_payload = {
        "protocol": "224px canonical benchmark, 5-seed SWA ensemble, single-scale, no TTA",
        "accuracy": accuracy,
        "class_order": CLASS_NAMES,
        "confusion_matrix": cm.tolist(),
    }

    for output_dir in OUTPUT_DIRS:
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "classification_report_ensemble.txt"), "w", encoding="utf-8") as f:
            f.write(payload)
        with open(os.path.join(output_dir, "confusion_matrix_ensemble.json"), "w", encoding="utf-8") as f:
            json.dump(raw_payload, f, indent=2)


def save_report_table(report_dict: dict) -> None:
    fig, ax = plt.subplots(figsize=(10, 5), facecolor="white")
    ax.axis("off")
    ax.set_title("Classification Report - EfficientNetB0", fontsize=14, fontweight="bold", pad=20)

    headers = ["Class", "Precision", "Recall", "F1-Score", "Support"]
    table_data = []
    for cls_name in CLASS_NAMES:
        row = report_dict[cls_name]
        table_data.append(
            [
                cls_name,
                f"{row['precision']:.4f}",
                f"{row['recall']:.4f}",
                f"{row['f1-score']:.4f}",
                f"{int(row['support'])}",
            ]
        )
    table_data.append(["", "", "", "", ""])
    table_data.append(
        [
            "Accuracy",
            "",
            "",
            f"{report_dict['accuracy']:.4f}",
            f"{int(report_dict['weighted avg']['support'])}",
        ]
    )
    table_data.append(
        [
            "Macro Avg",
            f"{report_dict['macro avg']['precision']:.4f}",
            f"{report_dict['macro avg']['recall']:.4f}",
            f"{report_dict['macro avg']['f1-score']:.4f}",
            f"{int(report_dict['macro avg']['support'])}",
        ]
    )
    table_data.append(
        [
            "Weighted Avg",
            f"{report_dict['weighted avg']['precision']:.4f}",
            f"{report_dict['weighted avg']['recall']:.4f}",
            f"{report_dict['weighted avg']['f1-score']:.4f}",
            f"{int(report_dict['weighted avg']['support'])}",
        ]
    )

    table = ax.table(cellText=table_data, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)

    for col in range(len(headers)):
        table[0, col].set_facecolor("#4472C4")
        table[0, col].set_text_props(color="white", fontweight="bold")
    for row in range(1, len(table_data) + 1):
        for col in range(len(headers)):
            table[row, col].set_facecolor("#D6E4F0" if row <= len(CLASS_NAMES) else "#F2F2F2")

    for output_dir in OUTPUT_DIRS:
        fig.savefig(
            os.path.join(output_dir, "classification_report_ensemble.png"),
            dpi=150,
            bbox_inches="tight",
        )
    plt.close(fig)


def save_confusion_matrix(cm: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        annot_kws={"size": 14},
        ax=ax,
    )
    ax.set_title("Confusion Matrix - EfficientNetB0", fontsize=14, fontweight="bold")
    ax.set_xlabel("Predicted", fontsize=12)
    ax.set_ylabel("Actual", fontsize=12)
    plt.tight_layout()

    for output_dir in OUTPUT_DIRS:
        fig.savefig(
            os.path.join(output_dir, "confusion_matrix_ensemble.png"),
            dpi=150,
            bbox_inches="tight",
        )
    plt.close(fig)


def main() -> None:
    print("Regenerating canonical current-model evaluation artefacts...")
    print("Protocol: 224x224 single-scale 5-seed SWA ensemble (no TTA)")

    x_test, y_true = load_test_split()
    print(f"  Test images loaded: {len(x_test)}")

    models = load_models()
    avg_probs = predict_single_scale_ensemble(models, x_test)
    y_pred = np.argmax(avg_probs, axis=1)

    accuracy = float(np.mean(y_pred == y_true))
    cm = confusion_matrix(y_true, y_pred, labels=list(range(len(CLASS_NAMES))))
    report_text = classification_report(y_true, y_pred, target_names=CLASS_NAMES)
    report_dict = classification_report(y_true, y_pred, target_names=CLASS_NAMES, output_dict=True)

    print(f"  Canonical accuracy: {accuracy * 100:.2f}%")
    print(f"  Confusion matrix: {cm.tolist()}")

    save_report_text(report_text, accuracy, cm)
    save_report_table(report_dict)
    save_confusion_matrix(cm)

    print("  Saved synced report + confusion matrix to:")
    for output_dir in OUTPUT_DIRS:
        print(f"    - {output_dir}")


if __name__ == "__main__":
    main()
