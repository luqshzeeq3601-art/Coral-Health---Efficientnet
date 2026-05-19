
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input

IMG_SIZE = 224
MODEL_DIR = r"c:\Users\ZeeqRyz\OneDrive\Desktop\BASEPROJECT\02_V2_Improved_HighPerf"

def build_model():
    print("Building model architecture...")
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

model = build_model()
model_path = os.path.join(MODEL_DIR, "coral_model_seed42_finetuned.h5")
print(f"Loading weights from {model_path}...")
model.load_weights(model_path)
print("Weights loaded.")

print("\n--- Main Model Layers ---")
efficientnet_layer = None
for layer in model.layers:
    print(f"Name: {layer.name}, Type: {layer.__class__.__name__}")
    if 'efficientnet' in layer.name.lower():
        efficientnet_layer = layer

if efficientnet_layer:
    print(f"\n--- efficientnetb0 Sub-Layers (checking for top_conv) ---")
    try:
        # Try to find top_conv
        target = efficientnet_layer.get_layer('top_conv')
        print(f"[SUCCESS] Found 'top_conv' layer directly.")
    except Exception as e:
        print(f"[FAIL] Could not get 'top_conv' directly: {e}")
        
    print("\nListing last 10 layers of EfficientNet base model:")
    found_conv = False
    for layer in reversed(efficientnet_layer.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            print(f" -> Found Conv2D layer: {layer.name}")
            found_conv = True
            break
            
    if not found_conv:
        print("[FAIL] No Conv2D layer found in reversed search.")
else:
    print("\n[CRITICAL FAIL] Could not find layer with 'efficientnet' in name.")
