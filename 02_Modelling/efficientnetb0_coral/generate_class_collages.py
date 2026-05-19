import os
import sys
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral")
import train_v4_robust

def create_class_grids():
    print("Loading test dataset...")
    _, _, _, _, test_paths, test_labels = train_v4_robust.split_dataset(train_v4_robust.DATASET_PATH)
    X_test, y_test = train_v4_robust.prepare_set(test_paths, test_labels)

    print("\nLoading saved SWA models...")
    models = []
    for seed in train_v4_robust.SEEDS:
        swa_path = os.path.join(train_v4_robust.MODEL_DIR, f"efficientnetb0_v4robust_seed{seed}_swa.weights.h5")
        m = train_v4_robust.build_model(weights='imagenet')
        m.load_weights(swa_path, by_name=True, skip_mismatch=True)
        models.append(m)

    print(f"\nRunning TTA prediction on {len(X_test)} test images...")
    avg_preds = train_v4_robust.predict_with_tta(models, X_test)
    y_pred_classes = np.argmax(avg_preds, axis=1)
    y_true_classes = np.argmax(y_test, axis=1)
    
    gradcam_model = models[0]
    out_dir = train_v4_robust.OUTPUT_DIR
    
    # Process per class
    for cls_idx, cls_name in enumerate(train_v4_robust.CLASS_NAMES):
        print(f"\nProcessing all test images for True Class: {cls_name}")
        # Find all test indices belonging to this true class
        idxs = np.where(y_true_classes == cls_idx)[0]
        num_images = len(idxs)
        
        if num_images == 0:
            continue
            
        # Sort them by confidence (descending) so the highest confidence ones are at the top
        idxs = sorted(idxs, key=lambda i: avg_preds[i][cls_idx], reverse=True)
        
        cols = 5
        rows = math.ceil(num_images / cols)
        
        # We need extra space at the top for the color key notes
        fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows + 1))
        
        # Handle 1-dimensional edge case for exactly 1 row
        if rows == 1:
            axes = np.expand_dims(axes, axis=0) 
            
        fig.suptitle(f"Target Class: {cls_name} (All Test Images)\n"
                     f"Color Meaning: RED = High Model Attention | YELLOW = Medium Focus | BLUE = Low/No Attention", 
                     fontsize=24, fontweight='bold', color='#1f4e79', y=0.98)
                     
        # Flatten axes for easy iteration
        flat_axes = axes.flatten()
        
        for k, j in enumerate(idxs):
            img = X_test[j]
            true_lbl = y_true_classes[j]
            pred_lbl = y_pred_classes[j]
            conf = avg_preds[j][pred_lbl]
            
            img_array = np.expand_dims(img, axis=0)
            heatmap = train_v4_robust.make_gradcam_heatmap_smooth(img_array, gradcam_model,
                                                                  aug_smooth=True, eigen_smooth=True)
            
            ax = flat_axes[k]
            ax.imshow(img.astype(np.uint8))
            if heatmap.max() > 0:
                # Add the jet overlay
                ax.imshow(heatmap, cmap='jet', alpha=0.4)
                
            is_correct = "CORRECT" if true_lbl == pred_lbl else f"WRONG (Pred {train_v4_robust.CLASS_NAMES[pred_lbl]})"
            base_name = os.path.basename(test_paths[j]).split('.')[0]
            
            # Title: predicted class with confidence and correct/wrong marker
            title = f"{base_name}\nPred: {train_v4_robust.CLASS_NAMES[pred_lbl]} ({conf*100:.1f}%) | {is_correct}"
            ax.set_title(title, fontsize=12, pad=6, 
                         color='darkgreen' if true_lbl==pred_lbl else 'red', 
                         fontweight='bold' if true_lbl!=pred_lbl else 'normal')
                         
            ax.axis('off')
            
            if (k+1) % 10 == 0:
                print(f"  Processed {k+1}/{num_images} images")
                
        # Turn off empty subplots if there are leftover axes in the grid
        for k in range(num_images, len(flat_axes)):
            flat_axes[k].axis('off')
            
        plt.tight_layout()
        plt.subplots_adjust(top=0.94) # Leave room for super title
        
        save_path = os.path.join(out_dir, f'gradcam_all_{cls_name}.png')
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved {save_path}")

if __name__ == "__main__":
    create_class_grids()
