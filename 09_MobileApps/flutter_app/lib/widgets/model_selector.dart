import 'package:flutter/material.dart';

import '../models.dart';

class ModelSelector extends StatelessWidget {
  const ModelSelector({
    super.key,
    required this.selected,
    required this.onChanged,
  });

  final ModelMode selected;
  final ValueChanged<ModelMode> onChanged;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Row(
      children: [
        Expanded(
          child: _OptionCard(
            title: 'Ensemble',
            subtitle: 'High Accuracy',
            icon: Icons.layers_outlined,
            selected: selected == ModelMode.ensemble,
            activeColor: scheme.primary,
            onTap: () => onChanged(ModelMode.ensemble),
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _OptionCard(
            title: 'Base',
            subtitle: 'Fast, Offline',
            icon: Icons.flash_on_outlined,
            selected: selected == ModelMode.base,
            activeColor: scheme.primary,
            onTap: () => onChanged(ModelMode.base),
          ),
        ),
      ],
    );
  }
}

class _OptionCard extends StatelessWidget {
  const _OptionCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.selected,
    required this.activeColor,
    required this.onTap,
  });

  final String title;
  final String subtitle;
  final IconData icon;
  final bool selected;
  final Color activeColor;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return AnimatedOpacity(
      duration: const Duration(milliseconds: 220),
      opacity: selected ? 1 : 0.68,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(24),
        child: Ink(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(24),
            border: Border.all(
              color: selected
                  ? activeColor
                  : Theme.of(context).colorScheme.outlineVariant,
              width: 1.8,
            ),
            color: selected
                ? activeColor.withValues(alpha: 0.10)
                : Theme.of(context).cardColor,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, color: activeColor),
              const SizedBox(height: 12),
              Text(
                title,
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
              ),
              Text(subtitle, style: Theme.of(context).textTheme.bodySmall),
            ],
          ),
        ),
      ),
    );
  }
}
