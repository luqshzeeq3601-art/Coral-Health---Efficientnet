# 09 — Coral Health Mobile App

Flutter mobile app for field coral health assessment using EfficientNetB0 SWA ensemble. Users capture or upload a coral image and receive a 3-class prediction (Healthy / Bleached / Dead) with confidence score, per-class probabilities, and a Grad-CAM heatmap.

## Project Structure

```
09_MobileApps/
├── README.md                  ← this file
├── docs/
│   ├── ARCHITECTURE.md        ← folder layout, data flow, state model
│   ├── PAGES.md               ← screen-by-screen UI spec
│   ├── SETUP.md               ← environment setup & run instructions
│   └── VERIFICATION.md        ← test checklist
├── backend/                   ← FastAPI server (ensemble mode)
│   ├── main.py
│   ├── model_service.py
│   ├── export_tflite_mobile.py
│   └── requirements.txt
└── flutter_app/               ← Flutter (Dart) cross-platform app
    ├── lib/
    │   ├── main.dart
    │   ├── app_state.dart
    │   ├── screens/
    │   ├── widgets/
    │   └── services/
    └── assets/
        └── models/
            ├── coral_single_float32.tflite
            └── labels.txt
```

## Quick Start

See [docs/SETUP.md](docs/SETUP.md) for full setup. Short version:

```bash
# 1. Start backend (for Ensemble mode)
cd backend
uvicorn main:app --port 8000 --host 0.0.0.0

# 2. Run Flutter app on Android Emulator
cd flutter_app
flutter run
```

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flutter (Dart) |
| Simulator | Android Emulator — Pixel 6, API 34 |
| On-device ML | `tflite_flutter` + `coral_single_float32.tflite` |
| API backend | FastAPI + uvicorn |
| State | Provider |
| Storage | sqflite (history) + path_provider |
| Charts | fl_chart |
| Camera | image_picker + camera |

## Model Modes

| Mode | How it works | Internet needed |
|---|---|---|
| **Base (fast)** | Single seed42 TFLite model runs on device | No |
| **Ensemble (accurate)** | Calls FastAPI `/api/predict` — 5-seed SWA + TTA + gradient Grad-CAM | Yes |
