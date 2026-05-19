import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import '../models.dart';

class ApiService {
  Future<bool> health(String baseUrl) async {
    final response = await http.get(Uri.parse('$baseUrl/api/health'));
    return response.statusCode == 200;
  }

  Future<PredictionResult> predict({
    required File imageFile,
    required String baseUrl,
    required ModelMode modelMode,
  }) async {
    final request = http.MultipartRequest(
      'POST',
      Uri.parse('$baseUrl/api/predict'),
    );
    request.files.add(
      await http.MultipartFile.fromPath('image', imageFile.path),
    );
    request.fields['model_type'] = modelMode == ModelMode.ensemble
        ? 'ensemble'
        : 'base';
    request.fields['gradcam_enabled'] = 'true';

    final streamed = await request.send();
    final response = await http.Response.fromStream(streamed);
    if (response.statusCode >= 400) {
      throw Exception('Prediction failed: ${response.body}');
    }
    final json = jsonDecode(response.body) as Map<String, dynamic>;
    return PredictionResult.fromApiJson(
      json,
      imagePath: imageFile.path,
      modelMode: modelMode,
    );
  }
}
