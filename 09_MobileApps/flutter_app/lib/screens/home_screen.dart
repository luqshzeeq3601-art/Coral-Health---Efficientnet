import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app_state.dart';
import '../models.dart';
import '../theme/app_theme.dart';
import 'settings_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    final lastResult = state.lastHistory;
    final brightness = Theme.of(context).brightness;
    return Scaffold(
      appBar: AppBar(
        title: const Text('Coral Health AI'),
        actions: [
          IconButton(
            onPressed: () =>
                Navigator.of(context).pushNamed(SettingsScreen.routeName),
            icon: const Icon(Icons.tune),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(32),
              gradient: AppTheme.heroGradient(brightness),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Field-ready coral assessment',
                  style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  'Capture or upload a reef image, compare fast offline scoring with ensemble inference, and review Grad-CAM evidence on-device.',
                  style: Theme.of(context).textTheme.bodyLarge,
                ),
                const SizedBox(height: 22),
                FilledButton.icon(
                  onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text(
                        'Use the Analyze tab to start a coral assessment.',
                      ),
                    ),
                  ),
                  icon: const Icon(Icons.arrow_forward),
                  label: const Text('Analyze Coral'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),
          const Row(
            children: [
              Expanded(
                child: _StatCard(label: 'Accuracy', value: '98.11%'),
              ),
              SizedBox(width: 12),
              Expanded(
                child: _StatCard(label: 'Inference', value: '~10 ms'),
              ),
              SizedBox(width: 12),
              Expanded(
                child: _StatCard(label: 'Classes', value: '3'),
              ),
            ],
          ),
          const SizedBox(height: 20),
          if (lastResult != null)
            _LastResultCard(entry: lastResult)
          else
            const _EmptyPreviewCard(),
        ],
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  const _StatCard({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(
              value,
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
            ),
            const SizedBox(height: 6),
            Text(label, style: Theme.of(context).textTheme.bodySmall),
          ],
        ),
      ),
    );
  }
}

class _LastResultCard extends StatelessWidget {
  const _LastResultCard({required this.entry});

  final HistoryEntry entry;

  @override
  Widget build(BuildContext context) {
    final color = AppTheme.statusColor(
      entry.prediction,
      Theme.of(context).brightness,
    );
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Row(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(18),
              child: SizedBox(
                width: 76,
                height: 76,
                child: Image.memory(
                  base64Decode(entry.originalImageBase64),
                  fit: BoxFit.cover,
                ),
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: color,
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      entry.prediction,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  const SizedBox(height: 10),
                  Text(
                    '${entry.confidence.toStringAsFixed(1)}% confidence',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    entry.modelUsed,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _EmptyPreviewCard extends StatelessWidget {
  const _EmptyPreviewCard();

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Icon(
              Icons.waves_outlined,
              size: 36,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 12),
            Text(
              'No saved assessments yet',
              style: Theme.of(
                context,
              ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 6),
            Text(
              'Run an analysis and save the result to see your latest coral check here.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}
