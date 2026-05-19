import os
import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# MODEL EFFICIENCY DATA
# ==========================================
# Canonical accuracy from the benchmark-verified notebook/report setup
# Param counts from get_params.py / classification_models
models = {
    'EfficientNetB0': {'accuracy': 98.11, 'params': 4053414},
    'DenseNet121':    {'accuracy': 92.45, 'params': 7040579},
    'ResNet18':       {'accuracy': 96.86, 'params': 11188428}
}

# ==========================================
# PLOTTING
# ==========================================
def generate_efficiency_plot():
    names = list(models.keys())
    accuracies = [models[m]['accuracy'] for m in names]
    params_m = [models[m]['params'] / 1e6 for m in names]  # Convert to Millions

    plt.figure(figsize=(10, 7), facecolor='white')
    
    # Define colors and markers
    colors = ['#1CCC8C', '#F5A623', '#5B5BEB']  # Green, Orange, Purple
    markers = ['o', 's', '^']                  # Circle, Square, Triangle
    
    for i, name in enumerate(names):
        plt.scatter(params_m[i], accuracies[i], 
                    s=200, c=colors[i], marker=markers[i], 
                    label=f"{name} ({accuracies[i]}%)", 
                    edgecolors='black', alpha=0.8, zorder=5)
        
        # Add labels for each point
        plt.annotate(name, 
                     (params_m[i], accuracies[i]),
                     textcoords="offset points", 
                     xytext=(0, 10), 
                     ha='center', fontsize=11, fontweight='bold')

    # Formatting
    plt.title('V4 Robust Model Efficiency: Accuracy vs. Parameters', fontsize=15, fontweight='bold', pad=20)
    plt.xlabel('Number of Parameters (Millions)', fontsize=12)
    plt.ylabel('Ensemble Test Accuracy (%)', fontsize=12)
    
    plt.grid(True, linestyle='--', alpha=0.6, zorder=1)
    plt.ylim(min(accuracies) - 2, 100)
    plt.xlim(0, max(params_m) + 2)
    
    plt.legend(loc='lower right', frameon=True, facecolor='white', edgecolor='gray', fontsize=10)
    
    # Save Output
    save_path = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\02_Modelling\efficientnetb0_coral\model_efficiency.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Efficiency plot saved to: {save_path}")

if __name__ == "__main__":
    generate_efficiency_plot()
