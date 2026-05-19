import os
import sys
import io
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input
import cv2
from scipy.optimize import minimize
from tqdm import tqdm

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IMG_SIZE = 224
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

def calculate_temperature(dataset_path):
    print(f"\nTraining Temperature Scaling...")
    
    with open(SPLIT_INFO_PATH, 'r') as f:
        split_info = json.load(f)

    # Use VAL set for calibration (never Test set)
    val_files = set(split_info['val_files'])
    
    models = []
    for seed in SEEDS:
        model_name = os.path.join(MODEL_DIR, f"coral_model_v4_expert_seed{seed}.h5")
        if os.path.exists(model_name):
            m = build_model()
            m.load_weights(model_name)
            # Create a model that outputs Logits (pre-softmax)
            # EfficientNetB0 -> GlobalAvg -> Dropout -> Dense(3)
            # The Dense layer has activation='softmax'. We need to strip it.
            # Efficient implementation: Get the dense layer weights and compute manually?
            # Or reconstruct model without softmax?
            
            # Reconstruct model to output logits
            # m is Sequential: [Input, EfficientNet, GlobalAvg, Dropout, Dense]
            
            # Get weights from the final Dense layer (Softmax)
            dense_layer = m.layers[-1]
            dense_weights = dense_layer.get_weights() # [W, b]
            
            # Create a new model that outputs the features (before Dense)
            # Input -> ... -> Dropout
            feature_model = Model(inputs=m.input, outputs=m.layers[-2].output)
            
            # Create the Logit Model
            x = feature_model.output
            # Create new Dense with LINEAR activation
            x = Dense(3, activation='linear')(x)
            logit_model = Model(inputs=feature_model.input, outputs=x)
            
            # Set weights
            logit_model.layers[-1].set_weights(dense_weights)
            
            models.append(logit_model)

    if not models: return

    # Collect Val Data
    image_data = []
    labels = []
    
    # 10-Crop TTA settings
    RESIZE_DIM = 256
    CROP_SIZE = 224

    def get_10_crops(img):
        img_r = cv2.resize(img, (RESIZE_DIM, RESIZE_DIM))
        crops = []
        x_c = (RESIZE_DIM - CROP_SIZE) // 2
        y_c = (RESIZE_DIM - CROP_SIZE) // 2
        crops.append(img_r[y_c:y_c+CROP_SIZE, x_c:x_c+CROP_SIZE]) # C
        crops.append(img_r[0:CROP_SIZE, 0:CROP_SIZE]) # TL
        crops.append(img_r[0:CROP_SIZE, RESIZE_DIM-CROP_SIZE:RESIZE_DIM]) # TR
        crops.append(img_r[RESIZE_DIM-CROP_SIZE:RESIZE_DIM, 0:CROP_SIZE]) # BL
        crops.append(img_r[RESIZE_DIM-CROP_SIZE:RESIZE_DIM, RESIZE_DIM-CROP_SIZE:RESIZE_DIM]) # BR
        flips = [cv2.flip(c, 1) for c in crops]
        crops.extend(flips)
        return np.array(crops).astype('float32')

    print("Collecting Validation Data...")
    for class_name in CLASS_NAMES:
        class_dir = os.path.join(dataset_path, class_name)
        if not os.path.exists(class_dir): class_dir = os.path.join(dataset_path, class_name.lower())
        if os.path.exists(class_dir):
            for img_name in sorted(os.listdir(class_dir)):
                # Match only files in the VAL set
                if f"{class_name}/{img_name}" in val_files:
                    path = os.path.join(class_dir, img_name)
                    try:
                        img = cv2.imread(path)
                        if img is None: continue
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        image_data.append(img)
                        labels.append(CLASS_NAMES.index(class_name))
                    except: pass
    
    labels = np.array(labels)
    print(f"Validation Samples: {len(labels)}")
    if len(labels) == 0:
        print("❌ No validation samples found. Check split_info.json path.")
        return

    all_logits = []

    print("Computing Logits...")
    for img in tqdm(image_data):
        crops = get_10_crops(img)
        
        ensemble_logits = np.zeros(3)
        for model in models:
            l = model.predict(crops, verbose=0) # (10, 3)
            ensemble_logits += np.mean(l, axis=0)
            
        avg_logits = ensemble_logits / len(models)
        all_logits.append(avg_logits)
        
    all_logits = np.array(all_logits) # (N, 3)

    # ---------------------------------------------------------
    # PART 2: Feature Centroids for Anomaly Detection
    # ---------------------------------------------------------
    print("\nComputing Feature Centroids...")
    
    # We need a model that outputs FEATURES (before Dense)
    # The first model in 'legacy_models' list is (Input -> ... -> Dropout -> Dense(Linear))
    # We want (Input -> ... -> Dropout)
    # Let's create a feature extractor from the first seed model
    # Note: features will be slightly different per seed. 
    # Proper way: Average features from all ensembles? Or just use one?
    # Ensemble features is best.
    
    feature_models = []
    for m in models:
        # m is the Logit Model (Input...DenseLinear)
        # m.layers[-2] is the Dropout layer (1280)
        fm = Model(inputs=m.input, outputs=m.layers[-2].output)
        feature_models.append(fm)
        
    all_features = []
    
    for img in tqdm(image_data):
        crops = get_10_crops(img)
        
        ensemble_feats = np.zeros(1280)
        for fm in feature_models:
            f = fm.predict(crops, verbose=0) # (10, 1280)
            ensemble_feats += np.mean(f, axis=0)
            
        avg_feats = ensemble_feats / len(models)
        all_features.append(avg_feats)
        
    all_features = np.array(all_features) # (N, 1280)
    
    # Compute Centroids
    centroids = {}
    distances = {0:[], 1:[], 2:[]}
    
    img_names_processed = [] 
    # We need to map back to filenames to find 80.png if it was in val? 
    # But 80.png is in TEST set. So it's not here.
    
    for cls_idx in range(3):
        cls_feats = all_features[labels == cls_idx]
        if len(cls_feats) == 0:
            print(f"⚠️ No samples for class {cls_idx}")
            continue
            
        centroid = np.mean(cls_feats, axis=0)
        centroids[cls_idx] = centroid
        
        # Compute distances
        dists = np.linalg.norm(cls_feats - centroid, axis=1)
        distances[cls_idx] = dists
        
        print(f"Class {CLASS_NAMES[cls_idx]}:")
        print(f"  Mean Dist: {np.mean(dists):.4f}")
        print(f"  Max Dist:  {np.max(dists):.4f}")
        print(f"  95th %ile: {np.percentile(dists, 95):.4f}")

    # Save Centroids
    np.save(os.path.join(MODEL_DIR, "centroids.npy"), centroids)
    
    # Calculate Global Max Distance Threshold (e.g. max of 99th percentiles)
    thresholds = [np.percentile(distances[i], 99) for i in range(3) if len(distances[i]) > 0]
    global_threshold = np.max(thresholds) if thresholds else 0
    print(f"\n🛡️ Recommended Anomaly Threshold (Distance): {global_threshold:.4f}")
    
    # Save Threshold
    with open(os.path.join(MODEL_DIR, "distance_threshold.txt"), "w") as f:
        f.write(str(global_threshold))

    # Minimize NLL w.r.t Temperature T
    def nll(x):
        T = x[0]
        scaled_logits = all_logits / T
        # Softmax
        exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
        
        # Cross Entropy
        p_true = probs[np.arange(len(labels)), labels]
        p_true = np.clip(p_true, 1e-7, 1.0)
        return -np.mean(np.log(p_true))

    print("Optimizing...")
    res = minimize(nll, x0=[1.0], bounds=[(0.1, 5.0)], method='L-BFGS-B')
    optimal_T = res.x[0]
    
    print("\n" + "="*55)
    print(f"🌡️ Optimal Temperature: {optimal_T:.4f}")
    
    # Test effect on a few examples
    print("\nEffect of Scaling (Validation Sample):")
    orig_l = all_logits[0]
    scaled_l = orig_l / optimal_T
    
    def softmax(z):
        e = np.exp(z - np.max(z))
        return e / np.sum(e)
        
    print(f"  Logits: {orig_l}")
    print(f"  Orig Probs:   {softmax(orig_l)}")
    print(f"  Scaled Probs: {softmax(scaled_l)}")

    # Save
    with open(os.path.join(MODEL_DIR, "temperature.txt"), "w") as f:
        f.write(str(optimal_T))
    
    print("\n" + "="*55)
    print(f"🌡️ Optimal Temperature: {optimal_T:.4f}")
    
    # Save
    with open(os.path.join(MODEL_DIR, "temperature.txt"), "w") as f:
        f.write(str(optimal_T))

if __name__ == "__main__":
    import kagglehub
    try:
        path = kagglehub.dataset_download("sonainjamil/bhd-corals")
        dataset_path = os.path.join(path, "Dataset")
        if not os.path.exists(dataset_path): dataset_path = path
        calculate_temperature(dataset_path)
    except Exception as e:
        print(f"Error: {e}")
