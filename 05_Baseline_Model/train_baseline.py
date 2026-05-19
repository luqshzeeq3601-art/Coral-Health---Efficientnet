import os
import sys
import io
import json
import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.utils import class_weight
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==========================================
# BASELINE CONFIG — No Advanced Techniques
# ==========================================
IMG_SIZE = 224
CLASS_NAMES = ['Healthy', 'Bleached', 'Dead']
SEED = 42
SPLIT_SEED = 42          # Same split as advanced model for fair comparison
EPOCHS = 30
BATCH_SIZE = 16
LEARNING_RATE = 1e-4     # Fixed learning rate (no cosine decay)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')
OUTPUT_ROOT = os.path.join(BASE_DIR, 'outputs')
OUTPUT_DIR = os.path.join(OUTPUT_ROOT, 'baseline_model')
DATASET_PATH = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\Dataset"

# Use same split file as advanced model if it exists
ADVANCED_MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), '02_Modelling', 'efficientnetb0_coral')
SPLIT_INFO_PATH = os.path.join(ADVANCED_MODEL_DIR, 'split_info_v3.json')

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_ROOT, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================
# Dataset Loading Functions
# ==========================================
def collect_file_paths(dataset_path):
    file_paths, labels, filenames = [], [], []
    for cls_idx, cls_name in enumerate(CLASS_NAMES):
        cls_dir = os.path.join(dataset_path, cls_name)
        if not os.path.exists(cls_dir):
            cls_dir = os.path.join(dataset_path, cls_name.lower())
        if os.path.exists(cls_dir):
            for fname in sorted(os.listdir(cls_dir)):
                if not fname.lower().endswith(('.png', '.jpg', '.jpeg')): continue
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
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            images.append(img)
        except:
            images.append(None)
    return images

def split_dataset(dataset_path):
    """Use the same split as the advanced model for fair comparison."""
    if os.path.exists(SPLIT_INFO_PATH):
        print(f"Loading existing split from {SPLIT_INFO_PATH}")
        with open(SPLIT_INFO_PATH, 'r') as f:
            split_info = json.load(f)
        def get_paths(filenames):
            paths, lbls = [], []
            for fname in filenames:
                full = os.path.join(dataset_path, fname)
                if os.path.exists(full):
                    paths.append(full)
                    cls = fname.split('/')[0]
                    if cls in CLASS_NAMES: lbls.append(CLASS_NAMES.index(cls))
            return paths, np.array(lbls)
        train_paths, train_labels = get_paths(split_info['train_files'])
        val_paths, val_labels = get_paths(split_info['val_files'])
        test_paths, test_labels = get_paths(split_info['test_files'])
        return train_paths, train_labels, val_paths, val_labels, test_paths, test_labels
    else:
        print("Creating new split (same seed as advanced model)...")
        file_paths, labels, filenames = collect_file_paths(dataset_path)
        indices = np.arange(len(file_paths))
        train_idx, temp_idx = train_test_split(indices, test_size=0.2, random_state=SPLIT_SEED, stratify=labels)
        temp_labels = labels[temp_idx]
        val_idx, test_idx = train_test_split(temp_idx, test_size=0.5, random_state=SPLIT_SEED, stratify=temp_labels)

        # Save split info so it can be reused
        split_info = {
            'train_files': [filenames[i] for i in train_idx],
            'val_files': [filenames[i] for i in val_idx],
            'test_files': [filenames[i] for i in test_idx],
        }
        split_save_path = os.path.join(BASE_DIR, 'split_info_v3.json')
        with open(split_save_path, 'w') as f:
            json.dump(split_info, f, indent=2)
        print(f"  Split saved to {split_save_path}")

        return ([file_paths[i] for i in train_idx], labels[train_idx],
                [file_paths[i] for i in val_idx],   labels[val_idx],
                [file_paths[i] for i in test_idx],  labels[test_idx])

def prepare_set(paths, labels):
    images = load_images(paths)
    valid_imgs, valid_lbls = [], []
    for img, label in zip(images, labels):
        if img is not None:
            valid_imgs.append(img)
            valid_lbls.append(label)
    X = np.array(valid_imgs, dtype='float32')
    y = tf.keras.utils.to_categorical(np.array(valid_lbls), num_classes=3)
    return X, y

def get_basic_augmenter():
    """Basic augmentation only — no color jitter, no shear, no brightness."""
    return tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=15,
        horizontal_flip=True,
        zoom_range=0.1,
        fill_mode='nearest'
    )

# ==========================================
# Baseline Model — Frozen Backbone
# ==========================================
def build_baseline_model():
    """EfficientNetB0 with ALL base layers frozen. Train classification head only."""
    base_model = EfficientNetB0(include_top=False, weights='imagenet', input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = False  # Freeze ALL layers

    model = Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        GlobalAveragePooling2D(),
        Dense(3, activation='softmax')  # No dropout, no regularization
    ])
    return model

# ==========================================
# Standard Grad-CAM (No Smoothing)
# ==========================================
def make_gradcam_heatmap(img_array, model, layer_name='top_conv'):
    """Standard Grad-CAM — no eigen_smooth, no aug_smooth."""
    efficientnet = None
    for layer in model.layers:
        if 'efficientnet' in layer.name.lower():
            efficientnet = layer
            break
    if efficientnet is None:
        return np.zeros((IMG_SIZE, IMG_SIZE))

    target_layer = None
    try:
        target_layer = efficientnet.get_layer(layer_name)
    except Exception:
        for layer in reversed(efficientnet.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                target_layer = layer
                break
    if target_layer is None:
        return np.zeros((IMG_SIZE, IMG_SIZE))

    grad_model_part1 = tf.keras.models.Model(
        inputs=efficientnet.input,
        outputs=target_layer.output
    )
    try:
        top_bn = efficientnet.get_layer('top_bn')
        top_activation = efficientnet.get_layer('top_activation')
        has_top_layers = True
    except:
        has_top_layers = False

    with tf.GradientTape() as tape:
        conv_outputs = grad_model_part1(img_array)
        tape.watch(conv_outputs)
        x = conv_outputs
        if has_top_layers:
            x = top_bn(x)
            x = top_activation(x)
        eff_index = -1
        for i, layer in enumerate(model.layers):
            if layer == efficientnet:
                eff_index = i
                break
        if eff_index != -1:
            for layer in model.layers[eff_index+1:]:
                x = layer(x)
        model_outputs = x
        pred_idx = tf.argmax(model_outputs[0])
        loss = model_outputs[:, pred_idx]

    grads = tape.gradient(loss, conv_outputs)
    if grads is None:
        return np.zeros((IMG_SIZE, IMG_SIZE))

    # Standard weighted sum — no eigen smooth
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out = conv_outputs[0]
    heatmap = conv_out @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.nn.relu(heatmap)
    heatmap = heatmap.numpy()

    heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
    return heatmap

# ==========================================
# Main Training Function
# ==========================================
def train_model():
    print("=" * 55)
    print("BASELINE - EfficientNetB0 Training (No Advanced Methods)")
    print("=" * 55)

    # ---- Load Dataset ----
    print("\nLoading Dataset...")
    train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = split_dataset(DATASET_PATH)

    X_train, y_train = prepare_set(train_paths, train_labels)
    X_val, y_val = prepare_set(val_paths, val_labels)
    X_test, y_test = prepare_set(test_paths, test_labels)

    print(f"  Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    # ---- Class Weights (standard balanced, no manual boost) ----
    y_integers = np.argmax(y_train, axis=1)
    class_weights_arr = class_weight.compute_class_weight(
        class_weight='balanced', classes=np.unique(y_integers), y=y_integers
    )
    class_weights_dict = dict(enumerate(class_weights_arr))
    print(f"  Class Weights (auto balanced): {class_weights_dict}")

    # ---- Build Model ----
    model = build_baseline_model()
    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',  # No label smoothing
        metrics=['accuracy']
    )

    # ---- Save model summary ----
    trainable_params = np.sum([tf.keras.backend.count_params(w) for w in model.trainable_weights])
    total_params = np.sum([tf.keras.backend.count_params(w) for w in model.weights])
    summary_lines = []
    model.summary(print_fn=lambda x: summary_lines.append(x))
    with open(os.path.join(OUTPUT_DIR, 'model_summary.txt'), 'w') as f:
        f.write('\n'.join(summary_lines))
        f.write(f"\n\nTotal Parameters: {int(total_params):,}")
        f.write(f"\nTrainable Parameters: {int(trainable_params):,}")
        f.write(f"\nNon-Trainable Parameters: {int(total_params - trainable_params):,}")
    print(f"  Total params: {int(total_params):,}")
    print(f"  Trainable params: {int(trainable_params):,}")

    # ---- Print Config ----
    print(f"\nTraining Config:")
    print(f"  Model: EfficientNetB0 (Baseline — Frozen Backbone)")
    print(f"  Label Smoothing: None (0.0)")
    print(f"  Learning Rate: Fixed {LEARNING_RATE}")
    print(f"  Ensemble: None (single model)")
    print(f"  Epochs: {EPOCHS} (with EarlyStopping patience=5)")
    print(f"  Batch Size: {BATCH_SIZE}")
    print(f"  SWA: None")
    print(f"  TTA: None")
    print(f"  Mixup: None")

    # ---- Data Augmentation ----
    aug = get_basic_augmenter()

    # ---- Callbacks ----
    model_path = os.path.join(MODEL_DIR, 'efficientnetb0_baseline.weights.h5')
    checkpoint = ModelCheckpoint(model_path, monitor='val_accuracy', save_best_only=True, verbose=1, save_weights_only=True)
    early_stop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True, verbose=1)

    # ---- Train ----
    print(f"\n{'='*40}")
    print(f"--- Training Baseline Model (Seed {SEED}) ---")
    print(f"{'='*40}")

    tf.random.set_seed(SEED)
    np.random.seed(SEED)

    train_start = time.time()
    history = model.fit(
        aug.flow(X_train, y_train, batch_size=BATCH_SIZE),
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        class_weight=class_weights_dict,
        callbacks=[checkpoint, early_stop],
        verbose=1
    )
    train_time = time.time() - train_start
    print(f"\n  Training Time: {train_time:.1f}s ({train_time/60:.1f} min)")

    # ==========================================
    # Training History Plot
    # ==========================================
    print("\n📊 Generating Training History Plot...")
    train_acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    train_loss = history.history['loss']
    val_loss = history.history['val_loss']
    actual_epochs = len(train_acc)

    plt.figure(figsize=(14, 5), facecolor='white')
    epochs_range = range(1, actual_epochs + 1)

    # Accuracy
    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(epochs_range, train_acc, label='Training Accuracy', color='tab:blue', linewidth=2.5)
    ax1.plot(epochs_range, val_acc, label='Validation Accuracy', color='tab:red', linewidth=2.5)
    ax1.set_title('Training and Validation Accuracy (Baseline)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.set_ylim([0.40, 1.00])
    ax1.tick_params(labelsize=11)
    ax1.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='gray', fontsize=11)
    ax1.grid(True, linestyle='--', color='#E0E0E0', alpha=0.5, linewidth=0.7)

    # Loss
    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(epochs_range, train_loss, label='Training Loss', color='tab:blue', linewidth=2.5)
    ax2.plot(epochs_range, val_loss, label='Validation Loss', color='tab:red', linewidth=2.5)
    ax2.set_title('Training and Validation Loss (Baseline)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Loss', fontsize=12)
    ax2.tick_params(labelsize=11)
    ax2.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='gray', fontsize=11)
    ax2.grid(True, linestyle='--', color='#E0E0E0', alpha=0.5, linewidth=0.7)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'training_history.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: training_history.png")

    # Save history JSON
    history_data = {
        'train_acc': train_acc,
        'val_acc': val_acc,
        'train_loss': train_loss,
        'val_loss': val_loss,
        'training_time_seconds': train_time,
        'actual_epochs': actual_epochs,
    }
    with open(os.path.join(OUTPUT_DIR, 'training_history.json'), 'w') as f:
        json.dump(history_data, f, indent=4)
    print(f"  Saved: training_history.json")

    # ==========================================
    # Evaluation — Direct Prediction (No TTA)
    # ==========================================
    print("\n🔍 Evaluating Baseline Model (No TTA, No Ensemble)...")

    # Load best weights
    model.load_weights(model_path)

    # Measure inference time
    inference_start = time.time()
    preds = model.predict(X_test, verbose=0)
    inference_time = time.time() - inference_start
    per_image_time = inference_time / len(X_test)

    y_pred_classes = np.argmax(preds, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)

    accuracy = np.mean(y_pred_classes == y_true_classes)
    print(f"\n✅ Baseline Test Accuracy: {accuracy*100:.2f}%")
    print(f"   Inference Time: {inference_time:.2f}s total, {per_image_time*1000:.1f}ms/image")

    # ==========================================
    # Classification Report
    # ==========================================
    report_text = classification_report(y_true_classes, y_pred_classes, target_names=CLASS_NAMES)
    print("\nBaseline Classification Report:\n", report_text)

    with open(os.path.join(OUTPUT_DIR, 'classification_report.txt'), 'w') as f:
        f.write(f"Baseline (EfficientNetB0) - Single Model, No Advanced Methods\n")
        f.write(f"Test Accuracy: {accuracy*100:.2f}%\n")
        f.write(f"Training Time: {train_time:.1f}s\n")
        f.write(f"Inference Time: {per_image_time*1000:.1f}ms/image\n\n")
        f.write(report_text)

    report_dict = classification_report(y_true_classes, y_pred_classes, target_names=CLASS_NAMES, output_dict=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    ax.set_title('Classification Report - Baseline EfficientNetB0', fontsize=14, fontweight='bold', pad=20)

    headers = ['Class', 'Precision', 'Recall', 'F1-Score', 'Support']
    table_data = []
    for cls_name in CLASS_NAMES:
        row = report_dict[cls_name]
        table_data.append([cls_name, f"{row['precision']:.4f}", f"{row['recall']:.4f}",
                          f"{row['f1-score']:.4f}", f"{int(row['support'])}"])
    table_data.append(['', '', '', '', ''])
    table_data.append(['Accuracy', '', '', f"{report_dict['accuracy']:.4f}",
                      f"{int(report_dict['weighted avg']['support'])}"])
    table_data.append(['Macro Avg', f"{report_dict['macro avg']['precision']:.4f}",
                      f"{report_dict['macro avg']['recall']:.4f}",
                      f"{report_dict['macro avg']['f1-score']:.4f}",
                      f"{int(report_dict['macro avg']['support'])}"])
    table_data.append(['Weighted Avg', f"{report_dict['weighted avg']['precision']:.4f}",
                      f"{report_dict['weighted avg']['recall']:.4f}",
                      f"{report_dict['weighted avg']['f1-score']:.4f}",
                      f"{int(report_dict['weighted avg']['support'])}"])

    table = ax.table(cellText=table_data, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)

    for j in range(len(headers)):
        table[0, j].set_facecolor('#E67E22')
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, len(table_data) + 1):
        for j in range(len(headers)):
            if i <= len(CLASS_NAMES):
                table[i, j].set_facecolor('#FDEBD0')
            else:
                table[i, j].set_facecolor('#F2F2F2')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'classification_report.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: classification_report.png")

    # ==========================================
    # Confusion Matrix
    # ==========================================
    cm = confusion_matrix(y_true_classes, y_pred_classes)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES,
                annot_kws={'size': 14})
    plt.title('Confusion Matrix - Baseline EfficientNetB0', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted', fontsize=12)
    plt.ylabel('Actual', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'confusion_matrix.png'), dpi=150)
    plt.close()
    print(f"  Saved: confusion_matrix.png")

    # ==========================================
    # Standard Grad-CAM Visualization
    # ==========================================
    print("\n🔬 Generating Standard Grad-CAM visualizations...")
    samples = []
    for cls_idx in range(3):
        idxs = np.where(y_true_classes == cls_idx)[0]
        correct_idxs = [j for j in idxs if y_pred_classes[j] == cls_idx]
        if len(correct_idxs) > 0:
            best_idx = max(correct_idxs, key=lambda j: preds[j][cls_idx])
            confidence = preds[best_idx][cls_idx]
            samples.append((X_test[best_idx], cls_idx, y_pred_classes[best_idx], confidence))
        elif len(idxs) > 0:
            confidence = preds[idxs[0]][y_pred_classes[idxs[0]]]
            samples.append((X_test[idxs[0]], y_true_classes[idxs[0]], y_pred_classes[idxs[0]], confidence))

    plt.figure(figsize=(15, 5))
    for i, (img, true_lbl, pred_lbl, conf) in enumerate(samples):
        img_array = np.expand_dims(img, axis=0)
        heatmap = make_gradcam_heatmap(img_array, model)

        plt.subplot(1, len(samples), i+1)
        plt.imshow(img.astype(np.uint8))
        if heatmap.max() > 0:
            plt.imshow(heatmap, cmap='jet', alpha=0.4)
        plt.title(f"True: {CLASS_NAMES[true_lbl]}\nPred: {CLASS_NAMES[pred_lbl]} ({conf*100:.1f}%)", fontsize=11)
        plt.axis('off')

    plt.suptitle('Grad-CAM - Baseline EfficientNetB0 (Standard)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'gradcam_outputs.png'), dpi=150)
    plt.close()
    print(f"  Saved: gradcam_outputs.png")

    # ==========================================
    # Save evaluation summary JSON
    # ==========================================
    eval_summary = {
        'model': 'Baseline EfficientNetB0',
        'accuracy': float(accuracy),
        'training_time_seconds': train_time,
        'inference_time_per_image_ms': per_image_time * 1000,
        'total_params': int(total_params),
        'trainable_params': int(trainable_params),
        'actual_epochs': actual_epochs,
        'per_class': {},
    }
    for cls_name in CLASS_NAMES:
        eval_summary['per_class'][cls_name] = {
            'precision': report_dict[cls_name]['precision'],
            'recall': report_dict[cls_name]['recall'],
            'f1': report_dict[cls_name]['f1-score'],
        }
    eval_summary['macro_avg'] = {
        'precision': report_dict['macro avg']['precision'],
        'recall': report_dict['macro avg']['recall'],
        'f1': report_dict['macro avg']['f1-score'],
    }
    with open(os.path.join(OUTPUT_DIR, 'eval_summary.json'), 'w') as f:
        json.dump(eval_summary, f, indent=4)
    print(f"  Saved: eval_summary.json")

    print(f"\n{'='*55}")
    print(f"✅ BASELINE Training Complete!")
    print(f"   Test Accuracy: {accuracy*100:.2f}%")
    print(f"   All outputs saved to: {OUTPUT_DIR}")
    print(f"{'='*55}")

if __name__ == "__main__":
    train_model()
