# Coral TPU Deployment Notes

The current 98.11% Keras model is not modified for Coral TPU work. This folder documents the optional Edge TPU path for files generated from the copied model in `07_RealTime_Analysis/models`.

## Export

From the project root:

```powershell
cd 07_RealTime_Analysis
..\.venv\Scripts\python.exe export_tflite.py --model seed42 --int8
```

The generated file is written to `07_RealTime_Analysis/artifacts/`.

## Compile For Edge TPU

Install Google's Edge TPU compiler separately, then run:

```powershell
edgetpu_compiler artifacts\efficientnetb0_v4robust_seed42_swa_int8.tflite
```

Keep all generated `.tflite`, compiled `.edgetpu.tflite`, and logs inside `07_RealTime_Analysis/artifacts/`.

## Safety

Do not run conversion or compiler output against `02_Modelling/efficientnetb0_coral/models`. The original `.h5` files remain the academic benchmark artifacts and should stay unchanged.
