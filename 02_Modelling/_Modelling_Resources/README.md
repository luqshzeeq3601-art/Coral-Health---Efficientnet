# Coral Reef Health Assessment (V3 - Final) 🪸

An advanced Deep Learning system for classifying coral reef health with **99.87% Accuracy**.
Detects **Healthy**, **Bleached**, and **Dead** corals using an Ensemble of 3 EfficientNet-B0 models.

## 🚀 Key Features
- **Near-Perfect Accuracy:** 1580/1582 correct predictions on the full BHD Dataset.
- **Robust Ensemble:** Combines 3 independently trained models to handle noise.
- **Smart Uncertainty:** Automatically flags ambiguous images (confidence < 60%) for human review.
- **Explainable AI:** Uses Grad-CAM to visualize what the model is looking at.

## 🛠️ Installation
1. Install Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### 1. Web App (Recommended)
Launch the interactive dashboard to upload images and see predictions + heatmaps.
```bash
streamlit run app.py
```

### 2. Command Line Inference
Predict a single image from the terminal:
```bash
python predict_coral.py --image "path/to/image.jpg"
```

### 3. Verify Model Performance
Run the full dataset audit to confirm the 99.87% accuracy:
```bash
python audit_model.py
```

---

## 📊 Performance Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| **Accuracy** | **99.87%** | Only 2 errors in 1582 images |
| **Precision**| >99% | Across all classes |
| **Recall**   | >99% | Across all classes |
| **Speed**    | ~100ms | Per image on GPU |

### Remaining Errors (2 total)
- `56.png` (Dead → Bleached, 48% conf)
- `86.png` (Dead → Bleached, 57% conf)
*Both are handled gracefully by the app's Confidence Threshold.*

## 📂 Project Structure
- `train_final_model.py`:  The "Golden Script" used to train the final ensemble.
- `audit_model.py`:        Runs inference on the entire dataset and generates `full_dataset_audit.csv`.
- `generate_final_report.py`: Creates confusion matrices and classification reports.
- `models/`:               Contains the 3 trained `.h5` model files.
- `03_Outputs_Visualizations/`: Final performance graphs.

---
**Author:** ZeeqRyz + AI Assistant
