import 'package:flutter/material.dart';

class CoralStatusCard extends StatelessWidget {
  const CoralStatusCard({
    super.key,
    required this.color,
    required this.severity,
    required this.description,
    required this.recommendation,
  });

  final Color color;
  final String severity;
  final String description;
  final String recommendation;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(24),
        color: color.withValues(alpha: 0.08),
        border: Border.all(color: color.withValues(alpha: 0.22)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.health_and_safety_outlined, color: color),
              const SizedBox(width: 10),
              Text(
                severity,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.w800,
                  color: color,
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Text(description, style: Theme.of(context).textTheme.bodyMedium),
          const SizedBox(height: 10),
          Text(
            'Recommendation',
            style: Theme.of(
              context,
            ).textTheme.labelLarge?.copyWith(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 4),
          Text(recommendation, style: Theme.of(context).textTheme.bodyMedium),
        ],
      ),
    );
  }
}
