# Sea-Water Colour Attention Evidence Pack

This evidence pack tests whether the current canonical EfficientNetB0 ensemble depends on blue/cyan sea-water coloured regions. It does not modify or retrain any model.

Important limitation: water regions are detected by HSV/RGB colour heuristics, not human-labelled segmentation masks. Treat the results as shortcut-risk evidence, not definitive pixel-level ground truth.

## Canonical Check

- Model: 5-seed SWA EfficientNetB0 ensemble, seeds `42`.
- Checkpoints: `02_Modelling/efficientnetb0_coral/models/efficientnetb0_v4robust_seed{seed}_swa.h5`.
- Architecture loader: canonical Chapter 4 path from `02_Modelling/efficientnetb0_coral/replot_evaluation.py`.
- Accuracy reproduced by this audit: **100.00%** (4/4).

## CAM Mode Comparison

| CAM mode | Overall majority water CAM | Bleached majority water CAM | Area-adjusted water bias | Median water CAM mass |
|---|---:|---:|---:|---:|
| vanilla | 75.00% | 75.00% | 0.00% | 77.64% |
| eigen | 75.00% | 75.00% | 0.00% | 78.35% |

## Mask Sensitivity

| Mask preset | CAM mode | Overall majority water CAM | Bleached majority water CAM | Median water area | Median enrichment |
|---|---|---:|---:|---:|---:|
| default | vanilla | 75.00% | 75.00% | 82.54% | 0.929x |
| strict_blue | vanilla | 50.00% | 50.00% | 66.86% | 0.735x |
| broad_cyan | vanilla | 100.00% | 100.00% | 87.45% | 0.969x |
| high_saturation | vanilla | 25.00% | 25.00% | 56.48% | 0.702x |

## Counterfactual Water-Region Tests

Water-colour pixels were either neutralized to the image's non-water median colour or hue-shifted/desaturated. Sensitivity means the predicted label changed or the original predicted class dropped by at least 10 percentage points.

| Metric | Value |
|---|---:|
| Counterfactual-sensitive images | 100.00% |
| Prediction changed after water perturbation | 75.00% |
| Median largest confidence drop | 57.87 pp |
| 75th percentile largest confidence drop | 59.27 pp |

| Original prediction | Count | Counterfactual sensitive | Label changed | Median largest drop |
|---|---:|---:|---:|---:|
| Bleached | 4 | 100.00% | 75.00% | 57.87 pp |

## Highest Water-Attention Examples

| Image | True | Predicted | Confidence | Water CAM mass | Enrichment |
|---|---|---|---:|---:|---:|
| Bleached/222.png | Bleached | Bleached | 84.83% | 98.49% | 0.992x |
| Bleached/237.png | Bleached | Bleached | 94.35% | 97.45% | 0.991x |
| Bleached/345.png | Bleached | Bleached | 99.13% | 57.82% | 0.866x |
| Bleached/184.png | Bleached | Bleached | 98.50% | 46.87% | 0.820x |

## Largest Counterfactual Drops

| Image | Original prediction | Original confidence | Mask drop | Shift drop | Label changed |
|---|---|---:|---:|---:|---|
| Bleached/345.png | Bleached | 99.13% | 62.74 pp | 3.29 pp | True |
| Bleached/222.png | Bleached | 84.83% | 58.11 pp | 13.37 pp | True |
| Bleached/237.png | Bleached | 94.35% | 57.62 pp | 5.36 pp | True |
| Bleached/184.png | Bleached | 98.50% | 34.46 pp | 8.19 pp | False |

## Thesis-Ready Conclusion

The audit confirms a moderate shortcut risk concentrated in Bleached predictions: overall water-dominant CAM is not the majority pattern, but Bleached predictions frequently place CAM mass on sea-water coloured regions.
Recommended report wording: Grad-CAM supports that most predictions remain coral-relevant, while the Bleached class has measurable water-colour shortcut risk that should be addressed in a future isolated water-robust training experiment.

## Generated Files

- `water_attention_metrics.csv`: baseline vanilla/default-mask per-image metrics.
- `water_attention_metrics_by_mode.csv`: per-image metrics for vanilla, eigen, and aug+eigen CAM.
- `cam_mode_comparison.csv`: summary table across CAM modes.
- `mask_sensitivity_summary.csv`: sensitivity of results to water-mask thresholds.
- `counterfactual_results.csv`: prediction/confidence changes after water-region perturbation.
- `water_attention_summary.json`: machine-readable evidence pack.
- `panels/`: report-ready example figures.
