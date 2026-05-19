import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/material.dart';

enum GradcamViewMode { original, overlay, heatmap }

class GradcamViewer extends StatefulWidget {
  const GradcamViewer({
    super.key,
    required this.originalBase64,
    required this.overlayBase64,
    required this.heatmapBase64,
  });

  final String originalBase64;
  final String overlayBase64;
  final String heatmapBase64;

  @override
  State<GradcamViewer> createState() => _GradcamViewerState();
}

class _GradcamViewerState extends State<GradcamViewer> {
  GradcamViewMode mode = GradcamViewMode.overlay;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SegmentedButton<GradcamViewMode>(
          segments: const [
            ButtonSegment(
              value: GradcamViewMode.original,
              label: Text('Original'),
            ),
            ButtonSegment(
              value: GradcamViewMode.overlay,
              label: Text('Overlay'),
            ),
            ButtonSegment(
              value: GradcamViewMode.heatmap,
              label: Text('Heatmap'),
            ),
          ],
          selected: {mode},
          onSelectionChanged: (set) => setState(() => mode = set.first),
        ),
        const SizedBox(height: 16),
        Container(
          height: 260,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),
            border: Border.all(
              color: Theme.of(context).colorScheme.outlineVariant,
            ),
          ),
          clipBehavior: Clip.antiAlias,
          child: Image.memory(
            _bytesForMode(),
            fit: BoxFit.cover,
            errorBuilder: (_, __, ___) =>
                const Center(child: Text('Grad-CAM preview unavailable')),
          ),
        ),
      ],
    );
  }

  Uint8List _bytesForMode() {
    switch (mode) {
      case GradcamViewMode.original:
        return base64Decode(widget.originalBase64);
      case GradcamViewMode.overlay:
        return base64Decode(widget.overlayBase64);
      case GradcamViewMode.heatmap:
        return base64Decode(widget.heatmapBase64);
    }
  }
}
