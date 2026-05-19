"""
=============================================================
  CONFIDENCE CALIBRATION ANALYSIS
  Coral Health - EfficientNetB0 V4 Robust
=============================================================
  Measures whether predicted confidence matches actual
  accuracy.  A well-calibrated model that says "90%
  confident" should be correct ~90% of the time.

  Outputs: calibration_results.json, calibration_report.txt,
           reliability_diagram.png, confidence_hist.png
=============================================================
"""
import os, sys, io, json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input
import cv2
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── CONFIG ────────────────────────────────────────────────
IMG_SIZE     = 224
CLASS_NAMES  = ['Healthy', 'Bleached', 'Dead']
SEEDS        = [42, 43, 44, 45, 46]
TTA_SCALES   = [224, 256]
N_BINS       = 10
SPLIT_INFO   = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral\split_info_v3.json"
DATASET_PATH = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\Dataset"
MODEL_DIR    = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral\models"
OUTPUT_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

# ── DATA ──────────────────────────────────────────────────
def load_test_set():
    if os.path.exists(SPLIT_INFO):
        with open(SPLIT_INFO) as f:
            split = json.load(f)
        paths, labels = [], []
        for fname in split.get('test_files', []):
            full = os.path.join(DATASET_PATH, fname)
            if os.path.exists(full):
                cls = fname.split('/')[0]
                if cls in CLASS_NAMES:
                    paths.append(full)
                    labels.append(CLASS_NAMES.index(cls))
        return paths, np.array(labels)
    else:
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
                tta.append(m.predict(np.expand_dims(inp.astype('float32'), 0), verbose=0)[0])
                tta.append(m.predict(np.expand_dims(cv2.flip(inp, 1).astype('float32'), 0), verbose=0)[0])
        preds.append(np.mean(tta, axis=0))
    return np.array(preds)

# ── CALIBRATION METRICS ───────────────────────────────────
def compute_ece(confidences, accuracies, n_bins=10):
    """Expected Calibration Error."""
    bins  = np.linspace(0, 1, n_bins + 1)
    ece   = 0.0
    n     = len(confidences)
    bin_data = []
    for i in range(n_bins):
        lo, hi = bins[i], bins[i+1]
        mask   = (confidences >= lo) & (confidences < hi)
        if i == n_bins - 1:
            mask = (confidences >= lo) & (confidences <= hi)
        count  = mask.sum()
        if count == 0:
            bin_data.append({'lo': lo, 'hi': hi, 'count': 0,
                             'avg_conf': (lo+hi)/2, 'avg_acc': 0.0})
            continue
        avg_conf = confidences[mask].mean()
        avg_acc  = accuracies[mask].mean()
        ece     += (count / n) * abs(avg_conf - avg_acc)
        bin_data.append({'lo': lo, 'hi': hi, 'count': int(count),
                         'avg_conf': float(avg_conf), 'avg_acc': float(avg_acc)})
    return float(ece), bin_data

# ── MAIN ──────────────────────────────────────────────────
def run_calibration():
    print("="*60)
    print("  CONFIDENCE CALIBRATION ANALYSIS")
    print("="*60)

    print("\n📂 Loading test set...")
    test_paths, test_labels = load_test_set()
    print(f"  Test images: {len(test_paths)}")

    print("\n🔧 Loading ensemble...")
    models = load_ensemble()
    if not models:
        print("❌ No models. Check MODEL_DIR."); return

    X_list, valid_idx = [], []
    for i, p in enumerate(test_paths):
        img = load_image(p)
        if img is not None:
            X_list.append(img); valid_idx.append(i)
    X     = np.array(X_list)
    y     = test_labels[valid_idx]
    print(f"  Valid images: {len(X)}")

    print("\n  Running TTA inference...")
    preds = predict_tta(models, X)
    confs  = np.max(preds, axis=1)          # top-class confidence
    yp     = np.argmax(preds, axis=1)
    correct = (yp == y).astype(float)

    acc = float(np.mean(correct))
    print(f"\n  Overall Accuracy : {acc*100:.2f}%")
    print(f"  Mean Confidence  : {confs.mean()*100:.2f}%")
    print(f"  Overconfidence   : {(confs.mean() - acc)*100:.2f}%")

    ece, bin_data = compute_ece(confs, correct, N_BINS)
    print(f"  ECE              : {ece:.4f}")

    # MCE (Maximum Calibration Error)
    mce = max(abs(b['avg_conf'] - b['avg_acc']) for b in bin_data if b['count'] > 0)
    print(f"  MCE              : {mce:.4f}")

    # ── Confidence stats per class ─────────────────────────
    class_stats = {}
    for ci, cls in enumerate(CLASS_NAMES):
        mask    = y == ci
        if mask.sum() == 0: continue
        c_confs = confs[mask]
        c_corr  = correct[mask]
        class_stats[cls] = {
            'n'              : int(mask.sum()),
            'accuracy'       : float(c_corr.mean()),
            'mean_confidence': float(c_confs.mean()),
            'gap'            : float(c_confs.mean() - c_corr.mean()),
        }
        print(f"  {cls:10s} | Acc: {c_corr.mean()*100:.1f}% | "
              f"Conf: {c_confs.mean()*100:.1f}% | "
              f"Gap: {(c_confs.mean()-c_corr.mean())*100:+.1f}%")

    # ── Save JSON ──────────────────────────────────────────
    cal_data = {
        'overall': {'accuracy': acc, 'mean_confidence': float(confs.mean()),
                    'ece': ece, 'mce': float(mce),
                    'overconfidence': float(confs.mean() - acc)},
        'bin_data': bin_data,
        'per_class': class_stats,
    }
    with open(os.path.join(OUTPUT_DIR, 'calibration_results.json'), 'w') as f:
        json.dump(cal_data, f, indent=4)

    # ── Save TXT ───────────────────────────────────────────
    with open(os.path.join(OUTPUT_DIR, 'calibration_report.txt'), 'w', encoding='utf-8') as f:
        f.write("CONFIDENCE CALIBRATION REPORT\n")
        f.write("EfficientNetB0 V4 Robust (SWA + TTA)\n")
        f.write("="*60 + "\n\n")
        f.write(f"Overall Accuracy  : {acc*100:.2f}%\n")
        f.write(f"Mean Confidence   : {confs.mean()*100:.2f}%\n")
        f.write(f"ECE               : {ece:.4f}  (lower is better)\n")
        f.write(f"MCE               : {mce:.4f}  (lower is better)\n\n")
        f.write("Per-Class:\n")
        for cls, st in class_stats.items():
            f.write(f"  {cls:10s} Acc={st['accuracy']*100:.1f}%  "
                    f"Conf={st['mean_confidence']*100:.1f}%  "
                    f"Gap={st['gap']*100:+.1f}%\n")
        f.write("\nBin Detail (confidence → actual accuracy):\n")
        for b in bin_data:
            if b['count'] == 0: continue
            f.write(f"  [{b['lo']:.1f}-{b['hi']:.1f}]  "
                    f"n={b['count']:>4}  conf={b['avg_conf']:.3f}  "
                    f"acc={b['avg_acc']:.3f}  "
                    f"gap={b['avg_conf']-b['avg_acc']:+.3f}\n")

    # ── Reliability Diagram ────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), facecolor='white')

    # Reliability diagram
    ax = axes[0]
    valid_bins = [b for b in bin_data if b['count'] > 0]
    xs  = [b['avg_conf'] for b in valid_bins]
    ys  = [b['avg_acc']  for b in valid_bins]
    ns  = [b['count']    for b in valid_bins]
    ax.plot([0, 1], [0, 1], 'k--', lw=1.5, label='Perfect Calibration')
    ax.bar([b['lo'] for b in valid_bins], ys,
           width=[b['hi']-b['lo'] for b in valid_bins],
           align='edge', alpha=0.55, color='#2196F3', label='Actual Accuracy')
    ax.bar([b['lo'] for b in valid_bins],
           [b['avg_conf']-b['avg_acc'] for b in valid_bins],
           bottom=ys, width=[b['hi']-b['lo'] for b in valid_bins],
           align='edge', alpha=0.35, color='#FF5722', label='Gap (Over/Under)')
    ax.scatter(xs, ys, zorder=5, color='#1565C0', s=40)
    ax.set_xlim([0, 1]); ax.set_ylim([0, 1])
    ax.set_xlabel('Mean Predicted Confidence', fontsize=11)
    ax.set_ylabel('Fraction Correct', fontsize=11)
    ax.set_title(f'Reliability Diagram  |  ECE={ece:.4f}', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(linestyle='--', alpha=0.3)

    # Confidence histogram
    ax2 = axes[1]
    ax2.hist(confs[correct == 1], bins=20, alpha=0.7, color='#4CAF50', label='Correct')
    ax2.hist(confs[correct == 0], bins=20, alpha=0.7, color='#F44336', label='Wrong')
    ax2.axvline(confs.mean(), color='#333', linestyle='--', lw=1.5,
                label=f'Mean conf: {confs.mean()*100:.1f}%')
    ax2.set_xlabel('Predicted Confidence', fontsize=11)
    ax2.set_ylabel('Count', fontsize=11)
    ax2.set_title('Confidence Distribution (Correct vs Wrong)', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(linestyle='--', alpha=0.3)
    ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'reliability_diagram.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✅ Done! Outputs → {OUTPUT_DIR}")
    print(f"   ECE = {ece:.4f}  |  MCE = {mce:.4f}")

if __name__ == "__main__":
    run_calibration()
