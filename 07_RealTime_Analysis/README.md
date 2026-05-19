# Safe Real-Time Coral Analysis

This folder is isolated from the current 98.11% model pipeline. It uses copied model artifacts from `07_RealTime_Analysis/models` and never writes generated files into `02_Modelling/efficientnetb0_coral/models`.

## What This Adds

- Standalone Flask app on `http://localhost:5050/`
- Live webcam analysis through the browser
- Local video-file analysis through the browser
- Optional server-side webcam/video capture APIs
- Fast single-model inference by default
- Optional Grad-CAM explanation only when requested
- Optional TFLite export into `07_RealTime_Analysis/artifacts`

## Safety

The copied model checksum is recorded in `model_manifest.json`.

Do not edit, overwrite, rename, or delete the original model files in:

```text
02_Modelling/efficientnetb0_coral/models/
```

Generated files must stay inside:

```text
07_RealTime_Analysis/artifacts/
```

## Run

From the project root:

```powershell
.venv\Scripts\python.exe 07_RealTime_Analysis\app.py
```

Then open:

```text
http://localhost:5050/
```

## Smartphone Camera Switching

The browser camera flow now:

- Prefers the rear camera first using `facingMode: environment`.
- Shows a `Camera` dropdown after camera permission is granted.
- Provides a `Flip Camera` button while webcam mode is running.
- Falls back to the selfie camera if the browser does not allow direct rear-camera access.

If the page still opens the selfie camera first, press `Flip Camera` once or choose the rear/back camera from the `Camera` dropdown.

## Live Prediction Box

The camera preview draws a live box over the analyzed frame and labels it with the current class and confidence score, for example `Healthy 99.12%`. This is a classifier overlay for the full analyzed view, not a true multi-object detector. Multiple object boxes would require a separate detection model such as YOLO.

## Modes

- `fast`: one copied model, no TTA, no automatic Grad-CAM.
- `balanced`: uses up to three copied models if they are later copied into this folder.
- `accurate`: uses up to five copied models if they are later copied into this folder.

Only `seed42` is copied by default to protect the current benchmark pipeline and keep the first real-time version fast.

## API

- `GET /api/health`
- `POST /api/frame`
- `POST /api/explain`
- `POST /api/video/start`
- `POST /api/video/stop`
- `GET /api/video/status`

## TFLite Export

Float32 export:

```powershell
cd 07_RealTime_Analysis
..\.venv\Scripts\python.exe export_tflite.py --model seed42
```

Full-int8 export for Coral TPU preparation:

```powershell
cd 07_RealTime_Analysis
..\.venv\Scripts\python.exe export_tflite.py --model seed42 --int8
```

TFLite outputs are saved only in `07_RealTime_Analysis/artifacts/`.
