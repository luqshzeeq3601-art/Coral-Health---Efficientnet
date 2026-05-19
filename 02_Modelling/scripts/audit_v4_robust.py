import os
import sys
import io
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input
import cv2
import pandas as pd
from tqdm import tqdm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IMG_SIZE = 224
CLASS_NAMES = ['Healthy', 'Bleached', 'Dead']
SEEDS = [42, 43, 44, 45, 46]
TTA_SCALES = [224, 256]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'efficientnetb0_coral', 'models')
SPLIT_INFO_PATH = os.path.join(BASE_DIR, '..', 'efficientnetb0_coral', 'split_info_v3.json')

def build_model():
    base_model = EfficientNetB0(include_top=False, weights=None, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = True
    for layer in base_model.layers[:-100]:
        layer.trainable = False
    
    model = Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        GlobalAveragePooling2D(),
        Dropout(0.6),
        Dense(3, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2(0.0001))
    ])
    return model

def temperature_scale_from_probs(probs, temperature):
    """Apply temperature scaling using probability domain: p^(1/T) then renormalize."""
    probs = np.asarray(probs, dtype=np.float64)
    probs = np.clip(probs, 1e-8, 1.0)
    if temperature is None or temperature <= 0:
        return probs / np.sum(probs)
    scaled = np.power(probs, 1.0 / float(temperature))
    scaled_sum = np.sum(scaled)
    if scaled_sum <= 0:
        return probs / np.sum(probs)
    return scaled / scaled_sum

def run_robust_audit(dataset_path):
    print(f"\n🔍 Starting V4 ROBUST Model Audit (SWA + Multi-Scale TTA)...")
    
    if not os.path.exists(SPLIT_INFO_PATH):
        print("❌ Split info not found.")
        return

    with open(SPLIT_INFO_PATH, 'r') as f:
        split_info = json.load(f)

    test_files = set(split_info['test_files'])
    
    print("\n🚀 Loading V4 SWA Ensemble Models...")
    models = []
    for seed in SEEDS:
        swa_path = os.path.join(MODEL_DIR, f"efficientnetb0_v4robust_seed{seed}_swa.h5")
        if os.path.exists(swa_path):
            try:
                model = build_model()
                model.load_weights(swa_path)
                models.append(model)
                print(f"   ✅ Loaded Robust Seed {seed}")
            except Exception as e:
                print(f"⚠️ Warning: Could not load {swa_path}: {e}")
        else:
             print(f"⚠️ Warning: Robust model not found for seed {seed}")

    if not models:
        print("❌ No models loaded. Exiting.")
        return

    # Load Calibration Artifacts
    temperature = 1.0
    ensemble_weights = None
    
    temp_path = os.path.join(MODEL_DIR, 'temperature.txt')
    weights_path = os.path.join(MODEL_DIR, 'ensemble_weights.npy')
    
    if os.path.exists(temp_path):
        with open(temp_path, 'r') as f:
            temperature = float(f.read().strip())
        print(f"🌡️ Loaded Temperature: {temperature:.4f}")
        
    if os.path.exists(weights_path):
        raw_weights = np.load(weights_path).astype(np.float64)
        ensemble_weights = raw_weights / np.sum(raw_weights)
        print(f"⚖️ Loaded Ensemble Weights: {ensemble_weights}")

    image_data = []
    for class_name in CLASS_NAMES:
        class_dir = os.path.join(dataset_path, class_name)
        if not os.path.exists(class_dir):
            class_dir = os.path.join(dataset_path, class_name.lower())

        if os.path.exists(class_dir):
            for img_name in sorted(os.listdir(class_dir)):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    key = f"{class_name}/{img_name}"
                    if key in test_files:
                        image_data.append({
                            'path': os.path.join(class_dir, img_name),
                            'filename': img_name,
                            'true_label': class_name
                        })

    print(f"📸 Test Images Found: {len(image_data)}")

    results = []
    correct_count = 0

    print("\n⚡ Running Calibrated Inference...")
    for item in tqdm(image_data):
        img_path = item['path']
        true_label = item['true_label']

        try:
            # OpenCV preprocessing — matches train_v4_robust.py and app.py exactly
            img_bgr = cv2.imread(img_path)
            if img_bgr is None:
                print(f"⚠️ Could not read {img_path}")
                continue
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            img_224 = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))  # uint8, INTER_LINEAR

            # Multi-Scale TTA — matches train_v4_robust.py predict_with_tta() exactly
            all_tta_preds = []  # Flat list across all models × TTA views
            for scale in TTA_SCALES:
                scaled_img = cv2.resize(img_224, (scale, scale))
                if scale == IMG_SIZE:
                    inp = scaled_img
                else:
                    # Center Crop to IMG_SIZE
                    start = (scale - IMG_SIZE) // 2
                    inp = scaled_img[start:start+IMG_SIZE, start:start+IMG_SIZE]

                # Original + Horizontal Flip
                inp_orig = np.expand_dims(inp.astype('float32'), axis=0)
                inp_flip = np.expand_dims(cv2.flip(inp, 1).astype('float32'), axis=0)

                for model in models:
                    all_tta_preds.append(model.predict(inp_orig, verbose=0)[0])
                    all_tta_preds.append(model.predict(inp_flip, verbose=0)[0])

            # Average ALL (model × TTA view) predictions — matches training evaluation
            avg_probs = np.mean(all_tta_preds, axis=0)

            # Apply Temperature Scaling Calibration
            avg_probs = temperature_scale_from_probs(avg_probs, temperature)
            
            pred_idx = int(np.argmax(avg_probs))
            pred_label = CLASS_NAMES[pred_idx]
            confidence = avg_probs[pred_idx] * 100

            is_correct = (pred_label == true_label)
            if is_correct:
                correct_count += 1

            results.append({
                'Filename': item['filename'],
                'True Label': true_label,
                'Predicted Label': pred_label,
                'Confidence (%)': f"{confidence:.2f}",
                'Correct': is_correct
            })
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    accuracy = (correct_count / len(results)) * 100 if results else 0
    print("\n" + "=" * 55)
    print(f"✅ V4 ROBUST Test Accuracy: {accuracy:.2f}% ({correct_count}/{len(results)})")
    
    # Write to canonical root evaluation directory (not model-local subfolder)
    # BASE_DIR = .../02_Modelling/scripts/, two parents up = BASEPROJECT/
    output_dir = os.path.normpath(os.path.join(
        os.path.dirname(os.path.dirname(BASE_DIR)),
        "03_Model_Evaluation", "Validation_Data", "02_Deployment_Phase"
    ))
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "robust_v4_audit_results.csv")
    df = pd.DataFrame(results)
    df.to_csv(csv_path, index=False)
    print(f"📝 Report saved to: {csv_path}")

if __name__ == "__main__":
    dataset_path = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\Dataset"
    run_robust_audit(dataset_path)
