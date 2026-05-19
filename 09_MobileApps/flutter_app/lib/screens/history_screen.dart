import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app_state.dart';
import '../models.dart';
import '../theme/app_theme.dart';
import 'result_screen.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  String filter = 'All';

  @override
  Widget build(BuildContext context) {
    final entries = context
        .watch<AppState>()
        .history
        .where((entry) => filter == 'All' || entry.prediction == filter)
        .toList();
    return Scaffold(
      appBar: AppBar(title: const Text('History')),
      body: entries.isEmpty
          ? const Center(child: Text('No saved assessments yet'))
          : Column(
              children: [
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.fromLTRB(20, 14, 20, 8),
                  child: Row(
                    children: ['All', 'Healthy', 'Bleached', 'Dead'].map((
                      label,
                    ) {
                      return Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: FilterChip(
                          selected: filter == label,
                          label: Text(label),
                          onSelected: (_) => setState(() => filter = label),
                        ),
                      );
                    }).toList(),
                  ),
                ),
                Expanded(
                  child: ListView.separated(
                    padding: const EdgeInsets.fromLTRB(20, 12, 20, 24),
                    itemCount: entries.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 12),
                    itemBuilder: (context, index) {
                      final entry = entries[index];
                      final color = AppTheme.statusColor(
                        entry.prediction,
                        Theme.of(context).brightness,
                      );
                      return InkWell(
                        borderRadius: BorderRadius.circular(24),
                        onTap: () => Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (_) => ResultScreen(
                              result: entry.toPredictionResult(),
                              readOnly: true,
                            ),
                          ),
                        ),
                        onLongPress: () => _confirmDelete(context, entry),
                        child: Ink(
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(24),
                            color: Theme.of(context).cardColor,
                            border: Border(
                              left: BorderSide(color: color, width: 4),
                            ),
                          ),
                          child: Row(
                            children: [
                              ClipRRect(
                                borderRadius: BorderRadius.circular(16),
                                child: Image.memory(
                                  base64Decode(entry.originalImageBase64),
                                  width: 60,
                                  height: 60,
                                  fit: BoxFit.cover,
                                ),
                              ),
                              const SizedBox(width: 14),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Container(
                                          padding: const EdgeInsets.symmetric(
                                            horizontal: 10,
                                            vertical: 5,
                                          ),
                                          decoration: BoxDecoration(
                                            color: color,
                                            borderRadius: BorderRadius.circular(
                                              999,
                                            ),
                                          ),
                                          child: Text(
                                            entry.prediction,
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.w700,
                                            ),
                                          ),
                                        ),
                                        const SizedBox(width: 8),
                                        Text(
                                          '${entry.confidence.toStringAsFixed(1)}%',
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 8),
                                    Text(
                                      '${entry.createdAt.day}/${entry.createdAt.month}/${entry.createdAt.year}  ${entry.createdAt.hour.toString().padLeft(2, '0')}:${entry.createdAt.minute.toString().padLeft(2, '0')}',
                                      style: Theme.of(
                                        context,
                                      ).textTheme.bodySmall,
                                    ),
                                    Text(
                                      entry.modelMode.label,
                                      style: Theme.of(
                                        context,
                                      ).textTheme.bodySmall,
                                    ),
                                  ],
                                ),
                              ),
                              const Icon(Icons.chevron_right),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
    );
  }

  Future<void> _confirmDelete(BuildContext context, HistoryEntry entry) async {
    final delete = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete assessment?'),
        content: const Text(
          'This saved result will be removed from local history.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Delete'),
          ),
        ],
      ),
    );
    if (delete == true && context.mounted) {
      await context.read<AppState>().deleteHistoryEntry(entry);
    }
  }
}
