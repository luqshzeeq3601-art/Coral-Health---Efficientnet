from __future__ import annotations

import base64
import io
import os
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential


IMG_SIZE = 224
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
SEED_ORDER = [42, 43, 44, 45, 46]
MODE_MODEL_LIMITS = {
    "fast": 1,
    "balanced": 3,
    "accurate": 5,
}


def build_model() -> Sequential:
    """Architecture that matches the current V4 robust EfficientNetB0 model."""
    base_model = EfficientNetB0(include_top=False, weights=None, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = True
    for layer in base_model.layers[:-100]:
        layer.trainable = False

    return Sequential(
        [
            Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
            base_model,
            GlobalAveragePooling2D(),
            Dropout(0.6),
            Dense(3, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.0001)),
        ]
    )


def temperature_scale_from_probs(probs: np.ndarray, temperature: float) -> np.ndarray:
    probs = np.asarray(probs, dtype=np.float64)
    probs = np.clip(probs, 1e-8, 1.0)
    if temperature <= 0:
        return probs / np.sum(probs)
    scaled = np.power(probs, 1.0 / float(temperature))
    scaled_sum = np.sum(scaled)
    if scaled_sum <= 0:
        return probs / np.sum(probs)
    return scaled / scaled_sum


def image_to_data_uri(rgb_img: np.ndarray, fmt: str = "JPEG") -> str:
    img = np.asarray(rgb_img)
    if img.max() <= 1.0:
        img = (img * 255).astype(np.uint8)
    else:
        img = img.astype(np.uint8)
    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format=fmt)
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    mime = "image/jpeg" if fmt.upper() in {"JPG", "JPEG"} else "image/png"
    return f"data:{mime};base64,{encoded}"


class RealTimeModelRuntime:
    """Loads copied model artifacts and runs fast frame-level inference."""

    def __init__(self, models_dir: Path):
        self.models_dir = Path(models_dir)
        self.temperature = self._load_temperature()
        self._model_cache: Dict[str, List[tf.keras.Model]] = {}
        self._model_path_cache: Dict[str, List[Path]] = {}
        self.last_loaded_mode = "fast"

    def _load_temperature(self) -> float:
        temp_path = self.models_dir / "temperature.txt"
        if not temp_path.exists():
            return 1.0
        try:
            value = float(temp_path.read_text(encoding="utf-8").strip())
            return value if value > 0 else 1.0
        except (OSError, ValueError):
            return 1.0

    def available_model_paths(self) -> List[Path]:
        paths = []
        for seed in SEED_ORDER:
            path = self.models_dir / f"efficientnetb0_v4robust_seed{seed}_swa.h5"
            if path.exists():
                paths.append(path)
        return paths

    def load_models(self, mode: str = "fast") -> List[tf.keras.Model]:
        mode = self.normalize_mode(mode)
        if mode in self._model_cache:
            self.last_loaded_mode = mode
            return self._model_cache[mode]

        limit = MODE_MODEL_LIMITS[mode]
        selected_paths = self.available_model_paths()[:limit]
        if not selected_paths:
            raise FileNotFoundError(f"No copied model files found in {self.models_dir}")

        models: List[tf.keras.Model] = []
        for path in selected_paths:
            model = build_model()
            model.load_weights(str(path))
            models.append(model)

        self._model_cache[mode] = models
        self._model_path_cache[mode] = selected_paths
        self.last_loaded_mode = mode
        return models

    def normalize_mode(self, mode: Optional[str]) -> str:
        if not mode:
            return "fast"
        mode = mode.lower().strip()
        return mode if mode in MODE_MODEL_LIMITS else "fast"

    def status(self, mode: Optional[str] = None) -> Dict[str, object]:
        normalized_mode = self.normalize_mode(mode or self.last_loaded_mode)
        loaded = self._model_cache.get(normalized_mode, [])
        copied_paths = self.available_model_paths()
        return {
            "backend": "keras",
            "requested_mode": normalized_mode,
            "temperature": self.temperature,
            "copied_models_available": [path.name for path in copied_paths],
            "models_loaded_for_mode": len(loaded),
            "model_folder": str(self.models_dir),
            "uses_original_model_folder": False,
        }

    def preprocess_bgr(self, frame_bgr: np.ndarray) -> np.ndarray:
        if frame_bgr is None or frame_bgr.size == 0:
            raise ValueError("Empty frame")
        rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
        return resized.astype("float32")

    def predict_frame(self, frame_bgr: np.ndarray, mode: str = "fast") -> Dict[str, object]:
        started = time.perf_counter()
        mode = self.normalize_mode(mode)
        models = self.load_models(mode)
        img = self.preprocess_bgr(frame_bgr)
        batch = np.expand_dims(img, axis=0)

        predictions = []
        for model in models:
            preds = model(batch, training=False).numpy()[0]
            predictions.append(preds)

        avg_preds = np.mean(predictions, axis=0)
        avg_preds = temperature_scale_from_probs(avg_preds, self.temperature)
        final_idx = int(np.argmax(avg_preds))
        latency_ms = (time.perf_counter() - started) * 1000.0

        return {
            "label": CLASS_NAMES[final_idx],
            "confidence": float(avg_preds[final_idx] * 100.0),
            "probabilities": {name: float(avg_preds[i] * 100.0) for i, name in enumerate(CLASS_NAMES)},
            "latency_ms": float(latency_ms),
            "mode": mode,
            "models_used": len(models),
            "copied_model_files": [path.name for path in self._model_path_cache.get(mode, [])],
            "frame_size": IMG_SIZE,
        }

    def explain_frame(self, frame_bgr: np.ndarray, class_name: Optional[str] = None, mode: str = "fast") -> Dict[str, object]:
        models = self.load_models(mode)
        model = models[0]
        img = self.preprocess_bgr(frame_bgr)
        pred = self.predict_frame(frame_bgr, mode=mode)
        if class_name in CLASS_NAMES:
            class_idx = CLASS_NAMES.index(str(class_name))
        else:
            class_idx = CLASS_NAMES.index(str(pred["label"]))

        heatmap = self._compute_gradcam(model, img, class_idx)
        overlay = self._overlay_heatmap(img, heatmap)
        return {
            "label": CLASS_NAMES[class_idx],
            "heatmap": image_to_data_uri(self._heatmap_rgb(heatmap), fmt="PNG"),
            "overlay": image_to_data_uri(overlay, fmt="PNG"),
            "source_prediction": pred,
        }

    def _compute_gradcam(self, model: tf.keras.Model, img_array: np.ndarray, class_idx: int) -> np.ndarray:
        efficientnet = next((layer for layer in model.layers if "efficientnet" in layer.name.lower()), None)
        if efficientnet is None:
            raise RuntimeError("EfficientNet layer was not found in copied model")

        try:
            target_layer = efficientnet.get_layer("top_conv")
        except ValueError:
            target_layer = next((layer for layer in reversed(efficientnet.layers) if isinstance(layer, tf.keras.layers.Conv2D)), None)
        if target_layer is None:
            raise RuntimeError("No convolution layer found for Grad-CAM")

        grad_model_part1 = tf.keras.models.Model(inputs=efficientnet.input, outputs=target_layer.output)
        try:
            top_bn = efficientnet.get_layer("top_bn")
            top_activation = efficientnet.get_layer("top_activation")
        except ValueError:
            top_bn = None
            top_activation = None

        conv_outputs_value = grad_model_part1(tf.cast(np.expand_dims(img_array, axis=0), tf.float32))
        conv_outputs = tf.Variable(conv_outputs_value, trainable=True, dtype=tf.float32)
        eff_index = list(model.layers).index(efficientnet)

        with tf.GradientTape() as tape:
            x = conv_outputs
            if top_bn is not None and top_activation is not None:
                x = top_bn(x, training=False)
                x = top_activation(x)
            for layer in model.layers[eff_index + 1 :]:
                try:
                    x = layer(x, training=False)
                except TypeError:
                    x = layer(x)
            loss = x[:, class_idx]

        grads = tape.gradient(loss, conv_outputs)
        if grads is None:
            raise RuntimeError("Grad-CAM gradients were empty")

        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_out = conv_outputs[0]
        heatmap = conv_out @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.nn.relu(heatmap).numpy()
        heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
        max_value = float(np.max(heatmap))
        if max_value > 0:
            heatmap = heatmap / max_value
        return heatmap

    def _heatmap_rgb(self, heatmap: np.ndarray) -> np.ndarray:
        colored = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
        return cv2.cvtColor(colored, cv2.COLOR_BGR2RGB)

    def _overlay_heatmap(self, rgb_img: np.ndarray, heatmap: np.ndarray, alpha: float = 0.38) -> np.ndarray:
        colored = self._heatmap_rgb(heatmap)
        img_uint8 = rgb_img.astype(np.uint8)
        return cv2.addWeighted(img_uint8, 1 - alpha, colored, alpha, 0)


def decode_frame_from_request(files, json_payload: Optional[Dict[str, object]]) -> np.ndarray:
    upload = files.get("frame") or files.get("image") or files.get("file")
    if upload is not None:
        file_bytes = np.frombuffer(upload.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Could not decode uploaded image frame")
        return frame

    if not json_payload or "image" not in json_payload:
        raise ValueError("No frame provided")

    image_data = str(json_payload["image"])
    if "," in image_data:
        image_data = image_data.split(",", 1)[1]
    raw = base64.b64decode(image_data)
    file_bytes = np.frombuffer(raw, np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Could not decode JSON image frame")
    return frame

