# GradCAM Smoothing Analysis — Improving Your Coral Health Visualizations

## Current State of Your GradCAM

Your project has a **custom TensorFlow/Keras Grad-CAM implementation** (not the `pytorch-grad-cam` library). The implementation is found across three files:

| File | Usage |
|------|-------|
| [train_v4_robust.py](file:///c:/Users/ZeeqRyz/Desktop/BASEPROJECT/02_Modelling/efficientnetb0_coral/train_v4_robust.py#L236-L299) | `make_gradcam_heatmap()` — generates post-training evaluation CAMs |
| [app.py](file:///c:/Users/ZeeqRyz/Desktop/BASEPROJECT/04_Web_Application/app.py#L25-L120) | `compute_gradcam()` — generates live inference CAMs for the web app |
| [predict_coral.py](file:///c:/Users/ZeeqRyz/Desktop/BASEPROJECT/02_Modelling/scripts/predict_coral.py#L40-L111) | `GradCAM` class — standalone prediction script |

### What Your Current Implementation Does

```python
# Core algorithm (same in all 3 files):
pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))   # Global average pooling of gradients
heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]  # Weighted combination
heatmap = tf.nn.relu(heatmap)                           # Keep only positive activations
heatmap = heatmap / np.max(heatmap)                     # Normalize to [0, 1]
```

This is **vanilla Grad-CAM** — no smoothing applied. Looking at your current output:

![Current GradCAM outputs](file:///c:/Users/ZeeqRyz/Desktop/BASEPROJECT/03_Model_Evaluation/01_EfficientNetB0_Evaluation/gradcam_outputs.png)

> [!WARNING]
> The heatmaps show noisy, diffuse activations that spread across the entire image rather than focusing tightly on the coral structures. This makes it hard to explain *precisely* what the model is looking at.

---

## How `pytorch-grad-cam` Smoothing Works

The [pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam) library offers two smoothing techniques as simple flags. Here's what they do under the hood:

### 1. `aug_smooth=True` — Test-Time Augmentation Smoothing

**Concept:** Instead of computing the CAM on a single image, compute it on **6 augmented versions** and average the results.

**Augmentations applied:**
- Original image × brightness factors `[1.0, 1.1, 0.9]` → 3 versions
- Horizontally flipped image × brightness factors `[1.0, 1.1, 0.9]` → 3 versions
- **Total: 6 forward passes → 6 CAMs → averaged**

```
Original × 1.0  → CAM₁ ─┐
Original × 1.1  → CAM₂  │
Original × 0.9  → CAM₃  ├─ Average → Smooth CAM
Flipped  × 1.0  → CAM₄  │
Flipped  × 1.1  → CAM₅  │
Flipped  × 0.9  → CAM₆ ─┘
```

**Effect:** Better centers the CAM around objects. The augmentations cause slight spatial shifts in where activations fire, and averaging these removes spurious edge activations while reinforcing consistent central regions.

**Trade-off:** 6× slower inference.

---

### 2. `eigen_smooth=True` — PCA-Based Noise Reduction

**Concept:** Instead of using the standard weighted combination of activation channels, extract only the **first principal component** of the `activations × weights` matrix.

**Standard Grad-CAM:**
```python
# Each channel weighted equally by its gradient importance
heatmap = Σ(weight_i × activation_i)  
```

**Eigen-smooth Grad-CAM:**
```python
# Reshape activations*weights into 2D matrix: (H×W) × C
# Compute SVD/PCA → take only first principal component
# Reshape back to H × W
heatmap = first_principal_component(activations * weights)
```

**Effect:** Dramatically reduces noise by keeping only the dominant spatial pattern from the activation maps. Minor noisy channels that disagree with the main signal are filtered out.

**Trade-off:** Minimal speed impact (one SVD computation), occasionally removes fine-grained detail.

---

### 3. `aug_smooth=True` + `eigen_smooth=True` — Combined

Applies both: TTA augmentation + PCA denoising. This gives the cleanest results.

---

## How to Implement This in Your TensorFlow Project

Since you're using **TensorFlow/Keras** (not PyTorch), you can't use `pytorch-grad-cam` directly. But the concepts are straightforward to implement. Here's what to add to your code:

### Approach A: Implement `aug_smooth` (TTA Smoothing)

```python
def make_gradcam_heatmap_aug_smooth(img_array, model, layer_name='top_conv'):
    """Grad-CAM with test-time augmentation smoothing (6x forward passes)."""
    heatmaps = []
    brightness_factors = [1.0, 1.1, 0.9]
    
    for flip in [False, True]:
        for brightness in brightness_factors:
            # Apply augmentation
            augmented = img_array.copy()
            augmented = augmented * brightness
            augmented = np.clip(augmented, 0, 255)
            
            if flip:
                augmented = np.flip(augmented, axis=2)  # Horizontal flip (axis=2 for batch)
            
            # Compute standard Grad-CAM
            hm = make_gradcam_heatmap(augmented, model, layer_name)
            
            if flip:
                hm = np.flip(hm, axis=1)  # Un-flip the heatmap to align
            
            heatmaps.append(hm)
    
    # Average all augmented heatmaps
    avg_heatmap = np.mean(heatmaps, axis=0)
    if np.max(avg_heatmap) > 0:
        avg_heatmap = avg_heatmap / np.max(avg_heatmap)
    
    return avg_heatmap
```

### Approach B: Implement `eigen_smooth` (PCA Denoising)

```python
def make_gradcam_heatmap_eigen_smooth(img_array, model, layer_name='top_conv'):
    """Grad-CAM with eigen (PCA) smoothing for noise reduction."""
    # ... (same setup as your existing make_gradcam_heatmap to get conv_outputs and grads)
    
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
    
    # --- EIGEN SMOOTH: PCA on activations * weights ---
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_out = conv_outputs[0].numpy()  # Shape: (H, W, C)
    weights = pooled_grads.numpy()      # Shape: (C,)
    
    # Element-wise multiply: each channel weighted by its gradient importance
    weighted_activations = conv_out * weights[np.newaxis, np.newaxis, :]  # (H, W, C)
    
    # Reshape to 2D: (H*W, C)
    h, w, c = weighted_activations.shape
    reshaped = weighted_activations.reshape(h * w, c)
    
    # SVD to get first principal component
    U, S, Vt = np.linalg.svd(reshaped, full_matrices=False)
    heatmap = U[:, 0] * S[0]  # First principal component
    heatmap = heatmap.reshape(h, w)
    
    # ReLU + normalize
    heatmap = np.maximum(heatmap, 0)
    heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
    
    return heatmap
```

### Approach C: Combined (Both)

```python
def make_gradcam_heatmap_smooth(img_array, model, layer_name='top_conv',
                                 aug_smooth=False, eigen_smooth=False):
    """Grad-CAM with optional aug_smooth and/or eigen_smooth."""
    
    # Choose base function
    base_fn = make_gradcam_heatmap_eigen_smooth if eigen_smooth else make_gradcam_heatmap
    
    if aug_smooth:
        heatmaps = []
        brightness_factors = [1.0, 1.1, 0.9]
        
        for flip in [False, True]:
            for brightness in brightness_factors:
                augmented = img_array.copy() * brightness
                augmented = np.clip(augmented, 0, 255)
                
                if flip:
                    augmented = np.flip(augmented, axis=2)
                
                hm = base_fn(augmented, model, layer_name)
                
                if flip:
                    hm = np.flip(hm, axis=1)
                
                heatmaps.append(hm)
        
        avg_heatmap = np.mean(heatmaps, axis=0)
        if np.max(avg_heatmap) > 0:
            avg_heatmap = avg_heatmap / np.max(avg_heatmap)
        return avg_heatmap
    else:
        return base_fn(img_array, model, layer_name)
```

---

## Comparison: What to Expect

| Method | Noise Level | Object Focus | Speed | Best For |
|--------|-------------|-------------|-------|----------|
| **Vanilla** (current) | High | Diffuse | 1× | Quick baseline |
| **`aug_smooth`** | Medium | Well-centered | 6× | Better localization |
| **`eigen_smooth`** | Low | Clean boundaries | ~1× | Noise reduction |
| **Both combined** | Lowest | Best | 6× | Publication-quality |

Based on your current coral images where the heatmaps spread across the entire image, I'd recommend:

> [!IMPORTANT]
> **Start with `eigen_smooth`** — it gives the biggest visual improvement at virtually no speed cost. Then optionally add `aug_smooth` for your training evaluation outputs where speed doesn't matter.
> 
> For the **web app** (real-time inference), use only `eigen_smooth` since `aug_smooth` adds 6× latency.

---

## Where to Apply Changes

| Location | Recommendation |
|----------|---------------|
| `train_v4_robust.py` (training evaluation) | Use **both** `aug_smooth + eigen_smooth` — speed doesn't matter for one-time evaluation |
| `app.py` (web app live predictions) | Use **eigen_smooth only** — keeps response time fast |
| `predict_coral.py` (CLI tool) | Use **both** — single-image tool, speed isn't critical |

## Decision Needed

> [!IMPORTANT]
> Do you want me to implement these smoothing improvements into your codebase? I can update all three files with the smoothing functions and add `aug_smooth` + `eigen_smooth` options.
