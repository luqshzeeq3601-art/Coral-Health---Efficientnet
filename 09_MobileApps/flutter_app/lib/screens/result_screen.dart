import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';

import '../app_state.dart';
import '../models.dart';
import '../theme/app_theme.dart';
import '../widgets/confidence_ring.dart';
import '../widgets/coral_status_card.dart';
import '../widgets/gradcam_viewer.dart';
import '../widgets/probability_bars.dart';

class ResultScreen extends StatefulWidget {
  const ResultScreen({super.key, required this.result, this.readOnly = false});

  final PredictionResult result;
  final bool readOnly;

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  bool saved = false;

  @override
  Widget build(BuildContext context) {
    final color = AppTheme.statusColor(
      widget.result.prediction,
      Theme.of(context).brightness,
    );
    return Scaffold(
      appBar: AppBar(title: const Text('Result')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
        children: [
          Center(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 10),
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(999),
              ),
              child: Text(
                widget.result.prediction,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w800,
                  fontSize: 18,
                ),
              ),
            ),
          ),
          const SizedBox(height: 18),
          Center(
            child: ConfidenceRing(
              value: widget.result.confidence,
              color: color,
            ),
          ),
          const SizedBox(height: 24),
          GradcamViewer(
            originalBase64: widget.result.originalImageBase64,
            overlayBase64: widget.result.overlayImageBase64,
            heatmapBase64: widget.result.heatmapImageBase64,
          ),
          const SizedBox(height: 24),
          ProbabilityBars(probabilities: widget.result.probabilities),
          if (widget.result.uncertainty)
            Padding(
              padding: const EdgeInsets.only(bottom: 18),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Theme.of(
                    context,
                  ).colorScheme.tertiary.withValues(alpha: 0.14),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.warning_amber_rounded),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        'Low confidence prediction. Consider re-capturing with better lighting.',
                      ),
                    ),
                  ],
                ),
              ),
            ),
          CoralStatusCard(
            color: color,
            severity: widget.result.status.severity,
            description: widget.result.status.description,
            recommendation: widget.result.status.recommendation,
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Icon(
                Icons.memory_outlined,
                size: 18,
                color: Theme.of(context).colorScheme.primary,
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  widget.result.modelUsed,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              Expanded(
                child: FilledButton.tonal(
                  onPressed: widget.readOnly || saved
                      ? null
                      : () => _save(context),
                  child: Text(saved ? 'Saved' : 'Save'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: FilledButton.tonalIcon(
                  onPressed: () => SharePlus.instance.share(
                    ShareParams(
                      text:
                          '${widget.result.prediction} coral with ${widget.result.confidence.toStringAsFixed(1)}% confidence via ${widget.result.modelUsed}.',
                    ),
                  ),
                  icon: const Icon(Icons.share_outlined),
                  label: const Text('Share'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: FilledButton(
                  onPressed: widget.readOnly
                      ? null
                      : () => Navigator.of(context).pop(),
                  child: const Text('Re-analyze'),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Future<void> _save(BuildContext context) async {
    await context.read<AppState>().saveCurrentResult();
    if (!mounted) {
      return;
    }
    setState(() => saved = true);
  }
}
