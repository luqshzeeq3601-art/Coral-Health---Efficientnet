"""
=============================================================
  RUN ALL ADVANCED TESTS
  Coral Health - EfficientNetB0 V4 Robust
=============================================================
  Master launcher. Runs all three tests in sequence:
    1. Stratified K-Fold Cross-Validation
    2. Robustness Testing
    3. Confidence Calibration Analysis
=============================================================
"""
import os, sys, io, subprocess, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON   = sys.executable

SCRIPTS = [
    ("01_stratified_kfold",    "run_kfold.py",        "Stratified K-Fold Cross-Validation"),
    ("02_robustness_testing",  "run_robustness.py",   "Robustness Testing"),
    ("03_calibration_analysis","run_calibration.py",  "Confidence Calibration Analysis"),
]

def run_test(folder, script, name):
    script_path = os.path.join(BASE_DIR, folder, script)
    if not os.path.exists(script_path):
        print(f"\n⚠️  Script not found: {script_path}")
        return False
    print(f"\n{'='*65}")
    print(f"\n  >>> Running: {name}")
    print(f"{'='*65}")
    t0  = time.time()
    ret = subprocess.run([PYTHON, script_path],
                         cwd=os.path.join(BASE_DIR, folder))
    elapsed = time.time() - t0
    if ret.returncode == 0:
        print(f"\n  ✅  {name} completed in {elapsed/60:.1f} min")
        return True
    else:
        print(f"\n  ❌  {name} FAILED (code {ret.returncode})")
        return False

if __name__ == "__main__":
    print("=" * 65)
    print("  ADVANCED MODEL TESTING SUITE")
    print("  EfficientNetB0 V4 Robust — Coral Health Classification")
    print("=" * 65)
    t_total = time.time()
    passed, failed = 0, 0
    for folder, script, name in SCRIPTS:
        ok = run_test(folder, script, name)
        passed += ok; failed += not ok

    elapsed_total = time.time() - t_total
    print(f"\n{'='*65}")
    print(f"  SUMMARY: {passed}/{len(SCRIPTS)} tests passed "
          f"in {elapsed_total/60:.1f} min")
    print(f"{'='*65}")
    print("\n  Results saved in each test's outputs/ folder.")
