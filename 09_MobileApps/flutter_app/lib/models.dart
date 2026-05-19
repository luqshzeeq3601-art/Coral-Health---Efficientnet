import 'dart:convert';

enum ModelMode { ensemble, base }

extension ModelModeX on ModelMode {
  String get label => this == ModelMode.ensemble ? 'Ensemble' : 'Base';
  String get description =>
      this == ModelMode.ensemble ? 'High Accuracy' : 'Fast, Offline';
  String get storageValue => name;

  static ModelMode fromStorage(String? value) {
    return value == ModelMode.base.name ? ModelMode.base : ModelMode.ensemble;
  }
}

class CoralStatus {
  const CoralStatus({
    required this.severity,
    required this.description,
    required this.recommendation,
  });

  final String severity;
  final String description;
  final String recommendation;

  Map<String, dynamic> toJson() => {
    'severity': severity,
    'description': description,
    'recommendation': recommendation,
  };

  factory CoralStatus.fromJson(Map<String, dynamic> json) => CoralStatus(
    severity: json['severity'] as String? ?? 'Info',
    description: json['description'] as String? ?? '',
    recommendation: json['recommendation'] as String? ?? '',
  );
}

class PredictionResult {
  const PredictionResult({
    required this.imagePath,
    required this.prediction,
    required this.confidence,
    required this.probabilities,
    required this.status,
    required this.modelMode,
    required this.modelUsed,
    required this.originalImageBase64,
    required this.overlayImageBase64,
    required this.heatmapImageBase64,
    required this.timestamp,
    required this.uncertainty,
    this.individualModels = const [],
  });

  final String imagePath;
  final String prediction;
  final double confidence;
  final Map<String, double> probabilities;
  final CoralStatus status;
  final ModelMode modelMode;
  final String modelUsed;
  final String originalImageBase64;
  final String overlayImageBase64;
  final String heatmapImageBase64;
  final DateTime timestamp;
  final bool uncertainty;
  final List<Map<String, dynamic>> individualModels;

  factory PredictionResult.fromApiJson(
    Map<String, dynamic> json, {
    required String imagePath,
    required ModelMode modelMode,
  }) {
    final rawProbabilities =
        (json['probabilities'] as Map<String, dynamic>? ?? {});
    final individuals = <Map<String, dynamic>>[];
    for (final item
        in (json['individual_models'] as List<dynamic>? ?? const <dynamic>[])) {
      if (item is Map<String, dynamic>) {
        individuals.add(item);
      } else if (item is Map) {
        individuals.add(
          item.map((key, value) => MapEntry(key.toString(), value)),
        );
      }
    }
    return PredictionResult(
      imagePath: imagePath,
      prediction: json['prediction'] as String? ?? 'Healthy',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0,
      probabilities: rawProbabilities.map(
        (key, value) => MapEntry(key, (value as num).toDouble()),
      ),
      status: CoralStatus.fromJson(
        json['status'] as Map<String, dynamic>? ?? {},
      ),
      modelMode: modelMode,
      modelUsed: json['model_used'] as String? ?? modelMode.label,
      originalImageBase64: json['original_image'] as String? ?? '',
      overlayImageBase64:
          (json['gradcam'] as Map<String, dynamic>? ?? {})['overlay']
              as String? ??
          '',
      heatmapImageBase64:
          (json['gradcam'] as Map<String, dynamic>? ?? {})['heatmap']
              as String? ??
          '',
      timestamp: DateTime.now(),
      uncertainty: json['uncertainty'] as bool? ?? false,
      individualModels: individuals,
    );
  }
}

class HistoryEntry {
  const HistoryEntry({
    this.id,
    required this.prediction,
    required this.confidence,
    required this.imagePath,
    required this.createdAt,
    required this.modelMode,
    required this.probabilities,
    required this.status,
    required this.modelUsed,
    required this.originalImageBase64,
    required this.overlayImageBase64,
    required this.heatmapImageBase64,
    required this.uncertainty,
  });

  final int? id;
  final String prediction;
  final double confidence;
  final String imagePath;
  final DateTime createdAt;
  final ModelMode modelMode;
  final Map<String, double> probabilities;
  final CoralStatus status;
  final String modelUsed;
  final String originalImageBase64;
  final String overlayImageBase64;
  final String heatmapImageBase64;
  final bool uncertainty;

  PredictionResult toPredictionResult() => PredictionResult(
    imagePath: imagePath,
    prediction: prediction,
    confidence: confidence,
    probabilities: probabilities,
    status: status,
    modelMode: modelMode,
    modelUsed: modelUsed,
    originalImageBase64: originalImageBase64,
    overlayImageBase64: overlayImageBase64,
    heatmapImageBase64: heatmapImageBase64,
    timestamp: createdAt,
    uncertainty: uncertainty,
  );

  factory HistoryEntry.fromResult(PredictionResult result) => HistoryEntry(
    prediction: result.prediction,
    confidence: result.confidence,
    imagePath: result.imagePath,
    createdAt: result.timestamp,
    modelMode: result.modelMode,
    probabilities: result.probabilities,
    status: result.status,
    modelUsed: result.modelUsed,
    originalImageBase64: result.originalImageBase64,
    overlayImageBase64: result.overlayImageBase64,
    heatmapImageBase64: result.heatmapImageBase64,
    uncertainty: result.uncertainty,
  );

  factory HistoryEntry.fromMap(Map<String, dynamic> map) => HistoryEntry(
    id: map['id'] as int?,
    prediction: map['prediction'] as String,
    confidence: (map['confidence'] as num).toDouble(),
    imagePath: map['image_path'] as String,
    createdAt: DateTime.parse(map['created_at'] as String),
    modelMode: ModelModeX.fromStorage(map['model_mode'] as String?),
    probabilities:
        (jsonDecode(map['probabilities_json'] as String)
                as Map<String, dynamic>)
            .map((key, value) => MapEntry(key, (value as num).toDouble())),
    status: CoralStatus.fromJson(
      jsonDecode(map['status_json'] as String) as Map<String, dynamic>,
    ),
    modelUsed: map['model_used'] as String,
    originalImageBase64: map['original_image'] as String,
    overlayImageBase64: map['overlay_image'] as String,
    heatmapImageBase64: map['heatmap_image'] as String,
    uncertainty: (map['uncertainty'] as int? ?? 0) == 1,
  );

  Map<String, dynamic> toMap() => {
    'id': id,
    'prediction': prediction,
    'confidence': confidence,
    'image_path': imagePath,
    'created_at': createdAt.toIso8601String(),
    'model_mode': modelMode.storageValue,
    'probabilities_json': jsonEncode(probabilities),
    'status_json': jsonEncode(status.toJson()),
    'model_used': modelUsed,
    'original_image': originalImageBase64,
    'overlay_image': overlayImageBase64,
    'heatmap_image': heatmapImageBase64,
    'uncertainty': uncertainty ? 1 : 0,
  };
}
