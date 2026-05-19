# Architecture

## Folder Layout

```
flutter_app/lib/
├── main.dart                    # MaterialApp, NavigationBar (4 tabs)
├── app_state.dart               # Provider — selected model, history list
├── screens/
│   ├── home_screen.dart         # Landing page, last result preview
│   ├── analysis_screen.dart     # Image input + model selector
│   ├── result_screen.dart       # Prediction, Grad-CAM, probability bars
│   ├── history_screen.dart      # Past assessments list (sqflite)
│   ├── info_screen.dart         # Coral health education cards
│   └── settings_screen.dart     # API URL, default model, dark mode
├── widgets/
│   ├── model_selector.dart      # Ensemble / Base radio toggle
│   ├── confidence_ring.dart     # Circular confidence % ring
│   ├── probability_bars.dart    # 3-class bar chart (fl_chart)
│   ├── gradcam_viewer.dart      # Image toggle: Original / Overlay / Heatmap
│   └── coral_status_card.dart   # Color-coded status badge + recommendation
└── services/
    ├── api_service.dart         # HTTP POST to /api/predict
    ├── tflite_service.dart      # On-device TFLite inference + CAM approx
    └── storage_service.dart     # sqflite CRUD for history

backend/
├── main.py                      # FastAPI routes: /api/predict, /api/health
├── model_service.py             # 5-seed SWA, TTA, temperature=0.441, Grad-CAM
└── export_tflite_mobile.py      # Converts seed42_swa.h5 → .tflite (float32)
```

## Data Flow

### Base mode (on-device)
```
User picks image
  → image_picker (File)
  → TFLiteService.predict()
      ├── Resize 224×224, float32
      ├── tflite_flutter interpreter
      ├── Softmax output × temperature T=0.441
      └── CAM approximation (last conv activations × Dense weights)
  → AppState.setResult(prediction, probs, gradcamBitmap)
  → ResultScreen renders
```

### Ensemble mode (API)
```
User picks image
  → image_picker (File)
  → ApiService.predict(imageBytes, modelType='ensemble')
      └── multipart POST to http://<host>:8000/api/predict
  → JSON response: prediction, confidence, probabilities, gradcam.overlay (base64)
  → AppState.setResult(...)
  → ResultScreen renders
```

## State Model (Provider)

```dart
class AppState extends ChangeNotifier {
  ModelMode selectedModel;   // ModelMode.base | ModelMode.ensemble
  PredictionResult? result;  // latest result
  List<HistoryEntry> history;
  String apiBaseUrl;
  bool darkMode;
}
```

## Backend Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/predict` | Accepts multipart image + model_type; returns full JSON result |
| GET | `/api/health` | Server + model load status |

### /api/predict response shape

```json
{
  "prediction": "Healthy",
  "confidence": 92.5,
  "probabilities": { "Healthy": 92.5, "Bleached": 5.1, "Dead": 2.4 },
  "gradcam": { "heatmap": "<base64>", "overlay": "<base64>" },
  "original_image": "<base64>",
  "uncertainty": false,
  "status": {
    "severity": "Good",
    "description": "...",
    "recommendation": "..."
  },
  "model_used": "EfficientNetB0 SWA Ensemble (5-seed)",
  "individual_models": [
    { "fold": 42, "prediction": "Healthy", "confidence": 93.2 }
  ]
}
```

## On-Device Grad-CAM Approximation

TFLite does not expose gradients, so the app uses Class Activation Mapping (CAM):

1. Run inference with a modified model that also outputs the final conv layer activations.
2. Multiply activations by the class-specific Dense layer weights.
3. ReLU + upsample to 224×224.
4. Apply Jet colormap → overlay on original image.

For Ensemble mode, the server sends the real gradient-based Grad-CAM PNG directly.

## Key Source Files to Reference

| File | Purpose |
|---|---|
| `04_Web_Application/app.py` | Port `/api/predict` logic to `backend/main.py` |
| `02_Modelling/efficientnetb0_coral/models/*.h5` | Source models (5 seeds) |
| `02_Modelling/efficientnetb0_coral/models/temperature.txt` | T=0.441 calibration |
| `04_Web_Application/templates/design9.html` (line 2640) | Model Selector UI reference |
