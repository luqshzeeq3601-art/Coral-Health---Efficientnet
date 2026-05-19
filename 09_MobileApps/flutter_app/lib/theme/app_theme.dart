import 'package:flutter/material.dart';

class AppTheme {
  static const reefDayPrimary = Color(0xFF0E7C86);
  static const reefDaySecondary = Color(0xFFFF7E6B);
  static const reefDayTertiary = Color(0xFFF4B860);
  static const reefDayBackground = Color(0xFFF8FBFC);
  static const reefDaySurfaceVariant = Color(0xFFEEF4F6);
  static const deepSeaPrimary = Color(0xFF5EEAD4);
  static const deepSeaSecondary = Color(0xFFFB7185);
  static const deepSeaTertiary = Color(0xFFFBBF24);
  static const deepSeaBackground = Color(0xFF0B1620);
  static const deepSeaSurface = Color(0xFF142433);
  static const deepSeaSurfaceVariant = Color(0xFF1E3245);

  static const healthyLight = Color(0xFF16A34A);
  static const bleachedLight = Color(0xFFF59E0B);
  static const deadLight = Color(0xFFDC2626);
  static const healthyDark = Color(0xFF4ADE80);
  static const bleachedDark = Color(0xFFFBBF24);
  static const deadDark = Color(0xFFF87171);

  static ThemeData get lightTheme {
    final scheme = ColorScheme.fromSeed(
      seedColor: reefDayPrimary,
      brightness: Brightness.light,
      primary: reefDayPrimary,
      secondary: reefDaySecondary,
      tertiary: reefDayTertiary,
      surface: Colors.white,
    );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: reefDayBackground,
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: Colors.white.withValues(alpha: 0.96),
        indicatorColor: reefDayPrimary.withValues(alpha: 0.12),
        labelTextStyle: WidgetStateProperty.all(
          const TextStyle(fontWeight: FontWeight.w600),
        ),
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        color: Colors.white,
        shadowColor: const Color(0xFF0F172A).withValues(alpha: 0.06),
        surfaceTintColor: Colors.transparent,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(24),
          side: const BorderSide(color: reefDaySurfaceVariant),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: reefDayBackground,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: Color(0xFFCBD5E1)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: reefDayPrimary, width: 1.4),
        ),
      ),
      chipTheme: ChipThemeData(
        side: BorderSide.none,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(999)),
      ),
    );
  }

  static ThemeData get darkTheme {
    final scheme = ColorScheme.fromSeed(
      seedColor: deepSeaPrimary,
      brightness: Brightness.dark,
      primary: deepSeaPrimary,
      secondary: deepSeaSecondary,
      tertiary: deepSeaTertiary,
      surface: deepSeaSurface,
    );
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: deepSeaBackground,
      navigationBarTheme: NavigationBarThemeData(
        backgroundColor: deepSeaSurface,
        indicatorColor: deepSeaPrimary.withValues(alpha: 0.18),
      ),
      cardTheme: CardThemeData(
        elevation: 0,
        color: deepSeaSurface,
        surfaceTintColor: Colors.transparent,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(24),
          side: const BorderSide(color: deepSeaSurfaceVariant),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: deepSeaSurfaceVariant,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: Color(0xFF334155)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: Color(0xFF334155)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
          borderSide: const BorderSide(color: deepSeaPrimary, width: 1.4),
        ),
      ),
      chipTheme: ChipThemeData(
        side: BorderSide.none,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(999)),
      ),
    );
  }

  static Color statusColor(String label, Brightness brightness) {
    switch (label.toLowerCase()) {
      case 'healthy':
        return brightness == Brightness.dark ? healthyDark : healthyLight;
      case 'bleached':
        return brightness == Brightness.dark ? bleachedDark : bleachedLight;
      case 'dead':
        return brightness == Brightness.dark ? deadDark : deadLight;
      default:
        return brightness == Brightness.dark ? deepSeaPrimary : reefDayPrimary;
    }
  }

  static LinearGradient heroGradient(Brightness brightness) {
    return brightness == Brightness.dark
        ? const LinearGradient(
            colors: [Color(0xFF07131B), Color(0xFF123343), Color(0xFF1F5E63)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          )
        : const LinearGradient(
            colors: [Color(0xFFE8F8FA), Color(0xFFC9EEF1), Color(0xFFFFE8DD)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          );
  }
}
