import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

class InfoScreen extends StatelessWidget {
  const InfoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Coral Health Guide')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
        children: const [
          _InfoCard(
            title: 'Healthy Coral',
            color: AppTheme.healthyLight,
            icon: Icons.eco_outlined,
            description:
                'Normal pigmentation, tissue intact, and strong structural appearance.',
            bullets: [
              'Vibrant color',
              'Full polyp extension',
              'Stable reef growth',
            ],
            actionText: 'Positive indicator. Continue routine monitoring.',
          ),
          SizedBox(height: 16),
          _InfoCard(
            title: 'Bleached Coral',
            color: AppTheme.bleachedLight,
            icon: Icons.sunny_snowing,
            description:
                'Loss of zooxanthellae causing a pale or white appearance.',
            bullets: [
              'Heat stress',
              'Pollution or sediment',
              'Disease or prolonged disturbance',
            ],
            actionText:
                'Monitor closely. Recovery is possible if stressors are reduced.',
          ),
          SizedBox(height: 16),
          _InfoCard(
            title: 'Dead Coral',
            color: AppTheme.deadLight,
            icon: Icons.warning_amber_rounded,
            description:
                'Bare skeleton, algal overgrowth, and structural decline.',
            bullets: [
              'Prolonged bleaching',
              'Physical breakage',
              'Severe disease',
            ],
            actionText: 'Document and report for conservation records.',
          ),
        ],
      ),
    );
  }
}

class _InfoCard extends StatelessWidget {
  const _InfoCard({
    required this.title,
    required this.color,
    required this.icon,
    required this.description,
    required this.bullets,
    required this.actionText,
  });

  final String title;
  final Color color;
  final IconData icon;
  final String description;
  final List<String> bullets;
  final String actionText;

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(28),
        border: Border(top: BorderSide(color: color, width: 4)),
        color: Theme.of(context).cardColor,
      ),
      child: ExpansionTile(
        collapsedShape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(28),
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
        title: Text(
          title,
          style: Theme.of(
            context,
          ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
        ),
        subtitle: Text(description),
        leading: Container(
          width: 44,
          height: 44,
          decoration: BoxDecoration(
            color: color.withValues(alpha: 0.14),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color),
        ),
        childrenPadding: const EdgeInsets.fromLTRB(20, 4, 20, 20),
        children: [
          Container(
            height: 160,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(22),
              gradient: LinearGradient(
                colors: [
                  color.withValues(alpha: 0.18),
                  color.withValues(alpha: 0.45),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
            ),
            child: Center(child: Icon(icon, size: 72, color: color)),
          ),
          const SizedBox(height: 16),
          ...bullets.map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.circle, size: 8, color: color),
                  const SizedBox(width: 10),
                  Expanded(child: Text(item)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 4),
          Text(
            actionText,
            style: Theme.of(
              context,
            ).textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.w700),
          ),
        ],
      ),
    );
  }
}
