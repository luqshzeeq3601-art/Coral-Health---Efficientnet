import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:geolocator/geolocator.dart';

class WeatherData {
  final double temperature;
  final double uvIndex;

  const WeatherData({required this.temperature, required this.uvIndex});
}

class WeatherService {
  static Future<WeatherData?> fetch() async {
    try {
      final position = await _getLocation();
      if (position == null) return null;

      final uri = Uri.parse(
        'https://api.open-meteo.com/v1/forecast'
        '?latitude=${position.latitude}'
        '&longitude=${position.longitude}'
        '&current=temperature_2m,uv_index'
        '&timezone=auto',
      );

      final response = await http.get(uri).timeout(const Duration(seconds: 8));
      if (response.statusCode != 200) return null;

      final json = jsonDecode(response.body);
      final current = json['current'];
      return WeatherData(
        temperature: (current['temperature_2m'] as num).toDouble(),
        uvIndex: (current['uv_index'] as num).toDouble(),
      );
    } catch (_) {
      return null;
    }
  }

  static Future<Position?> _getLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) return null;

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) return null;
    }
    if (permission == LocationPermission.deniedForever) return null;

    return await Geolocator.getCurrentPosition(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.low,
        timeLimit: Duration(seconds: 5),
      ),
    );
  }

  static String uvLabel(double uv) {
    if (uv < 3) return 'LOW';
    if (uv < 6) return 'MODERATE';
    if (uv < 8) return 'HIGH';
    if (uv < 11) return 'VERY HIGH';
    return 'EXTREME';
  }
}
