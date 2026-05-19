"""Replicate exact load pattern from replot_evaluation.py"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import GlobalAveragePooling2D, Dropout, Dense, Input

IMG_SIZE = 224
MODEL_DIR = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral\models"

def build_model():
    base_model = EfficientNetB0(include_top=False, weights="imagenet", input_shape=(IMG_SIZE, IMG_SIZE, 3))
    base_model.trainable = True
    for layer in base_model.layers[:-100]:
        layer.trainable = False
    return Sequential([Input(shape=(IMG_SIZE, IMG_SIZE, 3)), base_model,
                       GlobalAveragePooling2D(), Dropout(0.4),
                       Dense(3, activation="softmax", kernel_regularizer=tf.keras.regularizers.l2(0.0002))])

# Test all file variants for seed 42 and 43
for seed in [42, 43]:
    for variant in ['swa.h5', 'swa.weights.h5']:
        p = os.path.join(MODEL_DIR, f"efficientnetb0_v4robust_seed{seed}_{variant}")
        if not os.path.exists(p): 
            print(f"SKIP| {p} not found")
            continue
        try:
            m = build_model()
            m.load_weights(p)
            print(f"OK  | seed={seed} file={variant}")
        except Exception as e:
            print(f"FAIL| seed={seed} file={variant} => {str(e)[:100]}")
