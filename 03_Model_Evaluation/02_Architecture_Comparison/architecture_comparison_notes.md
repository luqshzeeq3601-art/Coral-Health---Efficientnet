# Architecture Comparison Notes

This comparison uses the same 159-image held-out test set and class order: `Healthy`, `Bleached`, `Dead`.

| Model | Type | Parameters | Accuracy | Macro F1 | Dead F1 | Errors |
|---|---|---:|---:|---:|---:|---:|
| EfficientNetB0 Ensemble | 5-seed SWA ensemble | 20.27M | 98.11% | 0.9769 | 0.9655 | 3 |
| ResNet50 Single | Single robust SWA model | 23.59M | 98.11% | 0.9586 | 0.8966 | 3 |
| ConvNeXtTiny Single | Single robust SWA model | 27.82M | 97.48% | 0.9724 | 0.9655 | 4 |

## Interpretation

- Best accuracy: `EfficientNetB0 Ensemble, ResNet50 Single` tied at `98.11%`.
- Best macro F1: `EfficientNetB0 Ensemble` at `0.9769`.
- Largest model: `ConvNeXtTiny Single` with `27.82M` parameters.
- EfficientNetB0 uses `4,053,414 x 5 = 20,267,070` parameters on the parameter axis because the current benchmark is a 5-model ensemble.
- ResNet50 matches EfficientNetB0 accuracy but has weaker `Dead` F1, so accuracy alone is not enough to describe robustness.
- ConvNeXtTiny has the largest parameter count, but its accuracy is lower than EfficientNetB0 and ResNet50 on this test split.
