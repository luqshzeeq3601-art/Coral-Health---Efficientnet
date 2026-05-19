import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import os

results_path = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation/Validation_Data\02_Deployment_Phase\robust_v4_audit_results.csv"
output_dir = os.path.dirname(results_path)

if os.path.exists(results_path):
    df = pd.read_csv(results_path)
    cm = confusion_matrix(df['True Label'], df['Predicted Label'], labels=['Healthy', 'Bleached', 'Dead'])
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Healthy', 'Bleached', 'Dead'],
                yticklabels=['Healthy', 'Bleached', 'Dead'])
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('V4 Robust Expert Ensemble - Confusion Matrix')
    
    cm_path = os.path.join(output_dir, "robust_v4_confusion_matrix.png")
    plt.savefig(cm_path)
    print(f"Saved confusion matrix to {cm_path}")
