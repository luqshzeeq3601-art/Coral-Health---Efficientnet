import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral"
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
JSON_PATH = os.path.join(OUTPUT_DIR, 'training_history_ensemble.json')

def plot_gap():
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
    
    avg_train_acc = np.array(data['avg_train_acc'])
    avg_val_acc = np.array(data['avg_val_acc'])
    avg_train_loss = np.array(data['avg_train_loss'])
    avg_val_loss = np.array(data['avg_val_loss'])

    # Calculations as requested
    acc_gap = avg_train_acc - avg_val_acc
    loss_gap = avg_val_loss - avg_train_loss

    epochs_range = range(1, len(avg_train_acc) + 1)
    
    plt.figure(figsize=(10, 6), facecolor='white')
    
    # Plotting lines
    plt.plot(epochs_range, acc_gap, label='Accuracy Gap (Train - Val)', color='tab:blue', linewidth=2.5)
    plt.plot(epochs_range, loss_gap, label='Loss Gap (Val - Train)', color='tab:red', linewidth=2.5)
    
    # Horizontal zero point reference line
    plt.axhline(0, color='black', linestyle='--', linewidth=1.5, label='Zero Reference')
    
    plt.title('Train-Validation Gap Graph', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Gap Value', fontsize=12)
    plt.xticks([1, 5, 10, 15, 20, 25, 30])
    plt.tick_params(labelsize=11)
    
    plt.legend(loc='best', frameon=True, facecolor='white', edgecolor='gray', fontsize=11)
    plt.grid(True, linestyle='--', color='#E0E0E0', alpha=0.5, linewidth=0.7)
    
    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'train_validation_gap.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print("Gap graph saved to:", output_path)

if __name__ == "__main__":
    plot_gap()
