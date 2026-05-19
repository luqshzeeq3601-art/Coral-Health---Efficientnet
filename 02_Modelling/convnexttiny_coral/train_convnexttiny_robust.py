import csv
import io
import json
import os
import subprocess
import sys
import time

import cv2
import matplotlib
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight, shuffle
from tensorflow.keras.applications import ConvNeXtTiny
from tensorflow.keras.callbacks import LearningRateScheduler, ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ==========================================
# ConvNeXtTiny Robust Single-Seed Config
# ==========================================
IMG_SIZE = 224
CLASS_NAMES = ["Healthy", "Bleached", "Dead"]
SEED = 42
SPLIT_SEED = 42
EPOCHS = 30
BATCH_SIZE = 6
LABEL_SMOOTHING = 0.05
INITIAL_LR = 5e-5
OVERSAMPLE_FACTOR = 20
GPU_MAX_TEMP_C = 78
GPU_RESUME_TEMP_C = 68
GPU_COOLDOWN_SECONDS = 45
GPU_BATCH_CHECK_INTERVAL = 10

HARD_EXAMPLES = {
    "Bleached": [
        "157.png", "158.png", "193.png", "194.png", "199.png", "200.png",
        "205.png", "206.png", "240.png", "252.png", "37.png", "38.png",
        "438.png", "445.png", "471.png", "477.png", "480.png", "55.png",
        "56.png", "568.png", "569.png", "590.png", "659.png", "665.png",
        "671.png", "685.png", "686.png", "689.png", "695.png",
    ],
    "Dead": [
        "83.png", "84.png", "85.png", "86.png", "112.png", "116.png",
        "119.png", "123.png", "130.png", "131.png", "139.png", "142.png",
        "145.png", "137.png", "67.png",
    ],
    "Healthy": ["292.png", "34.png"],
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
MODEL_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
SPLIT_INFO_PATH = os.path.join(PROJECT_ROOT, "05_Baseline_Model", "split_info_v3.json")
DATASET_PATH = os.path.join(PROJECT_ROOT, "Dataset")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def configure_gpu_memory_growth():
    gpus = tf.config.list_physical_devices("GPU")
    if not gpus:
        print("No TensorFlow GPU detected. Training will run on CPU.")
        return
    for gpu in gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as exc:
            print(f"Could not set memory growth for {gpu.name}: {exc}")
    print(f"TensorFlow GPU devices: {[gpu.name for gpu in gpus]}")


def query_gpu_status():
    query = "name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw,power.limit"
    cmd = [
        "nvidia-smi",
        f"--query-gpu={query}",
        "--format=csv,noheader,nounits",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
    except (FileNotFoundError, subprocess.SubprocessError):
        return None

    lines = result.stdout.strip().splitlines()
    if not lines:
        return None

    parts = [part.strip() for part in lines[0].split(",")]
    if len(parts) < 7:
        return None

    def parse_float(value):
        try:
            return float(value)
        except ValueError:
            return None

    return {
        "name": parts[0],
        "temperature_c": parse_float(parts[1]),
        "utilization_gpu_percent": parse_float(parts[2]),
        "memory_used_mib": parse_float(parts[3]),
        "memory_total_mib": parse_float(parts[4]),
        "power_draw_w": parse_float(parts[5]),
        "power_limit_w": parse_float(parts[6]),
    }


def fmt_status_value(value, suffix=""):
    if value is None:
        return "N/A"
    return f"{value:.0f}{suffix}"


class GPUTemperatureCallback(tf.keras.callbacks.Callback):
    def __init__(
        self,
        log_path,
        max_temp_c=GPU_MAX_TEMP_C,
        resume_temp_c=GPU_RESUME_TEMP_C,
        cooldown_seconds=GPU_COOLDOWN_SECONDS,
        batch_check_interval=GPU_BATCH_CHECK_INTERVAL,
    ):
        super().__init__()
        self.log_path = log_path
        self.max_temp_c = max_temp_c
        self.resume_temp_c = resume_temp_c
        self.cooldown_seconds = cooldown_seconds
        self.batch_check_interval = batch_check_interval
        self.enabled = query_gpu_status() is not None
        self._init_log()

    def _init_log(self):
        with open(self.log_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "event",
                "epoch",
                "batch",
                "gpu_name",
                "temperature_c",
                "utilization_gpu_percent",
                "memory_used_mib",
                "memory_total_mib",
                "power_draw_w",
                "power_limit_w",
                "note",
            ])
            if not self.enabled:
                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    "temperature_control_disabled",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "nvidia-smi was not available",
                ])

    def _write_status(self, event, epoch, batch=None, note=""):
        status = query_gpu_status()
        if status is None:
            return None
        with open(self.log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"),
                event,
                "" if epoch is None else epoch + 1,
                "" if batch is None else batch + 1,
                status["name"],
                status["temperature_c"],
                status["utilization_gpu_percent"],
                status["memory_used_mib"],
                status["memory_total_mib"],
                status["power_draw_w"],
                status["power_limit_w"],
                note,
            ])
        return status

    def _cooldown_if_needed(self, epoch, phase, batch=None):
        if not self.enabled:
            return
        status = self._write_status(f"{phase}_check", epoch, batch=batch)
        if status is None:
            return

        while status["temperature_c"] is not None and status["temperature_c"] >= self.max_temp_c:
            note = (
                f"temperature {status['temperature_c']:.0f}C >= {self.max_temp_c}C; "
                f"waiting until <= {self.resume_temp_c}C"
            )
            print(f"GPU cooldown: {note}")
            self._write_status("cooldown_wait", epoch, batch=batch, note=note)
            time.sleep(self.cooldown_seconds)
            status = self._write_status("cooldown_recheck", epoch, batch=batch)
            if status is None:
                return

        if status["temperature_c"] is not None and status["temperature_c"] <= self.resume_temp_c:
            self._write_status(
                "cooldown_clear",
                epoch,
                batch=batch,
                note=f"temperature <= {self.resume_temp_c}C",
            )

    def on_train_begin(self, logs=None):
        self._cooldown_if_needed(None, "train_begin")

    def on_epoch_begin(self, epoch, logs=None):
        self._cooldown_if_needed(epoch, "epoch_begin")

    def on_train_batch_begin(self, batch, logs=None):
        if batch % self.batch_check_interval == 0:
            self._cooldown_if_needed(self.params.get("epochs_seen"), "batch_begin", batch=batch)

    def on_epoch_end(self, epoch, logs=None):
        self._cooldown_if_needed(epoch, "epoch_end")


def collect_file_paths(dataset_path):
    file_paths, labels, filenames = [], [], []
    for cls_idx, cls_name in enumerate(CLASS_NAMES):
        cls_dir = os.path.join(dataset_path, cls_name)
        if not os.path.exists(cls_dir):
            cls_dir = os.path.join(dataset_path, cls_name.lower())
        if os.path.exists(cls_dir):
            for fname in sorted(os.listdir(cls_dir)):
                if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    continue
                file_paths.append(os.path.join(cls_dir, fname))
                labels.append(cls_idx)
                filenames.append(f"{cls_name}/{fname}")
    return file_paths, np.array(labels), filenames


def load_images(file_paths):
    images = []
    for path in file_paths:
        try:
            img = cv2.imread(path)
            if img is not None:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
            images.append(img)
        except Exception:
            images.append(None)
    return images


def split_dataset(dataset_path):
    if os.path.exists(SPLIT_INFO_PATH):
        print(f"Loading canonical split from {SPLIT_INFO_PATH}")
        with open(SPLIT_INFO_PATH, "r", encoding="utf-8") as f:
            split_info = json.load(f)

        def get_paths(filenames):
            paths, labels = [], []
            for fname in filenames:
                full = os.path.join(dataset_path, fname)
                if os.path.exists(full):
                    paths.append(full)
                    cls_name = fname.split("/")[0]
                    labels.append(CLASS_NAMES.index(cls_name))
            return paths, np.array(labels)

        train_paths, train_labels = get_paths(split_info["train_files"])
        val_paths, val_labels = get_paths(split_info["val_files"])
        test_paths, test_labels = get_paths(split_info["test_files"])
        return train_paths, train_labels, val_paths, val_labels, test_paths, test_labels

    print("Canonical split was not found. Creating a deterministic stratified split.")
    file_paths, labels, _ = collect_file_paths(dataset_path)
    indices = np.arange(len(file_paths))
    train_idx, temp_idx = train_test_split(
        indices, test_size=0.2, random_state=SPLIT_SEED, stratify=labels
    )
    temp_labels = labels[temp_idx]
    val_idx, test_idx = train_test_split(
        temp_idx, test_size=0.5, random_state=SPLIT_SEED, stratify=temp_labels
    )
    return (
        [file_paths[i] for i in train_idx],
        labels[train_idx],
        [file_paths[i] for i in val_idx],
        labels[val_idx],
        [file_paths[i] for i in test_idx],
        labels[test_idx],
    )


def prepare_set(paths, labels):
    images = load_images(paths)
    valid_imgs, valid_lbls = [], []
    for img, label in zip(images, labels):
        if img is not None:
            valid_imgs.append(img)
            valid_lbls.append(label)
    X = np.array(valid_imgs, dtype="float32")
    y = tf.keras.utils.to_categorical(np.array(valid_lbls), num_classes=3)
    return X, y


def get_augmenter():
    return tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.15,
        height_shift_range=0.15,
        horizontal_flip=True,
        vertical_flip=False,
        zoom_range=0.15,
        shear_range=0.05,
        fill_mode="nearest",
        brightness_range=[0.8, 1.2],
    )


def should_train_backbone_layer(layer):
    return "convnext_tiny_stage_3" in layer.name or layer.name == "layer_normalization"


def build_model(weights="imagenet"):
    base_model = ConvNeXtTiny(
        include_top=False,
        include_preprocessing=True,
        weights=weights,
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
    )
    base_model.trainable = True
    for layer in base_model.layers:
        layer.trainable = should_train_backbone_layer(layer)

    return Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        GlobalAveragePooling2D(),
        Dropout(0.5),
        Dense(3, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.0002)),
    ])


def cosine_decay(epoch):
    cosine_decay_val = 0.5 * (1 + np.cos(np.pi * epoch / EPOCHS))
    return INITIAL_LR * cosine_decay_val


class SWACallback(tf.keras.callbacks.Callback):
    def __init__(self, start_epoch, swa_path):
        super().__init__()
        self.start_epoch = start_epoch
        self.swa_path = swa_path
        self.swa_weights = None
        self.n_models = 0

    def on_epoch_end(self, epoch, logs=None):
        if epoch >= self.start_epoch:
            current_weights = self.model.get_weights()
            if self.swa_weights is None:
                self.swa_weights = [np.copy(w) for w in current_weights]
            else:
                for i in range(len(self.swa_weights)):
                    self.swa_weights[i] = (
                        self.swa_weights[i] * self.n_models + current_weights[i]
                    ) / (self.n_models + 1)
            self.n_models += 1
            print(f"  [SWA] Averaged weights from epoch {epoch + 1} ({self.n_models} models)")

    def on_train_end(self, logs=None):
        if self.swa_weights is not None:
            self.model.set_weights(self.swa_weights)
            self.model.save_weights(self.swa_path)
            print(f"  [SWA] Final averaged weights saved to {self.swa_path}")


class EpochTrackingCallback(tf.keras.callbacks.Callback):
    def on_epoch_begin(self, epoch, logs=None):
        self.params["epochs_seen"] = epoch


class AugmentedMixupGenerator(tf.keras.utils.Sequence):
    def __init__(self, X, y, batch_size, augment_gen, alpha=0.1, class_weights_dict=None):
        self.gen = augment_gen.flow(X, y, batch_size=batch_size)
        self.alpha = alpha
        self.batch_size = batch_size
        self.class_weights_dict = class_weights_dict

    def __len__(self):
        return len(self.gen)

    def _apply_color_jitter(self, X_batch):
        X_scaled = np.clip(X_batch / 255.0, 0.0, 1.0).astype("float32")
        X_scaled = tf.image.random_hue(X_scaled, 0.05).numpy()
        X_scaled = tf.image.random_saturation(X_scaled, 0.8, 1.2).numpy()
        return np.clip(X_scaled * 255.0, 0.0, 255.0).astype("float32")

    def __getitem__(self, index):
        X_batch, y_batch = self.gen[index]
        X_batch = self._apply_color_jitter(X_batch)

        batch_size = len(X_batch)
        if batch_size < 2:
            return X_batch.astype("float32"), y_batch

        lam = np.random.beta(self.alpha, self.alpha, batch_size)
        perm_index = np.random.permutation(batch_size)
        lam_img = lam.reshape(batch_size, 1, 1, 1)
        lam_lbl = lam.reshape(batch_size, 1)

        X_mixed = lam_img * X_batch + (1 - lam_img) * X_batch[perm_index]
        y_mixed = lam_lbl * y_batch + (1 - lam_lbl) * y_batch[perm_index]
        X_mixed = np.clip(X_mixed, 0.0, 255.0).astype("float32")

        if self.class_weights_dict:
            y_i1 = np.argmax(y_batch, axis=1)
            y_i2 = np.argmax(y_batch[perm_index], axis=1)
            w1 = np.array([self.class_weights_dict[i] for i in y_i1])
            w2 = np.array([self.class_weights_dict[i] for i in y_i2])
            sample_weights = lam * w1 + (1 - lam) * w2
            return X_mixed, y_mixed, sample_weights

        return X_mixed, y_mixed


def prepare_training_data(paths, labels, seed):
    train_filenames = [
        f"{p.replace(chr(92), '/').split('/')[-2]}/{p.replace(chr(92), '/').split('/')[-1]}"
        for p in paths
    ]
    hard_filenames = {
        f"{cls_name}/{fname}"
        for cls_name, files in HARD_EXAMPLES.items()
        for fname in files
    }

    images = load_images(paths)
    base_imgs, base_lbls = [], []
    hard_imgs, hard_lbls = [], []

    for img, label, fname in zip(images, labels, train_filenames):
        if img is None:
            continue
        base_imgs.append(img)
        base_lbls.append(label)
        if fname in hard_filenames:
            cls_name = fname.split("/")[0]
            factor = 30 if cls_name == "Dead" else OVERSAMPLE_FACTOR
            for _ in range(factor):
                hard_imgs.append(img)
                hard_lbls.append(label)

    print(f"  Base training images: {len(base_imgs)}")
    print(f"  Hard images (oversampled): {len(hard_imgs)}")

    X = np.array(base_imgs + hard_imgs, dtype="float32")
    y = np.array(base_lbls + hard_lbls)
    y = tf.keras.utils.to_categorical(y, num_classes=3)
    X, y = shuffle(X, y, random_state=seed)
    print(f"  Total training samples: {len(X)}")
    return X, y


def save_training_history(history):
    history_data = {
        "train_accuracy": history.history["accuracy"],
        "val_accuracy": history.history["val_accuracy"],
        "train_loss": history.history["loss"],
        "val_loss": history.history["val_loss"],
    }
    with open(os.path.join(OUTPUT_DIR, "training_history_convnexttiny.json"), "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4)

    epochs_range = range(1, len(history_data["train_accuracy"]) + 1)
    plt.figure(figsize=(14, 5), facecolor="white")

    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(epochs_range, history_data["train_accuracy"], label="Training Accuracy", linewidth=2.5)
    ax1.plot(epochs_range, history_data["val_accuracy"], label="Validation Accuracy", linewidth=2.5)
    ax1.set_title("ConvNeXtTiny Training and Validation Accuracy", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Accuracy")
    ax1.set_ylim([0.60, 1.00])
    ax1.grid(True, linestyle="--", alpha=0.5)
    ax1.legend(loc="lower right")

    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(epochs_range, history_data["train_loss"], label="Training Loss", linewidth=2.5)
    ax2.plot(epochs_range, history_data["val_loss"], label="Validation Loss", linewidth=2.5)
    ax2.set_title("ConvNeXtTiny Training and Validation Loss", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Loss")
    ax2.grid(True, linestyle="--", alpha=0.5)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "training_history_convnexttiny.png"), dpi=150, bbox_inches="tight")
    plt.close()


def evaluate_swa_model(model, X_test, y_test):
    preds = model.predict(X_test, batch_size=BATCH_SIZE, verbose=1)
    y_pred_classes = np.argmax(preds, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    accuracy = float(np.mean(y_pred_classes == y_true_classes))

    report_text = classification_report(y_true_classes, y_pred_classes, target_names=CLASS_NAMES)
    report_dict = classification_report(
        y_true_classes, y_pred_classes, target_names=CLASS_NAMES, output_dict=True
    )

    with open(os.path.join(OUTPUT_DIR, "classification_report_convnexttiny.txt"), "w", encoding="utf-8") as f:
        f.write("ConvNeXtTiny Robust Single Model - Seed 42 SWA\n")
        f.write("Protocol: 224px single-scale, no TTA\n")
        f.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")
        f.write(report_text)

    cm = confusion_matrix(y_true_classes, y_pred_classes)
    cm_payload = {
        "model": "ConvNeXtTiny Robust Single Model",
        "seed": SEED,
        "protocol": "224px single-scale, no TTA",
        "accuracy": accuracy,
        "accuracy_percent": round(accuracy * 100, 2),
        "test_samples": int(len(y_true_classes)),
        "total_errors": int(np.sum(y_true_classes != y_pred_classes)),
        "class_order": CLASS_NAMES,
        "confusion_matrix": cm.tolist(),
        "classification_report": report_dict,
    }
    with open(os.path.join(OUTPUT_DIR, "confusion_matrix_convnexttiny.json"), "w", encoding="utf-8") as f:
        json.dump(cm_payload, f, indent=4)

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        annot_kws={"size": 14},
    )
    plt.title("Confusion Matrix - ConvNeXtTiny", fontsize=14, fontweight="bold")
    plt.xlabel("Predicted", fontsize=12)
    plt.ylabel("Actual", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix_convnexttiny.png"), dpi=150)
    plt.close()
    return accuracy, cm_payload


def train_model():
    configure_gpu_memory_growth()
    tf.keras.utils.set_random_seed(SEED)

    print("=" * 60)
    print("CONVNEXTTINY ROBUST TRAINING - Single Seed 42")
    print("=" * 60)

    gpu_status = query_gpu_status()
    if gpu_status:
        print(
            "GPU detected: "
            f"{gpu_status['name']} | {fmt_status_value(gpu_status['temperature_c'], 'C')} | "
            f"{fmt_status_value(gpu_status['memory_used_mib'])}/"
            f"{fmt_status_value(gpu_status['memory_total_mib'])} MiB"
        )
    else:
        print("nvidia-smi was not available. GPU temperature control will be disabled.")

    print("\nLoading dataset and canonical split...")
    train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = split_dataset(DATASET_PATH)
    print(f"  Train paths: {len(train_paths)}")
    print(f"  Val paths:   {len(val_paths)}")
    print(f"  Test paths:  {len(test_paths)}")

    X_train, y_train = prepare_training_data(train_paths, train_labels, SEED)
    X_val, y_val = prepare_set(val_paths, val_labels)
    X_test, y_test = prepare_set(test_paths, test_labels)

    y_integers = np.argmax(y_train, axis=1)
    class_weights = class_weight.compute_class_weight(
        class_weight="balanced", classes=np.unique(y_integers), y=y_integers
    )
    class_weights_dict = dict(enumerate(class_weights))
    class_weights_dict[2] = class_weights_dict[2] * 1.3

    model = build_model()
    total_params = int(model.count_params())
    trainable_params = int(sum(tf.keras.backend.count_params(w) for w in model.trainable_weights))
    print("\nTraining Config:")
    print("  Model: ConvNeXtTiny Robust Single Model")
    print(f"  Total Params: {total_params:,}")
    print(f"  Trainable Params: {trainable_params:,}")
    print(f"  Seed: {SEED}")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Batch Size: {BATCH_SIZE}")
    print(f"  Label Smoothing: {LABEL_SMOOTHING}")
    print(f"  Initial LR: {INITIAL_LR}")
    print(f"  SWA: Last 5 epochs")
    print(
        "  GPU Temp Control: "
        f"max {GPU_MAX_TEMP_C}C, resume {GPU_RESUME_TEMP_C}C, "
        f"batch check every {GPU_BATCH_CHECK_INTERVAL} batches"
    )
    print(f"  Class Weights: {class_weights_dict}")

    run_summary = {
        "model": "ConvNeXtTiny Robust Single Model",
        "seed": SEED,
        "img_size": IMG_SIZE,
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "label_smoothing": LABEL_SMOOTHING,
        "initial_lr": INITIAL_LR,
        "swa_start_epoch": EPOCHS - 5,
        "total_params": total_params,
        "trainable_params": trainable_params,
        "class_weights": {str(k): float(v) for k, v in class_weights_dict.items()},
        "split_info_path": SPLIT_INFO_PATH,
        "dataset_path": DATASET_PATH,
        "include_preprocessing": True,
        "input_value_range": "raw RGB 0-255",
        "trainable_backbone_scope": "convnext_tiny_stage_3 plus final layer_normalization",
        "gpu_temperature_limit_c": GPU_MAX_TEMP_C,
        "gpu_resume_temperature_c": GPU_RESUME_TEMP_C,
        "gpu_cooldown_seconds": GPU_COOLDOWN_SECONDS,
        "gpu_batch_check_interval": GPU_BATCH_CHECK_INTERVAL,
    }
    with open(os.path.join(OUTPUT_DIR, "run_summary_convnexttiny.json"), "w", encoding="utf-8") as f:
        json.dump(run_summary, f, indent=4)

    loss_fn = tf.keras.losses.CategoricalCrossentropy(label_smoothing=LABEL_SMOOTHING)
    model.compile(optimizer=Adam(learning_rate=INITIAL_LR), loss=loss_fn, metrics=["accuracy"])

    model_path = os.path.join(MODEL_DIR, "convnexttiny_robust_seed42.weights.h5")
    swa_path = os.path.join(MODEL_DIR, "convnexttiny_robust_seed42_swa.weights.h5")
    gpu_log_path = os.path.join(OUTPUT_DIR, "gpu_temperature_log.csv")

    callbacks = [
        EpochTrackingCallback(),
        ModelCheckpoint(model_path, monitor="val_accuracy", save_best_only=True, verbose=1, save_weights_only=True),
        LearningRateScheduler(cosine_decay),
        SWACallback(start_epoch=EPOCHS - 5, swa_path=swa_path),
        GPUTemperatureCallback(log_path=gpu_log_path),
    ]

    train_gen = AugmentedMixupGenerator(
        X_train,
        y_train,
        batch_size=BATCH_SIZE,
        augment_gen=get_augmenter(),
        alpha=0.1,
        class_weights_dict=class_weights_dict,
    )

    history = model.fit(
        train_gen,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    save_training_history(history)

    print("\nLoading SWA weights for final evaluation...")
    model.load_weights(swa_path)
    accuracy, eval_payload = evaluate_swa_model(model, X_test, y_test)

    run_summary["final_accuracy"] = accuracy
    run_summary["final_accuracy_percent"] = round(accuracy * 100, 2)
    run_summary["total_errors"] = eval_payload["total_errors"]
    with open(os.path.join(OUTPUT_DIR, "run_summary_convnexttiny.json"), "w", encoding="utf-8") as f:
        json.dump(run_summary, f, indent=4)

    print("\n" + "=" * 60)
    print("ConvNeXtTiny Robust Training Complete")
    print(f"Final SWA Accuracy: {accuracy * 100:.2f}%")
    print(f"Outputs saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    train_model()
