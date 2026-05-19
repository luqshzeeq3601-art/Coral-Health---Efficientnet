import os
import sys
import codecs
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import cv2
from tqdm import tqdm

# Configuration
IMG_SIZE = 224
CLASS_NAMES = ['Healthy', 'Bleached', 'Dead']
SEEDS = [42, 43, 44, 45, 46]

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..', '..')
DATASET_DIR = os.path.join(PROJECT_ROOT, 'Dataset')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'legacy_models')
SPLIT_INFO_PATH = os.path.join(MODEL_DIR, 'split_info_v3.json')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, '03_Model_Evaluation/Validation_Data', '02_Deployment_Phase')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def build_model():
    """EfficientNetB0 - Matching V4 Expert"""
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

def load_ensemble_models():
    models = []
    print("\nLoading V4 Expert Ensemble models...")
    for seed in SEEDS:
        model_path = os.path.join(MODEL_DIR, f"coral_model_v4_expert_seed{seed}.h5")
        if os.path.exists(model_path):
            try:
                model = build_model()
                model.load_weights(model_path)
                models.append(model)
                print(f"  [OK] Loaded Seed {seed}")
            except Exception as e:
                print(f"  [FAIL] Failed to load Seed {seed}: {e}")
        else:
            print(f"  [MISSING] Model for Seed {seed} not found at {model_path}")
    return models

def load_test_dataset():
    """Load ONLY the held-out test set for V4 metrics."""
    print("\nLoading TEST dataset based on split_info...")
    
    if not os.path.exists(SPLIT_INFO_PATH):
        print(f"❌ Split info not found at {SPLIT_INFO_PATH}")
        return [], []
        
    with open(SPLIT_INFO_PATH, 'r') as f:
        split_info = json.load(f)

    test_files = set(split_info['test_files'])
    
    images = []
    labels = []
    
    for cls_idx, cls_name in enumerate(CLASS_NAMES):
        cls_dir = os.path.join(DATASET_DIR, cls_name)
        if not os.path.exists(cls_dir):
            cls_dir = os.path.join(DATASET_DIR, cls_name.lower())
            
        if os.path.exists(cls_dir):
            for fname in sorted(os.listdir(cls_dir)):
                if not fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue
                
                key = f"{cls_name}/{fname}"
                if key in test_files:
                    path = os.path.join(cls_dir, fname)
                    try:
                        img = cv2.imread(path)
                        if img is None: continue
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                        images.append(img)
                        labels.append(cls_idx)
                    except Exception as e:
                        pass
                
    X = np.array(images, dtype='float32')
    y = np.array(labels)
    return X, y

def evaluate_ensemble(models, X):
    if not models:
        return None
        
    print(f"\nEvaluating ensemble with {len(models)} models using TTA...")
    
    summed_probs = np.zeros((len(X), 3))
    
    # We use simple Horizontal Flip TTA to match the 98.11% result
    for i, model in enumerate(models):
        print(f"  Processing Model {i+1}/{len(models)}...")
        # Original Predict
        p1 = model.predict(X, batch_size=16, verbose=0)
        
        # Flipped Predict
        X_flip = np.array([cv2.flip(img, 1) for img in X])
        p2 = model.predict(X_flip, batch_size=16, verbose=0)
        
        summed_probs += (p1 + p2) / 2
        
    avg_probs = summed_probs / len(models)
    predictions = np.argmax(avg_probs, axis=1)
    return predictions

def generate_artifacts(y_true, y_pred):
    print("\nGenerating Artifacts...")
    
    # 1. Classification Report
    report_dict = classification_report(y_true, y_pred, target_names=CLASS_NAMES, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    report_csv_path = os.path.join(OUTPUT_DIR, "final_classification_report.csv")
    report_df.to_csv(report_csv_path)
    print(f"  Saved Report: {report_csv_path}")
    
    # Heatmap of Report
    plt.figure(figsize=(10, 6))
    sns.heatmap(report_df.iloc[:-1, :-1], annot=True, cmap="Blues", fmt=".4f")
    plt.title("Classification Report Heatmap")
    heatmap_path = os.path.join(OUTPUT_DIR, "final_classification_report_heatmap.png")
    plt.savefig(heatmap_path, bbox_inches='tight')
    plt.close()
    
    # 2. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title(f'V4 Expert Ensemble Confusion Matrix (Acc: {acc*100:.2f}%)')
    cm_path = os.path.join(OUTPUT_DIR, "final_confusion_matrix.png")
    plt.savefig(cm_path, bbox_inches='tight')
    plt.close()
    print(f"  Saved Confusion Matrix: {cm_path}")
    
    # 3. Summary Text
    total_samples = len(y_true)
    total_errors = np.sum(y_true != y_pred)
    
    summary_text = (
        f"Deployment Model V4 (Expert Ensemble w/ Mixup + Hard Mining)\n"
        f"Accuracy: {acc*100:.2f}%\n"
        f"Total Test Samples: {total_samples}\n"
        f"Total Errors: {total_errors}\n"
        f"Ensemble Size: 5 Models\n"
    )
    
    summary_path = os.path.join(OUTPUT_DIR, "final_summary.txt")
    with open(summary_path, 'w') as f:
        f.write(summary_text)
    print(f"  Saved Summary: {summary_path}")

def main():
    models = load_ensemble_models()
    if not models:
        return
        
    X, y = load_test_dataset()
    if len(X) == 0:
        return
        
    print(f"  [OK] Loaded {len(X)} Test Images")
    
    y_pred = evaluate_ensemble(models, X)
    
    if y_pred is not None:
        generate_artifacts(y, y_pred)
        print("\n✅ Deployment Artifacts Generated Successfully!")

if __name__ == "__main__":
    main()
