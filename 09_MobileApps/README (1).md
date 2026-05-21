# 09 — Coral Health Mobile App

Flutter mobile app for field coral health assessment using EfficientNetB0 SWA ensemble. Users capture or upload a coral image and receive a 3-class prediction (Healthy / Bleached / Dead) with confidence score, per-class probabilities, and a Grad-CAM heatmap.

**Design language:** Dark-first UI inspired by modern fitness/health tracker apps — high-contrast bioluminescent aqua accent (`#00F5D4`) on deep oceanic black (`#0E0E0E`), with rounded card-based layouts, large metric typography, and pill-shaped controls.

---

## Project Structure

```
09_MobileApps/
├── README.md                  ← this file
├── docs/
│   ├── ARCHITECTURE.md        ← folder layout, data flow, state model
│   ├── PAGES.md               ← screen-by-screen UI spec (updated design)
│   ├── THEME.md               ← colour, typography, component tokens
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
    │   ├── theme/
    │   │   └── app_theme.dart     ← AppColors + light/dark themes
    │   ├── screens/
    │   ├── widgets/
    │   └── services/
    └── assets/
        ├── models/
        │   ├── coral_single_float32.tflite
        │   └── labels.txt
        ├── fonts/
        │   └── Inter/              ← Inter font family
        └── images/
            └── coral_hero.jpg      ← onboarding hero image
```

---

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

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flutter (Dart) |
| Simulator | Android Emulator — Pixel 6, API 34 |
| Design System | Material 3 + custom marine theme |
| On-device ML | `tflite_flutter` + `coral_single_float32.tflite` |
| API backend | FastAPI + uvicorn |
| State | Provider |
| Storage | sqflite (history) + path_provider |
| Charts | fl_chart |
| Camera | image_picker + camera |
| Fonts | Inter (Google Fonts) |

---

## Design Identity at a Glance

| Token | Value | Role |
|---|---|---|
| Background | `#0E0E0E` | Deep oceanic black |
| Surface (cards) | `#1A1A1A` | Card layer |
| Primary accent | `#00F5D4` | Bioluminescent aqua — CTAs, active states |
| Secondary | `#FF7E6B` | Coral pink — highlights |
| Text | `#FFFFFF` / `#A1A1AA` | Primary / muted |
| Healthy | `#4ADE80` | Class badge |
| Bleached | `#FBBF24` | Class badge |
| Dead | `#F87171` | Class badge |

Full spec in [docs/THEME.md](docs/THEME.md).

---

## Model Modes

| Mode | How it works | Internet needed |
|---|---|---|
| **Base (fast)** | Single seed42 TFLite model runs on device | No |
| **Ensemble (accurate)** | Calls FastAPI `/api/predict` — 5-seed SWA + TTA + gradient Grad-CAM | Yes |

---

## App Screens (6 total)

| # | Screen | Purpose |
|---|---|---|
| 1 | Onboarding | Hero welcome screen with CTA |
| 2 | Home / Dashboard | Last scan + health metrics grid |
| 3 | Analyze | Image input + model selector |
| 4 | Result | Confidence ring + Grad-CAM + probabilities |
| 5 | History | Past assessments with weekly trend chart |
| 6 | Info | Coral health education cards |

Settings is a sub-screen accessible from Home top-right gear icon.

Full screen specs in [docs/PAGES.md](docs/PAGES.md).

---

## Design Inspiration

Visual language adapted from modern fitness/health tracker UI patterns:

| Reference Element | CoralScan Adaptation |
|---|---|
| "Health Grade 80" circular ring | Confidence % ring on Result screen |
| Hero stat card with icon | "Last Assessment" card on Home |
| Filter pills row | Grad-CAM toggle, class filters |
| 2×2 metrics with mini charts | Health metrics dashboard |
| Bottom nav with active accent circle | 4-tab navigation |
| Weekly line chart | Assessment activity over time |

The signature **neon yellow → bioluminescent aqua** swap maintains the same high-contrast visual impact while tying to the ocean/marine project theme.
