import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import 'models.dart';
import 'services/api_service.dart';
import 'services/storage_service.dart';
import 'services/tflite_service.dart';

class AppState extends ChangeNotifier {
  AppState({
    StorageService? storageService,
    ApiService? apiService,
    TfliteService? tfliteService,
  }) : _storage = storageService ?? StorageService(),
       _api = apiService ?? ApiService(),
       _tflite = tfliteService ?? TfliteService();

  final StorageService _storage;
  final ApiService _api;
  final TfliteService _tflite;

  ModelMode selectedModel = ModelMode.ensemble;
  PredictionResult? result;
  List<HistoryEntry> history = const [];
  String apiBaseUrl = 'http://10.0.2.2:8000';
  bool darkMode = false;

  Future<void> initialize() async {
    selectedModel = ModelModeX.fromStorage(
      await _storage.getSetting('defaultModel'),
    );
    apiBaseUrl = await _storage.getSetting('apiBaseUrl') ?? apiBaseUrl;
    darkMode = (await _storage.getSetting('darkMode')) == 'true';
    history = await _storage.loadHistory();
    notifyListeners();
  }

  HistoryEntry? get lastHistory => history.isEmpty ? null : history.first;

  Future<void> setSelectedModel(ModelMode mode) async {
    selectedModel = mode;
    await _storage.saveSetting('defaultModel', mode.storageValue);
    notifyListeners();
  }

  Future<void> setDarkMode(bool enabled) async {
    darkMode = enabled;
    await _storage.saveSetting('darkMode', enabled.toString());
    notifyListeners();
  }

  Future<void> setApiBaseUrl(String url) async {
    apiBaseUrl = url;
    await _storage.saveSetting('apiBaseUrl', url);
    notifyListeners();
  }

  Future<bool> testConnection() => _api.health(apiBaseUrl);

  Future<PredictionResult> analyzeImage(XFile file) async {
    final imageFile = File(file.path);
    if (selectedModel == ModelMode.ensemble) {
      result = await _api.predict(
        imageFile: imageFile,
        baseUrl: apiBaseUrl,
        modelMode: selectedModel,
      );
    } else {
      result = await _tflite.predict(imageFile);
    }
    notifyListeners();
    return result!;
  }

  Future<void> saveCurrentResult() async {
    if (result == null) {
      return;
    }
    await _storage.saveHistoryEntry(HistoryEntry.fromResult(result!));
    history = await _storage.loadHistory();
    notifyListeners();
  }

  Future<void> deleteHistoryEntry(HistoryEntry entry) async {
    if (entry.id != null) {
      await _storage.deleteHistoryEntry(entry.id!);
      history = await _storage.loadHistory();
      notifyListeners();
    }
  }
}
