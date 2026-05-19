
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0

IMG_SIZE = 224

print("Building EfficientNetB0...")
base_model = EfficientNetB0(include_top=False, weights=None, input_shape=(IMG_SIZE, IMG_SIZE, 3))

print("\nFinding layers after 'top_conv':")
found = False
layers_after = []
for layer in base_model.layers:
    if layer.name == 'top_conv':
        found = True
        continue
    if found:
        print(f" - {layer.name} ({layer.__class__.__name__})")
        layers_after.append(layer)

print(f"\nTotal layers after top_conv: {len(layers_after)}")
