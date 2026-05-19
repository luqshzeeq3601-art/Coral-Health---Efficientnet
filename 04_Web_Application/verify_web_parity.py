import os
import sys
import cv2
import pandas as pd
import numpy as np
from typing import List

sys.path.append(r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\04_Web_Application')
import app

# Force models to load
app.load_models()
client = app.app.test_client()

CSV_PATH = r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation\02_Deployment_Phase\robust_v4_audit_results.csv'
DATASET_PATH = r'c:\Users\ZeeqRyz\Desktop\BASEPROJECT\Dataset'

df = pd.read_csv(CSV_PATH)
CLASS_NAMES = ['Healthy', 'Bleached', 'Dead']
TTA_SCALES = [224, 256]
IMG_SIZE = 224

discrepancies: List[dict] = []
total_checked = 0

for index, row in df.iterrows():
    filename = str(row['Filename'])
    true_label = str(row['True Label'])
    audit_pred = str(row['Predicted Label'])
    audit_conf = float(row['Confidence (%)'])
    
    img_path = os.path.join(DATASET_PATH, true_label, filename)
    if not os.path.exists(img_path):
        print(f"Warning: Image not found {img_path}")
        continue
    
    with open(img_path, 'rb') as f:
        response = client.post('/api/predict', data={'file': (f, filename)})
        
    if response.status_code != 200:
        print(f"Error in API for {filename}: {response.get_data(as_text=True)}")
        continue

    res_json = response.get_json()
    if not res_json or 'confidence' not in res_json:
        print(f"Error in API response for {filename}: {res_json}")
        continue
        
    final_conf = float(res_json['confidence'])
    
    if abs(final_conf - audit_conf) > 0.05:
        discrepancies.append({
            'filename': filename,
            'audit_conf': audit_conf,
            'web_conf': final_conf,
            'diff': abs(final_conf - audit_conf)
        })
    total_checked = total_checked + 1

print(f"\nChecked {total_checked} images.")
if not discrepancies:
    print("SUCCESS: Web app logic exactly matches audit logic for all dataset images!")
else:
    print(f"FAILED: Found {len(discrepancies)} discrepancies.")
    shown_discrepancies = discrepancies[0:10]
    for d in shown_discrepancies:
         print(f"  {d['filename']}: Web {d['web_conf']:.2f}% vs Audit {d['audit_conf']:.2f}% (Diff: {d['diff']:.2f}%)")
