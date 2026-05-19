import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

class ProbabilityBars extends StatelessWidget {
  const ProbabilityBars({super.key, required this.probabilities});

  final Map<String, double> probabilities;

  @override
  Widget build(BuildContext context) {
    final brightness = Theme.of(context).brightness;
    const labels = ['Healthy', 'Bleached', 'Dead'];
    return Column(
      children: labels.map((label) {
        final value = probabilities[label] ?? 0;
        final color = AppTheme.statusColor(label, brightness);
        return Padding(
          padding: const EdgeInsets.only(bottom: 14),
          child: Row(
            children: [
              SizedBox(
                width: 84,
                child: Text(
                  label,
                  style: Theme.of(context).textTheme.titleSmall,
                ),
              ),
              Expanded(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(999),
                  child: Container(
                    height: 14,
                    color: Theme.of(context).colorScheme.outlineVariant,
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: TweenAnimationBuilder<double>(
                        tween: Tween(begin: 0, end: value.clamp(0, 100)),
                        duration: const Duration(milliseconds: 900),
                        builder: (context, animated, _) => FractionallySizedBox(
                          widthFactor: animated / 100,
                          child: Container(color: color),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              SizedBox(
                width: 52,
                child: Text(
                  '${value.toStringAsFixed(1)}%',
                  textAlign: TextAlign.right,
                  style: Theme.of(context).textTheme.titleSmall?.copyWith(
                    color: color,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}
