import json
import os

SAMPLE_IMAGE = r"c:\Users\ZeeqRyz\OneDrive\Desktop\BASEPROJECT\03_Model_Evaluation\prediction_result_test_healthy.png"
URL = "http://127.0.0.1:5000/api/predict?debug=1"


def main():
    if not os.path.exists(SAMPLE_IMAGE):
        raise FileNotFoundError(SAMPLE_IMAGE)

    try:
        import requests
    except Exception as e:
        print(f"requests import failed: {e}")
        return

    with open(SAMPLE_IMAGE, "rb") as f:
        response = requests.post(URL, files={"image": f}, timeout=180)

    print("HTTP", response.status_code)
    data = response.json()
    print("prediction:", data.get("prediction"))
    print("confidence:", round(float(data.get("confidence", 0.0)), 3))
    probs = {k: round(float(v), 3) for k, v in (data.get("probabilities") or {}).items()}
    print("probabilities:", probs)

    models = data.get("individual_models") or []
    for idx, item in enumerate(models, start=1):
        print(
            f"model{idx} seed={item.get('seed')} pred={item.get('prediction')} conf={float(item.get('confidence', 0.0)):.3f}%"
        )

    debug_rows = data.get("debug_preprocessing") or []
    if debug_rows:
        print("\nServer-side preprocessing debug:")
        for row in debug_rows:
            old_block = row.get("old_div255") or {}
            new_block = row.get("new_float255") or {}
            print(
                f"seed={row.get('seed')} | OLD {old_block.get('prediction')} {float(old_block.get('confidence', 0.0)):.3f}% "
                f"-> NEW {new_block.get('prediction')} {float(new_block.get('confidence', 0.0)):.3f}%"
            )


if __name__ == "__main__":
    main()
