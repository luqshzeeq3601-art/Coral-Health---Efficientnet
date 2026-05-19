import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral"
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
JSON_PATH = os.path.join(OUTPUT_DIR, 'training_history_ensemble.json')

def replot():
    with open(JSON_PATH, 'r') as f:
        data = json.load(f)
    
    avg_train_acc = data['avg_train_acc']
    avg_val_acc = data['avg_val_acc']
    avg_train_loss = data['avg_train_loss']
    avg_val_loss = data['avg_val_loss']

    plt.figure(figsize=(14, 5), facecolor='white')
    epochs_range = range(1, len(avg_train_acc) + 1)
    
    train_color = 'tab:blue'
    val_color = 'tab:red'
    
    # Accuracy Subplot
    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(epochs_range, avg_train_acc, label='Training Accuracy', color=train_color, linewidth=2.5)
    ax1.plot(epochs_range, avg_val_acc, label='Validation Accuracy', color=val_color, linewidth=2.5)
    ax1.set_title('Training and Validation Accuracy', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.set_ylim([0.60, 1.00])
    ax1.set_xticks([1, 5, 10, 15, 20, 25, 30])
    ax1.tick_params(labelsize=11)
    ax1.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='gray', fontsize=11)
    ax1.grid(True, linestyle='--', color='#E0E0E0', alpha=0.5, linewidth=0.7)
    
    # Loss Subplot
    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(epochs_range, avg_train_loss, label='Training Loss', color=train_color, linewidth=2.5)
    ax2.plot(epochs_range, avg_val_loss, label='Validation Loss', color=val_color, linewidth=2.5)
    ax2.set_title('Training and Validation Loss', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Loss', fontsize=12)
    ax2.set_ylim([0.25, 0.95])
    ax2.set_xticks([1, 5, 10, 15, 20, 25, 30])
    ax2.tick_params(labelsize=11)
    ax2.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='gray', fontsize=11)
    ax2.grid(True, linestyle='--', color='#E0E0E0', alpha=0.5, linewidth=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'training_history_ensemble.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("Regenerated training_history_ensemble.png with clearer ticks")

if __name__ == "__main__":
    replot()
