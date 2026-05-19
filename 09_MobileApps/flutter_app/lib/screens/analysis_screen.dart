import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../app_state.dart';
import '../widgets/model_selector.dart';
import 'result_screen.dart';

class AnalysisScreen extends StatefulWidget {
  const AnalysisScreen({super.key});

  @override
  State<AnalysisScreen> createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  final picker = ImagePicker();
  XFile? selectedImage;
  bool loading = false;

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    return Scaffold(
      appBar: AppBar(title: const Text('Analyze Coral')),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(20, 12, 20, 32),
        children: [
          Text(
            'Select Image',
            style: Theme.of(
              context,
            ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => _pickImage(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera_outlined),
                  label: const Text('Camera'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: () => _pickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library_outlined),
                  label: const Text('Gallery'),
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          Container(
            height: 280,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(28),
              border: Border.all(
                color: Theme.of(context).colorScheme.outlineVariant,
              ),
              color: Theme.of(
                context,
              ).colorScheme.surfaceContainerHighest.withValues(alpha: 0.35),
            ),
            clipBehavior: Clip.antiAlias,
            child: selectedImage == null
                ? Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.image_search_outlined,
                          size: 42,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                        const SizedBox(height: 10),
                        const Text('No image selected'),
                      ],
                    ),
                  )
                : Image.file(File(selectedImage!.path), fit: BoxFit.cover),
          ),
          const SizedBox(height: 20),
          Text(
            'Model Selector',
            style: Theme.of(
              context,
            ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 12),
          ModelSelector(
            selected: state.selectedModel,
            onChanged: (mode) => state.setSelectedModel(mode),
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            onPressed: selectedImage == null || loading
                ? null
                : () => _runAnalysis(context),
            icon: loading
                ? const SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Icon(Icons.analytics_outlined),
            label: Text(loading ? 'Analyzing...' : 'Analyze'),
          ),
        ],
      ),
    );
  }

  Future<void> _pickImage(ImageSource source) async {
    final file = await picker.pickImage(source: source, imageQuality: 92);
    if (file == null) {
      return;
    }
    setState(() => selectedImage = file);
  }

  Future<void> _runAnalysis(BuildContext context) async {
    final file = selectedImage;
    if (file == null) {
      return;
    }
    setState(() => loading = true);
    try {
      final result = await context.read<AppState>().analyzeImage(file);
      if (!mounted) {
        return;
      }
      await Navigator.of(
        context,
      ).push(MaterialPageRoute(builder: (_) => ResultScreen(result: result)));
    } catch (error) {
      if (!mounted) {
        return;
      }
      final message = error.toString().contains('Prediction failed')
          ? 'Cannot reach backend. Switch to Base mode.'
          : 'Please select an image file';
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(message)));
    } finally {
      if (mounted) {
        setState(() => loading = false);
      }
    }
  }
}
