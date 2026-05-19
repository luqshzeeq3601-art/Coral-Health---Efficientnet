
import os

METRICS_DIR = r"c:\Users\ZeeqRyz\OneDrive\Desktop\BASEPROJECT\02_V2_Improved_HighPerf\03_Model_Evaluation\02_Deployment_Phase"

print(f"Checking METRICS_DIR: {METRICS_DIR}")
if os.path.exists(METRICS_DIR):
    print("  [OK] Directory exists")
    print("  Contents:", os.listdir(METRICS_DIR))
else:
    print("  [FAIL] Directory does not exist")

files_to_check = [
    'final_classification_report.csv',
    'final_confusion_matrix.png',
    'final_summary.txt'
]

for f in files_to_check:
    path = os.path.join(METRICS_DIR, f)
    if os.path.exists(path):
        print(f"  [OK] Found {f}")
        # Try reading summary
        if 'summary' in f:
            try:
                with open(path, 'r') as file:
                    content = file.read()
                    print(f"    Content length: {len(content)}")
                    # Test Regex
                    import re
                    acc = re.search(r'Accuracy:\s*([\d\.]+)%', content)
                    err = re.search(r'Total Errors:\s*(\d+)', content)
                    print(f"    Parsed Accuracy: {acc.group(1) if acc else 'None'}")
                    print(f"    Parsed Errors: {err.group(1) if err else 'None'}")
            except Exception as e:
                print(f"    [FAIL] Error reading: {e}")
    else:
        print(f"  [FAIL] Missing {f}")
