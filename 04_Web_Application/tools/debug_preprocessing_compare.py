import os
import numpy as np
from PIL import Image

import app as webapp

SAMPLE_IMAGE = r"c:\Users\ZeeqRyz\OneDrive\Desktop\BASEPROJECT\03_Model_Evaluation\prediction_result_test_healthy.png"


def fmt_probs(probs):
    return {name: round(float(probs[i]) * 100, 3) for i, name in enumerate(webapp.CLASS_NAMES)}


def run_debug(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Sample image not found: {image_path}")

    if len(webapp.MODELS) == 0:
        webapp.load_models()

    image = Image.open(image_path).convert("RGB").resize((webapp.IMG_SIZE, webapp.IMG_SIZE))
    arr = np.array(image)

    inp_old = np.expand_dims(arr.astype("float32") / 255.0, axis=0)
    inp_new = np.expand_dims(arr.astype("float32"), axis=0)

    print("=" * 72)
    print("Preprocessing side-by-side debug (per-model)")
    print(f"Sample image: {image_path}")
    print("Old preprocessing  : float32 / 255.0")
    print("Current preprocessing: float32 0-255")
    print("=" * 72)

    old_preds = []
    new_preds = []

    for i, model in enumerate(webapp.MODELS):
        p_old = model.predict(inp_old, verbose=0)[0]
        p_new = model.predict(inp_new, verbose=0)[0]
        old_preds.append(p_old)
        new_preds.append(p_new)

        old_idx = int(np.argmax(p_old))
        new_idx = int(np.argmax(p_new))

        print(f"\nModel {i+1} (seed {webapp.SEEDS[i]}):")
        print(
            f"  OLD  -> {webapp.CLASS_NAMES[old_idx]} | conf={p_old[old_idx]*100:.3f}% | scores={fmt_probs(p_old)}"
        )
        print(
            f"  NEW  -> {webapp.CLASS_NAMES[new_idx]} | conf={p_new[new_idx]*100:.3f}% | scores={fmt_probs(p_new)}"
        )

    ens_old = np.mean(old_preds, axis=0)
    ens_new = np.mean(new_preds, axis=0)

    idx_old = int(np.argmax(ens_old))
    idx_new = int(np.argmax(ens_new))

    print("\n" + "-" * 72)
    print(
        f"ENSEMBLE OLD -> {webapp.CLASS_NAMES[idx_old]} | conf={ens_old[idx_old]*100:.3f}% | scores={fmt_probs(ens_old)}"
    )
    print(
        f"ENSEMBLE NEW -> {webapp.CLASS_NAMES[idx_new]} | conf={ens_new[idx_new]*100:.3f}% | scores={fmt_probs(ens_new)}"
    )
    print("-" * 72)


if __name__ == "__main__":
    run_debug(SAMPLE_IMAGE)
