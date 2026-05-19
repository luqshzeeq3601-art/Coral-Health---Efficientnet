"""
=============================================================
  ROBUSTNESS TESTING
  Coral Health - EfficientNetB0 V4 Robust
=============================================================
  Tests model under real-world underwater degradation:
    - Gaussian Noise (sensor noise)
    - Motion Blur   (camera movement)
    - JPEG Compression (transmission artefacts)
    - Brightness shift (lighting depth changes)
    - Colour jitter  (water turbidity / white balance)
  Outputs: robustness_results.json, robustness_report.txt,
           robustness_bar_chart.png
=============================================================
"""
import os, sys, io, json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input
from sklearn.metrics import classification_report
import cv2
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── CONFIG ────────────────────────────────────────────────
IMG_SIZE     = 224
CLASS_NAMES  = ['Healthy', 'Bleached', 'Dead']
SEEDS        = [42, 43, 44, 45, 46]
TTA_SCALES   = [224, 256]
SPLIT_INFO   = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral\split_info_v3.json"
DATASET_PATH = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\Dataset"
MODEL_DIR    = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral\models"
OUTPUT_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── CORRUPTION FUNCTIONS ──────────────────────────────────
def apply_gaussian_noise(img, sigma=15):
    """Simulate camera sensor noise."""
    noise  = np.random.randn(*img.shape) * sigma
    noisy  = np.clip(img + noise, 0, 255)
    return noisy.astype('float32')

def apply_motion_blur(img, kernel_size=11):
    """Simulate camera shake / diver movement."""
    kernel = np.zeros((kernel_size, kernel_size))
    kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
    kernel /= kernel_size
    blurred = cv2.filter2D(img.astype(np.uint8), -1, kernel)
    return blurred.astype('float32')

def apply_jpeg_compression(img, quality=25):
    """Simulate lossy image transmission."""
    uint_img = img.astype(np.uint8)
    _, enc    = cv2.imencode('.jpg', cv2.cvtColor(uint_img, cv2.COLOR_RGB2BGR),
                             [cv2.IMWRITE_JPEG_QUALITY, quality])
    dec      = cv2.imdecode(enc, cv2.IMREAD_COLOR)
    return cv2.cvtColor(dec, cv2.COLOR_BGR2RGB).astype('float32')

def apply_brightness(img, factor=0.5):
    """Simulate deep / shallow water lighting."""
    return np.clip(img * factor, 0, 255).astype('float32')

def apply_color_jitter(img):
    """Simulate water turbidity / white balance drift."""
    img = img.astype('float32')
    img[:, :, 0] = np.clip(img[:, :, 0] * np.random.uniform(0.7, 1.3), 0, 255)
    img[:, :, 1] = np.clip(img[:, :, 1] * np.random.uniform(0.7, 1.3), 0, 255)
    img[:, :, 2] = np.clip(img[:, :, 2] * np.random.uniform(0.7, 1.3), 0, 255)
    return img

CORRUPTIONS = {
    'Clean (Baseline)'    : lambda x: x,
    'Gaussian Noise σ=15' : lambda x: apply_gaussian_noise(x, 15),
    'Gaussian Noise σ=30' : lambda x: apply_gaussian_noise(x, 30),
    'Motion Blur k=11'    : lambda x: apply_motion_blur(x, 11),
    'JPEG Compression Q=25': lambda x: apply_jpeg_compression(x, 25),
    'JPEG Compression Q=10': lambda x: apply_jpeg_compression(x, 10),
    'Brightness 50%'      : lambda x: apply_brightness(x, 0.5),
    'Brightness 150%'     : lambda x: apply_brightness(x, 1.5),
    'Color Jitter'        : lambda x: apply_color_jitter(x),
}

# ── DATA ──────────────────────────────────────────────────
def load_test_set():
    if os.path.exists(SPLIT_INFO):
        print(f"  Loading split from {SPLIT_INFO}")
        with open(SPLIT_INFO) as f:
            split = json.load(f)
        test_files = split.get('test_files', [])
        paths, labels = [], []
        for fname in test_files:
            full = os.path.join(DATASET_PATH, fname)
            if os.path.exists(full):
                cls = fname.split('/')[0]
                if cls in CLASS_NAMES:
                    paths.append(full)
                    labels.append(CLASS_NAMES.index(cls))
        return paths, np.array(labels)
    else:
        print("  split_info_v3.json not found - loading all data as test set")
        paths, labels = [], []
        for ci, cls in enumerate(CLASS_NAMES):
            d = os.path.join(DATASET_PATH, cls)
            if not os.path.exists(d): continue
            for f in sorted(os.listdir(d)):
                if f.lower().endswith(('.png','.jpg','.jpeg')):
                    paths.append(os.path.join(d, f))
                    labels.append(ci)
        return paths, np.array(labels)

def load_image(path):
    img = cv2.imread(path)
    if img is None: return None
    return cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
                      (IMG_SIZE, IMG_SIZE)).astype('float32')

# ── MODEL ─────────────────────────────────────────────────
def build_model():
    base = EfficientNetB0(include_top=False, weights='imagenet',
                          input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base.trainable = True
    for layer in base.layers[:-100]:
        layer.trainable = False
    return Sequential([Input(shape=(IMG_SIZE, IMG_SIZE, 3)), base,
                       GlobalAveragePooling2D(), Dropout(0.4),
                       Dense(3, activation='softmax',
                             kernel_regularizer=tf.keras.regularizers.l2(0.0002))])

def load_ensemble():
    models = []
    for s in SEEDS:
        p = os.path.join(MODEL_DIR, f"efficientnetb0_v4robust_seed{s}_swa.h5")
        if not os.path.exists(p):
            p = os.path.join(MODEL_DIR, f"efficientnetb0_v4robust_seed{s}_swa.weights.h5")
        if not os.path.exists(p):
            print(f"  WARNING: Missing weights seed {s}"); continue
        m = build_model(); m.load_weights(p)
        models.append(m); print(f"  Loaded seed {s}")
    return models

def predict_tta(models, X):
    preds = []
    for img in X:
        tta = []
        u8  = img.astype(np.uint8) if img.max() > 1.0 else (img*255).astype(np.uint8)
        for scale in TTA_SCALES:
            sc  = cv2.resize(u8, (scale, scale))
            inp = sc if scale == IMG_SIZE else sc[(scale-IMG_SIZE)//2:(scale-IMG_SIZE)//2+IMG_SIZE,
                                                  (scale-IMG_SIZE)//2:(scale-IMG_SIZE)//2+IMG_SIZE]
            for m in models:
                preds_ = m.predict(np.expand_dims(inp.astype('float32'), 0), verbose=0)[0]
                tta.append(preds_)
                tta.append(m.predict(np.expand_dims(cv2.flip(inp, 1).astype('float32'), 0), verbose=0)[0])
        preds.append(np.mean(tta, axis=0))
    return np.array(preds)

# ── MAIN ──────────────────────────────────────────────────
def run_robustness():
    print("="*60)
    print("  ROBUSTNESS TESTING - Underwater Degradation Suite")
    print("="*60)

    print("\n📂 Loading test set...")
    test_paths, test_labels = load_test_set()
    print(f"  Test images: {len(test_paths)}")

    print("\n🔧 Loading ensemble...")
    models = load_ensemble()
    if not models:
        print("❌ No models. Check MODEL_DIR."); return

    # Load clean images once
    print("\n  Loading clean images...")
    X_clean, valid_idx = [], []
    for i, p in enumerate(test_paths):
        img = load_image(p)
        if img is not None:
            X_clean.append(img); valid_idx.append(i)
    X_clean = np.array(X_clean)
    y_true  = test_labels[valid_idx]
    print(f"  Valid images: {len(X_clean)}")

    np.random.seed(42)  # for color jitter reproducibility
    results = {}

    for name, corrupt_fn in CORRUPTIONS.items():
        print(f"\n  ── {name} ──")
        X_corrupt = np.array([corrupt_fn(img) for img in X_clean])
        preds     = predict_tta(models, X_corrupt)
        yp        = np.argmax(preds, axis=1)
        acc       = float(np.mean(yp == y_true))

        rep = classification_report(y_true, yp, target_names=CLASS_NAMES,
                                    output_dict=True, zero_division=0)
        results[name] = {
            'accuracy': acc,
            'macro_f1': rep['macro avg']['f1-score'],
            'per_class': {cls: {'f1': rep[cls]['f1-score'],
                                'precision': rep[cls]['precision'],
                                'recall': rep[cls]['recall']}
                          for cls in CLASS_NAMES}
        }
        print(f"     Accuracy: {acc*100:.2f}%  |  Macro F1: {rep['macro avg']['f1-score']:.4f}")

    # ── Save JSON ──────────────────────────────────────────
    with open(os.path.join(OUTPUT_DIR, 'robustness_results.json'), 'w') as f:
        json.dump(results, f, indent=4)

    # ── Save TXT ───────────────────────────────────────────
    with open(os.path.join(OUTPUT_DIR, 'robustness_report.txt'), 'w', encoding='utf-8') as f:
        f.write("ROBUSTNESS TESTING REPORT\n")
        f.write("EfficientNetB0 V4 Robust (SWA + TTA)\n")
        f.write("="*60 + "\n\n")
        f.write(f"{'Corruption':<30} {'Accuracy':>10}  {'Macro F1':>10}\n")
        f.write("-"*55 + "\n")
        for name, r in results.items():
            f.write(f"{name:<30} {r['accuracy']*100:>9.2f}%  {r['macro_f1']:>10.4f}\n")

    # ── Bar Plot ───────────────────────────────────────────
    names = list(results.keys())
    accs  = [results[n]['accuracy']*100 for n in names]
    f1s   = [results[n]['macro_f1'] for n in names]
    baseline = accs[0]

    x   = np.arange(len(names))
    w   = 0.38
    fig, ax = plt.subplots(figsize=(15, 6), facecolor='white')
    b1  = ax.bar(x - w/2, accs, w, label='Accuracy (%)',
                 color=['#2196F3' if a >= baseline - 2 else '#FF5722' for a in accs],
                 edgecolor='white', linewidth=1.2)
    b2  = ax.bar(x + w/2, [f*100 for f in f1s], w, label='Macro F1 × 100',
                 color=['#4CAF50' if f >= f1s[0] - 0.02 else '#FF9800' for f in f1s],
                 edgecolor='white', linewidth=1.2)
    ax.axhline(baseline, color='#1565C0', linestyle='--', lw=1.5,
               label=f'Baseline: {baseline:.2f}%')
    for bar, v in zip(b1, accs):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                f'{v:.1f}', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=30, ha='right', fontsize=9)
    ax.set_ylabel('Score (%)'); ax.set_ylim([0, 105])
    ax.set_title('Robustness Under Underwater Imaging Degradations',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'robustness_bar_chart.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✅ Done! Outputs → {OUTPUT_DIR}")

if __name__ == "__main__":
    run_robustness()
