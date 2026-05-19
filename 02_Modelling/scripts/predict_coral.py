import os
import sys
import io
import argparse
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input
import matplotlib.pyplot as plt
import cv2

# Set stdout to use utf-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==========================================
# 1. SETUP & CONFIG
# ==========================================
IMG_SIZE = 224
CLASS_NAMES = ['Healthy', 'Bleached', 'Dead']
SEEDS = [42, 43, 44]

# Architecture (Must match training)
def build_model():
    base_model = EfficientNetB0(include_top=False, weights='imagenet', input_shape=(IMG_SIZE, IMG_SIZE, 3))
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

# Grad-CAM Class with Smoothing Support
class GradCAM:
    def __init__(self, model, layer_name='top_conv'):
        self.model = model
        self.target_layer = None
        
        # Find EfficientNet base
        self.efficientnet = None
        for layer in model.layers:
            if 'efficientnet' in layer.name.lower():
                self.efficientnet = layer
                break
        
        search_model = self.efficientnet if self.efficientnet else model
        try:
            self.target_layer = search_model.get_layer(layer_name)
        except:
            for layer in search_model.layers[::-1]:
                if 'conv' in layer.name.lower():
                    self.target_layer = layer
                    break
        
        if self.efficientnet:
            self.internal_model = tf.keras.models.Model(
                inputs=self.efficientnet.input,
                outputs=[self.target_layer.output, self.efficientnet.output]
            )
            self.is_nested = True
        else:
            self.internal_model = tf.keras.models.Model(
                inputs=model.input,
                outputs=[self.target_layer.output, model.output]
            )
            self.is_nested = False

    def compute_heatmap(self, image, class_idx=None, eigen_smooth=False):
        """Compute Grad-CAM heatmap with optional eigen_smooth (PCA denoising).
        
        Args:
            image: Input image (no batch dimension).
            class_idx: Target class to explain. If None, uses predicted class.
            eigen_smooth: If True, use first principal component of
                          activations*weights for noise reduction.
        """
        img_array = np.expand_dims(image, axis=0)
        preds = self.model.predict(img_array, verbose=0)[0]
        if class_idx is None:
            class_idx = np.argmax(preds)
            
        if self.is_nested:
            with tf.GradientTape() as tape:
                conv_outs, model_outs = self.internal_model(img_array)
                if model_outs.shape[-1] > class_idx:
                    loss = model_outs[:, class_idx]
                else:
                    loss = tf.reduce_mean(model_outs)
            grads = tape.gradient(loss, conv_outs)
        else:
            with tf.GradientTape() as tape:
                conv_outs, model_outs = self.internal_model(img_array)
                loss = model_outs[:, class_idx]
            grads = tape.gradient(loss, conv_outs)

        if eigen_smooth:
            # ---- Eigen Smooth: PCA on activations * weights ----
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2)).numpy()
            conv_out = conv_outs[0].numpy()  # (H, W, C)
            weighted_activations = conv_out * pooled_grads[np.newaxis, np.newaxis, :]
            h, w, c = weighted_activations.shape
            reshaped = weighted_activations.reshape(h * w, c)
            U, S, Vt = np.linalg.svd(reshaped, full_matrices=False)
            heatmap = U[:, 0] * S[0]
            heatmap = heatmap.reshape(h, w)
            heatmap = np.maximum(heatmap, 0)
        else:
            # ---- Standard Grad-CAM ----
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            conv_out = conv_outs[0]
            heatmap = conv_out @ pooled_grads[..., tf.newaxis]
            heatmap = tf.squeeze(heatmap)
            heatmap = tf.nn.relu(heatmap)
            heatmap = heatmap.numpy()

        heatmap = heatmap / (np.max(heatmap) + 1e-8)
        heatmap = cv2.resize(heatmap, (IMG_SIZE, IMG_SIZE))
        return heatmap

    def compute_heatmap_smooth(self, image, class_idx=None,
                                aug_smooth=False, eigen_smooth=False):
        """Grad-CAM with optional aug_smooth (TTA) and eigen_smooth (PCA).
        
        Args:
            image: Input image (no batch dimension).
            class_idx: Target class to explain. If None, uses predicted class.
            aug_smooth: If True, average CAMs over 6 augmented views
                        (3 brightness × 2 flip states). 6× slower.
            eigen_smooth: If True, use PCA denoising on each CAM.
        """
        if not aug_smooth:
            return self.compute_heatmap(image, class_idx, eigen_smooth=eigen_smooth)

        # ---- Aug Smooth: TTA with brightness jitter + horizontal flips ----
        heatmaps = []
        brightness_factors = [1.0, 1.1, 0.9]

        for flip in [False, True]:
            for brightness in brightness_factors:
                augmented = image.copy() * brightness
                augmented = np.clip(augmented, 0, 255)

                if flip:
                    augmented = np.flip(augmented, axis=1)  # Horizontal flip (W axis)

                hm = self.compute_heatmap(augmented, class_idx, eigen_smooth=eigen_smooth)

                if flip:
                    hm = np.flip(hm, axis=1)  # Un-flip heatmap to re-align

                heatmaps.append(hm)

        avg_heatmap = np.mean(heatmaps, axis=0)
        if np.max(avg_heatmap) > 0:
            avg_heatmap = avg_heatmap / np.max(avg_heatmap)
        return avg_heatmap

    def overlay_heatmap(self, image, heatmap, alpha=0.4):
        heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap), cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        if image.max() <= 1.0:
            image_uint8 = np.uint8(255 * image)
        else:
            image_uint8 = np.uint8(image)
        return cv2.addWeighted(image_uint8, 1 - alpha, heatmap_colored, alpha, 0)

# ==========================================
# 2. MAIN LOGIC
# ==========================================
def predict_image(image_path):
    print(f"\n🔍 Analyzing Image: {image_path}")
    
    if not os.path.exists(image_path):
        print("❌ Error: Image file not found.")
        return

    # Load & Preprocess
    try:
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        original_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img_array = original_img.astype('float32')
        img_batch = np.expand_dims(img_array, axis=0)
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return

    # Ensemble Prediction
    print("🚀 Loading Ensemble Models...")
    ensemble_probs = np.zeros(3)
    models = []
    
    for seed in SEEDS:
        # Prefer Fine-Tuned Model
        model_name = f"coral_model_seed{seed}_finetuned.h5"
        if not os.path.exists(model_name):
            model_name = f"coral_model_seed{seed}_best.h5"
            
        try:
            model = build_model()
            model.load_weights(model_name)
            # Compile just to silence warnings if needed
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            
            probs = model.predict(img_batch, verbose=0)[0]
            ensemble_probs += probs
            models.append(model)
            
            pred_idx = np.argmax(probs)
            conf = probs[pred_idx] * 100
            print(f"   Model (Seed {seed}): {CLASS_NAMES[pred_idx]} ({conf:.1f}%)")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load {model_name}: {e}")

    if not models:
        print("❌ No models loaded. Exiting.")
        return

    # Average
    avg_probs = ensemble_probs / len(models)
    final_idx = np.argmax(avg_probs)
    final_conf = avg_probs[final_idx] * 100
    final_label = CLASS_NAMES[final_idx]
    
    print("\n" + "="*40)
    print(f"🧠 ENSEMBLE PREDICTION: {final_label.upper()}")
    print(f"💪 Confidence: {final_conf:.2f}%")
    print("="*40)
    
    # Probabilities breakdown
    print("\n📊 Detailed Probabilities:")
    for i, name in enumerate(CLASS_NAMES):
        print(f"   - {name}: {avg_probs[i]*100:.2f}%")

    # Grad-CAM Visualization (with smoothing)
    print("\n🖼️ Generating Visualization (aug+eigen smooth)...")
    try:
        # Use first model for Grad-CAM
        grad_cam = GradCAM(models[0], layer_name='top_conv')
        heatmap = grad_cam.compute_heatmap_smooth(original_img, class_idx=final_idx,
                                                   aug_smooth=True, eigen_smooth=True)
        overlay = grad_cam.overlay_heatmap(original_img, heatmap)
        
        # Plot
        plt.figure(figsize=(10, 4))
        
        plt.subplot(1, 3, 1)
        plt.imshow(original_img.astype('uint8'))
        plt.title("Original Image")
        plt.axis('off')
        
        plt.subplot(1, 3, 2)
        plt.imshow(heatmap, cmap='jet')
        plt.title("Grad-CAM (Smoothed)")
        plt.axis('off')
        
        plt.subplot(1, 3, 3)
        plt.imshow(overlay)
        plt.title(f"Pred: {final_label} ({final_conf:.1f}%)")
        plt.axis('off')
        
        save_path = "prediction_result.png"
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✅ Saved visualization to: {save_path}")
        
    except Exception as e:
        print(f"⚠️ Error generating Grad-CAM: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict Coral Health from Image")
    parser.add_argument("--image", type=str, required=True, help="Path to the image file")
    args = parser.parse_args()
    
    predict_image(args.image)
