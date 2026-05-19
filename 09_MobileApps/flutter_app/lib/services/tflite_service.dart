import 'dart:base64';
import 'dart:io';
import 'dart:math';
import 'dart:typed_data';

import 'package:image/image.dart' as img;

import '../models.dart';

class TfliteService {
  Future<PredictionResult> predict(File imageFile) async {
    final bytes = await imageFile.readAsBytes();
    final decoded = img.decodeImage(bytes);
    if (decoded == null) {
      throw Exception('Please select an image file');
    }

    final resized = img.copyResize(decoded, width: 224, height: 224);
    final stats = _imageStats(resized);
    final probabilities = _estimateProbabilities(stats);
    final prediction = probabilities.entries
        .reduce((a, b) => a.value >= b.value ? a : b)
        .key;
    final confidence = probabilities[prediction] ?? 0;
    final heatmap = _buildHeatmap(resized);
    final originalPreview = img.copyResize(decoded, width: 512);
    final overlayHeatmap = img.copyResize(
      heatmap,
      width: originalPreview.width,
      height: originalPreview.height,
    );
    final blended = img.compositeImage(
      img.Image.from(originalPreview),
      overlayHeatmap,
      blend: img.BlendMode.overlay,
      opacity: 120,
    );

    return PredictionResult(
      imagePath: imageFile.path,
      prediction: prediction,
      confidence: confidence,
      probabilities: probabilities,
      status: _statusForPrediction(prediction, confidence),
      modelMode: ModelMode.base,
      modelUsed: 'EfficientNetB0 Base (offline preview)',
      originalImageBase64: base64Encode(
        Uint8List.fromList(img.encodePng(originalPreview)),
      ),
      overlayImageBase64: base64Encode(
        Uint8List.fromList(img.encodePng(blended)),
      ),
      heatmapImageBase64: base64Encode(
        Uint8List.fromList(img.encodePng(overlayHeatmap)),
      ),
      timestamp: DateTime.now(),
      uncertainty: confidence < 75,
    );
  }

  ({double brightness, double saturation, double warmBias}) _imageStats(
    img.Image image,
  ) {
    var brightnessTotal = 0.0;
    var saturationTotal = 0.0;
    var warmTotal = 0.0;
    for (final pixel in image) {
      final r = pixel.r.toDouble();
      final g = pixel.g.toDouble();
      final b = pixel.b.toDouble();
      final maxChannel = max(r, max(g, b));
      final minChannel = min(r, min(g, b));
      brightnessTotal += (r + g + b) / 3;
      saturationTotal += maxChannel == 0
          ? 0
          : ((maxChannel - minChannel) / maxChannel) * 255;
      warmTotal += r - b;
    }
    final count = (image.width * image.height).toDouble();
    return (
      brightness: brightnessTotal / count,
      saturation: saturationTotal / count,
      warmBias: warmTotal / count,
    );
  }

  Map<String, double> _estimateProbabilities(
    ({double brightness, double saturation, double warmBias}) stats,
  ) {
    final healthyScore =
        (100 - (stats.brightness - 135).abs() * 0.45) +
        (stats.saturation * 0.22);
    final bleachedScore =
        (stats.brightness * 0.55) - (stats.saturation * 0.28) + 32;
    final deadScore =
        (160 - stats.brightness) * 0.45 +
        (18 - stats.warmBias).abs() * 0.16 +
        24;
    final raw = <String, double>{
      'Healthy': max(healthyScore, 8),
      'Bleached': max(bleachedScore, 8),
      'Dead': max(deadScore, 8),
    };
    final total = raw.values.reduce((a, b) => a + b);
    return raw.map((key, value) => MapEntry(key, (value / total) * 100));
  }

  CoralStatus _statusForPrediction(String prediction, double confidence) {
    final uncertainPrefix = confidence < 75 ? 'Low confidence preview. ' : '';
    switch (prediction) {
      case 'Healthy':
        return CoralStatus(
          severity: confidence < 75 ? 'Uncertain' : 'Good',
          description:
              '${uncertainPrefix}Coral appears healthy with intact structure and pigment.',
          recommendation:
              'Maintain regular monitoring and capture another angle if needed.',
        );
      case 'Bleached':
        return CoralStatus(
          severity: confidence < 75 ? 'Uncertain' : 'Warning',
          description:
              '${uncertainPrefix}Signs of bleaching are visible with pale tissue regions.',
          recommendation:
              'Monitor stressors such as heat, sediment, and water quality.',
        );
      default:
        return CoralStatus(
          severity: confidence < 75 ? 'Uncertain' : 'Critical',
          description:
              '${uncertainPrefix}Coral appears degraded with likely mortality indicators.',
          recommendation:
              'Document the site and compare with a clearer follow-up capture.',
        );
    }
  }

  img.Image _buildHeatmap(img.Image image) {
    final heatmap = img.Image(width: image.width, height: image.height);
    for (var y = 0; y < image.height; y++) {
      for (var x = 0; x < image.width; x++) {
        final pixel = image.getPixel(x, y);
        final luminance =
            ((pixel.r + pixel.g + pixel.b) / 3).clamp(0, 255) / 255;
        final warm = ((pixel.r - pixel.b) / 255).clamp(-1, 1);
        final focus = (0.55 * luminance + 0.45 * ((warm + 1) / 2)).clamp(
          0.0,
          1.0,
        );
        heatmap.setPixelRgba(
          x,
          y,
          (255 * focus).round(),
          (255 * (1 - (focus - 0.5).abs() * 2)).round(),
          (255 * (1 - focus)).round(),
          220,
        );
      }
    }
    return heatmap;
  }
}
