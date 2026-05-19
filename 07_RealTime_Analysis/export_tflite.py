from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
import tensorflow as tf

from src.model_runtime import IMG_SIZE, SEED_ORDER, build_model


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
PROJECT_ROOT = BASE_DIR.parent
DATASET_DIR = PROJECT_ROOT / "Dataset"


def representative_images(max_samples: int) -> Iterable[np.ndarray]:
    image_paths = []
    for class_name in ["Healthy", "Bleached", "Dead"]:
        class_dir = DATASET_DIR / class_name
        if class_dir.exists():
            image_paths.extend(sorted(class_dir.glob("*.png"))[: max_samples // 3 + 1])

    for path in image_paths[:max_samples]:
        img = cv2.imread(str(path))
        if img is None:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
        yield np.expand_dims(img.astype("float32"), axis=0)


def build_representative_dataset(max_samples: int):
    def dataset():
        for sample in representative_images(max_samples):
            yield [sample]

    return dataset


def resolve_model_path(seed: int) -> Path:
    path = MODELS_DIR / f"efficientnetb0_v4robust_seed{seed}_swa.h5"
    if not path.exists():
        raise FileNotFoundError(f"Copied model file not found: {path}")
    return path


def export_tflite(seed: int, int8: bool, samples: int) -> Path:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = resolve_model_path(seed)
    model = build_model()
    model.load_weights(str(model_path))

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    suffix = "float32"
    if int8:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = build_representative_dataset(samples)
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        suffix = "int8"

    tflite_model = converter.convert()
    output_path = ARTIFACTS_DIR / f"efficientnetb0_v4robust_seed{seed}_swa_{suffix}.tflite"
    output_path.write_bytes(tflite_model)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the copied real-time model to TFLite.")
    parser.add_argument("--model", default="seed42", help="Model seed to export, e.g. seed42.")
    parser.add_argument("--int8", action="store_true", help="Use full-int8 quantization for Coral TPU preparation.")
    parser.add_argument("--samples", type=int, default=90, help="Representative dataset sample count for int8 export.")
    args = parser.parse_args()

    seed_text = str(args.model).lower().replace("seed", "")
    seed = int(seed_text)
    if seed not in SEED_ORDER:
        raise ValueError(f"Unsupported seed {seed}; expected one of {SEED_ORDER}")

    output_path = export_tflite(seed=seed, int8=args.int8, samples=max(1, args.samples))
    print(f"Saved TFLite model to {output_path}")
    if args.int8:
        print("For Coral TPU, compile this file with: edgetpu_compiler <model>.tflite")


if __name__ == "__main__":
    main()
