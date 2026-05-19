# Setup & Run Instructions

## Prerequisites

### 1. Flutter SDK
- Install Flutter: https://docs.flutter.dev/get-started/install/windows
- Recommended channel: `stable`
- Minimum version: 3.19+

```bash
flutter doctor   # verify all checks pass
```

### 2. Android Studio
- Install Android Studio (for Android Emulator)
- Install AVD: **Pixel 6**, API Level **34** (Android 14)
- Enable Hardware Acceleration (HAXM or Hyper-V)

### 3. Python 3.10+ (for backend)
- Confirm the existing project `.venv` has FastAPI + uvicorn:

```bash
cd 04_Web_Application
.venv\Scripts\activate
pip list | findstr fastapi
```

If not present:
```bash
pip install fastapi "uvicorn[standard]" tensorflow pillow numpy opencv-python
```

---

## Step 1 — Export TFLite Model

Run once to generate the on-device model file:

```bash
cd 09_MobileApps\backend
python export_tflite_mobile.py
```

Output: `09_MobileApps\flutter_app\assets\models\coral_single_float32.tflite`

Source model: `02_Modelling\efficientnetb0_coral\models\efficientnetb0_v4robust_seed42_swa.h5`

---

## Step 2 — Start Backend (Ensemble Mode)

```bash
cd 09_MobileApps\backend
uvicorn main:app --port 8000 --host 0.0.0.0
```

Verify: open `http://localhost:8000/api/health` in browser — should return `{"status": "ok"}`.

The Android Emulator accesses the host machine at `http://10.0.2.2:8000` (not localhost).

---

## Step 3 — Run Flutter App

```bash
cd 09_MobileApps\flutter_app

# Install dependencies
flutter pub get

# Start emulator (from Android Studio AVD Manager), then:
flutter run
```

To target a specific device:
```bash
flutter devices          # list connected devices
flutter run -d emulator-5554
```

---

## Flutter Dependencies (`pubspec.yaml`)

```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.2
  tflite_flutter: ^0.10.4
  image_picker: ^1.0.7
  camera: ^0.10.5
  http: ^1.2.1
  sqflite: ^2.3.2
  path_provider: ^2.1.3
  fl_chart: ^0.68.0
  image: ^4.1.7          # pixel manipulation for Grad-CAM
  share_plus: ^9.0.0
```

---

## Backend Dependencies (`backend/requirements.txt`)

```
fastapi
uvicorn[standard]
tensorflow>=2.13
pillow
numpy
opencv-python
python-multipart
```

---

## Android Permissions (`android/app/src/main/AndroidManifest.xml`)

Add these inside `<manifest>`:

```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
<uses-permission android:name="android.permission.INTERNET"/>
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `flutter doctor` shows Android SDK missing | Set `ANDROID_HOME` env var to SDK path |
| TFLite model not found | Re-run `export_tflite_mobile.py` |
| Ensemble mode times out | Check backend is running; confirm URL is `http://10.0.2.2:8000` in Settings |
| Camera not working in emulator | Enable camera in AVD settings (virtual camera) |
| `INTERNET` permission error on Android | Add permission to `AndroidManifest.xml` |
