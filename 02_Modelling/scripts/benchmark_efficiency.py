import time
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
import os

def benchmark_efficiency():
    print("Starting Speed and Efficiency Analysis...")
    
    # 1. Model Statistics
    print("\n--- 1. Model Architecture Stats ---")
    model = EfficientNetB0(weights=None, classes=3)
    num_params = model.count_params()
    print(f"Model: EfficientNet-B0")
    print(f"Parameters: {num_params:,}")
    # Size on disk estimation
    size_mb = (num_params * 4) / (1024 * 1024) 
    print(f"Estimated Size (FP32): {size_mb:.2f} MB")

    # 2. Inference Speed Benchmark
    print("\n--- 2. Inference Speed Benchmark ---")
    img_size = 224
    dummy_input = np.random.rand(1, img_size, img_size, 3).astype('float32')
    
    # Warm-up
    _ = model.predict(dummy_input, verbose=0)
    
    # Single Prediction
    start = time.time()
    for _ in range(10):
        _ = model.predict(dummy_input, verbose=0)
    end = time.time()
    avg_inf_single = (end - start) / 10 * 1000
    print(f"Single Forward Pass (Avg): {avg_inf_single:.2f} ms")
    
    # Ensemble (x3)
    print(f"Ensemble (3 models) Estimate: {avg_inf_single * 3:.2f} ms")
    
    # TTA (10-crop batch)
    dummy_tta = np.random.rand(10, img_size, img_size, 3).astype('float32')
    start = time.time()
    for _ in range(5):
        _ = model.predict(dummy_tta, verbose=0)
    end = time.time()
    avg_inf_tta = (end - start) / 5 * 1000
    print(f"10-Crop TTA Batch (Avg): {avg_inf_tta:.2f} ms")
    
    # Total Assessment Pipeline (3 models * 10 crops)
    pipeline_total = avg_inf_tta * 3
    print(f"Total Prediction Pipeline (Ensemble + TTA): {pipeline_total:.2f} ms")

    # 3. Efficiency Insights
    print("\n--- 3. Efficiency Insights ---")
    print(f"Throughput (Single): {1000/avg_inf_single:.1f} FPS")
    print(f"Throughput (TTA Ensemble): {1000/pipeline_total:.2f} Images/Sec")
    
    print("\nSummary:")
    print("- EfficientNet-B0 provides high accuracy with minimal parameters compared to ResNet/VGG.")
    print("- Batching TTA crops reduces overhead compared to sequential processing.")
    print("- The bottleneck is the Ensemble size + TTA count, which prioritizes accuracy over raw speed.")

if __name__ == "__main__":
    benchmark_efficiency()
