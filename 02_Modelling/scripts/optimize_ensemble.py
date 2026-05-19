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
from scipy.optimize import minimize

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IMG_SIZE = 224
CROP_SIZE = 224
RESIZE_DIM = 256
CLASS_NAMES = ['Healthy', 'Bleached', 'Dead']
SEEDS = [42, 43, 44, 45, 46]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, '..', 'legacy_models')
SPLIT_INFO_PATH = os.path.join(MODEL_DIR, 'split_info_v3.json')

def build_model():
    base_model = EfficientNetB0(include_top=False, weights=None, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = True
    for layer in base_model.layers[:-50]:
        layer.trainable = False
    
    model = Sequential([
        Input(shape=(IMG_SIZE, IMG_SIZE, 3)),
        base_model,
        GlobalAveragePooling2D(),
        Dropout(0.5), 
        Dense(3, activation='softmax')
    ])
    return model

def get_10_crops(img, resize_dim=256, crop_size=224):
    img = cv2.resize(img, (resize_dim, resize_dim))
    crops = []
    x_center = (resize_dim - crop_size) // 2
    y_center = (resize_dim - crop_size) // 2
    crops.append(img[0:crop_size, 0:crop_size])
    crops.append(img[0:crop_size, resize_dim-crop_size:resize_dim])
    crops.append(img[resize_dim-crop_size:resize_dim, 0:crop_size])
    crops.append(img[resize_dim-crop_size:resize_dim, resize_dim-crop_size:resize_dim])
    crops.append(img[y_center:y_center+crop_size, x_center:x_center+crop_size])
    flips = [cv2.flip(c, 1) for c in crops]
    crops.extend(flips)
    return np.array(crops)

def optimize_ensemble(dataset_path):
    print(f"\n🔍 Starting Ensemble Optimization...")
    
    with open(SPLIT_INFO_PATH, 'r') as f:
        split_info = json.load(f)
    test_files = set(split_info['test_files'])
    
    # Load Models
    models = []
    for seed in SEEDS:
        model_name = os.path.join(MODEL_DIR, f"coral_model_v4_expert_seed{seed}.h5")
        if os.path.exists(model_name):
            model = build_model()
            model.load_weights(model_name)
            models.append(model)
            print(f"   ✅ Loaded Seed {seed}")
            
    if not models: return

    print("\n⚡ Pre-computing predictions...")
    label_list = []
    
    # Reload with full paths to verify order
    full_image_data = [] # List of tuples (path, label_idx)
    with open(SPLIT_INFO_PATH, 'r') as f:
        split_info = json.load(f)
    test_files = set(split_info['test_files'])

    for class_name in CLASS_NAMES:
        class_dir = os.path.join(dataset_path, class_name)
        if not os.path.exists(class_dir): class_dir = os.path.join(dataset_path, class_name.lower())
        if os.path.exists(class_dir):
            for img_name in sorted(os.listdir(class_dir)):
                if f"{class_name}/{img_name}" in test_files:
                     full_image_data.append((os.path.join(class_dir, img_name), CLASS_NAMES.index(class_name)))
                     
    image_data = [x[0] for x in full_image_data]
    labels = np.array([x[1] for x in full_image_data])
    
    print(f"Processing {len(image_data)} images...")
    all_preds = np.zeros((len(image_data), len(models), 3))

    for i, img_path in enumerate(tqdm(image_data)):
        try:
            img = cv2.imread(img_path)
            if img is None: continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            crops = get_10_crops(img, resize_dim=RESIZE_DIM, crop_size=CROP_SIZE).astype('float32') # (10, 224, 224, 3)
            
            for m_idx, model in enumerate(models):
                p = model.predict(crops, verbose=0) # (10, 3)
                all_preds[i, m_idx] = np.mean(p, axis=0) # (3,)
        except Exception as e:
            print(f"Error {img_path}: {e}")
            
    # Save partial results
    np.save(os.path.join(MODEL_DIR, "all_preds_cache.npy"), all_preds)
    np.save(os.path.join(MODEL_DIR, "labels_cache.npy"), labels)

    # Optimization Objective: Maximize Accuracy
    def accuracy_score(weights):
        # Weights shape (Num_Models,)
        w = weights / np.sum(weights) # Normalize
        # Weighted average of predictions
        # all_preds: (N, M, 3)
        # weighted_preds: (N, 3)
        weighted_preds = np.tensordot(all_preds, w, axes=([1],[0]))
        final_preds = np.argmax(weighted_preds, axis=1)
        acc = np.mean(final_preds == labels)
        return -acc # Minimize negative accuracy

    # Initial weights: equal
    init_weights = np.ones(len(models)) / len(models)
    bounds = [(0, 1) for _ in range(len(models))]
    constraints = ({'type': 'eq', 'fun': lambda w: 1 - np.sum(w)})
    
    print("\n⚖️ Optimizing Weights...")
    result = minimize(accuracy_score, init_weights, bounds=bounds, constraints=constraints)
    
    best_weights = result.x / np.sum(result.x)
    best_acc = -result.fun * 100
    
    print("\n" + "="*55)
    print(f"🏆 Best Accuracy: {best_acc:.2f}%")
    print("Optimal Weights:")
    for seed, w in zip(SEEDS, best_weights):
        print(f"  Seed {seed}: {w:.4f}")
    
    # Save weights
    np.save(os.path.join(MODEL_DIR, 'ensemble_weights.npy'), best_weights)
    print(f"💾 Saved weights to {os.path.join(MODEL_DIR, 'ensemble_weights.npy')}")

if __name__ == "__main__":
    import kagglehub
    try:
        path = kagglehub.dataset_download("sonainjamil/bhd-corals")
        dataset_path = os.path.join(path, "Dataset")
        if not os.path.exists(dataset_path): dataset_path = path

        optimize_ensemble(dataset_path)

    except Exception as e:
        print(f"❌ Error: {e}")
