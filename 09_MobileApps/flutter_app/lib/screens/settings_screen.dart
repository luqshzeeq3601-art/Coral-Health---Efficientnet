import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../app_state.dart';
import '../models.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  static const routeName = '/settings';

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late final TextEditingController controller;
  bool testing = false;

  @override
  void initState() {
    super.initState();
    controller = TextEditingController(
      text: context.read<AppState>().apiBaseUrl,
    );
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 28),
        children: [
          TextField(
            controller: controller,
            decoration: const InputDecoration(
              labelText: 'Backend API URL',
              hintText: 'http://10.0.2.2:8000',
            ),
            onChanged: (value) => state.setApiBaseUrl(value),
          ),
          const SizedBox(height: 12),
          FilledButton.tonalIcon(
            onPressed: testing ? null : () => _testConnection(context),
            icon: testing
                ? const SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.network_ping_outlined),
            label: Text(testing ? 'Testing...' : 'Test Connection'),
          ),
          const SizedBox(height: 24),
          Card(
            child: Column(
              children: [
                RadioListTile<ModelMode>(
                  value: ModelMode.ensemble,
                  groupValue: state.selectedModel,
                  title: const Text('Default Model: Ensemble'),
                  subtitle: const Text('5-seed backend inference'),
                  onChanged: (value) =>
                      value == null ? null : state.setSelectedModel(value),
                ),
                RadioListTile<ModelMode>(
                  value: ModelMode.base,
                  groupValue: state.selectedModel,
                  title: const Text('Default Model: Base'),
                  subtitle: const Text('Offline mobile preview'),
                  onChanged: (value) =>
                      value == null ? null : state.setSelectedModel(value),
                ),
                SwitchListTile(
                  value: state.darkMode,
                  title: const Text('Dark Mode'),
                  onChanged: (value) => state.setDarkMode(value),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text(
                    'About',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
                  ),
                  SizedBox(height: 12),
                  Text('Model: EfficientNetB0 SWA Ensemble'),
                  Text('Accuracy: 98.11%'),
                  Text('Classes: Healthy, Bleached, Dead'),
                  Text('App version: 1.0.0'),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _testConnection(BuildContext context) async {
    setState(() => testing = true);
    try {
      final ok = await context.read<AppState>().testConnection();
      if (!context.mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            ok ? 'Backend reachable.' : 'Backend health check failed.',
          ),
        ),
      );
    } catch (_) {
      if (!context.mounted) {
        return;
      }
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(const SnackBar(content: Text('Cannot reach backend.')));
    } finally {
      if (mounted) {
        setState(() => testing = false);
      }
    }
  }
}
