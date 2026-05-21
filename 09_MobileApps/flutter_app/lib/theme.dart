import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class CoralColors extends ThemeExtension<CoralColors> {
  const CoralColors({
    required this.background,
    required this.surface,
    required this.surfaceElevated,
    required this.surfaceContainerLowest,
    required this.surfaceContainer,
    required this.surfaceContainerHigh,
    required this.primary,
    required this.primaryFixedDim,
    required this.onPrimary,
    required this.onBackground,
    required this.textMuted,
    required this.divider,
    required this.outline,
    required this.healthy,
    required this.bleached,
    required this.dead,
    required this.onTertiary,
    required this.glassThin,
    required this.glassMid,
    required this.glassStrong,
    required this.dim,
    required this.bright,
    required this.scrim,
    required this.heroGradientStart,
    required this.heroGradientEnd,
  });

  final Color background;
  final Color surface;
  final Color surfaceElevated;
  final Color surfaceContainerLowest;
  final Color surfaceContainer;
  final Color surfaceContainerHigh;
  final Color primary;
  final Color primaryFixedDim;
  final Color onPrimary;
  final Color onBackground;
  final Color textMuted;
  final Color divider;
  final Color outline;
  final Color healthy;
  final Color bleached;
  final Color dead;
  final Color onTertiary;
  // Glass / overlay tokens
  final Color glassThin;
  final Color glassMid;
  final Color glassStrong;
  final Color dim;
  final Color bright;
  final Color scrim;
  final Color heroGradientStart;
  final Color heroGradientEnd;

  static const dark = CoralColors(
    background: Color(0xFF0E0E0E),
    surface: Color(0xFF1A1A1A),
    surfaceElevated: Color(0xFF2B2B2B),
    surfaceContainerLowest: Color(0xFF0E0E0E),
    surfaceContainer: Color(0xFF201F1F),
    surfaceContainerHigh: Color(0xFF2A2A2A),
    primary: Color(0xFF00F5D4),
    primaryFixedDim: Color(0xFF00DFC1),
    onPrimary: Color(0xFF006C5C),
    onBackground: Color(0xFFE5E2E1),
    textMuted: Color(0xFFA1A1AA),
    divider: Color(0xFF27272A),
    outline: Color(0xFF83948F),
    healthy: Color(0xFF4ADE80),
    bleached: Color(0xFFFBBF24),
    dead: Color(0xFFF87171),
    onTertiary: Color(0xFF3C2F00),
    glassThin: Color(0x0DFFFFFF),
    glassMid: Color(0x1AFFFFFF),
    glassStrong: Color(0x33FFFFFF),
    dim: Color(0x66FFFFFF),
    bright: Color(0xCCFFFFFF),
    scrim: Color(0xCC000000),
    heroGradientStart: Color(0x00000000),
    heroGradientEnd: Color(0xFF0E0E0E),
  );

  static const light = CoralColors(
    background: Color(0xFFF8F9FA),
    surface: Color(0xFFFFFFFF),
    surfaceElevated: Color(0xFFF1F5F9),
    surfaceContainerLowest: Color(0xFFF8F9FA),
    surfaceContainer: Color(0xFFFFFFFF),
    surfaceContainerHigh: Color(0xFFE5E7EB),
    primary: Color(0xFF00F5D4),
    primaryFixedDim: Color(0xFF00A88E),
    onPrimary: Color(0xFF003D33),
    onBackground: Color(0xFF1A1A1A),
    textMuted: Color(0xFF6B7280),
    divider: Color(0xFFE5E7EB),
    outline: Color(0xFF9CA3AF),
    healthy: Color(0xFF4ADE80),
    bleached: Color(0xFFFBBF24),
    dead: Color(0xFFF87171),
    onTertiary: Color(0xFF3C2F00),
    glassThin: Color(0x0A000000),
    glassMid: Color(0x14000000),
    glassStrong: Color(0x1F000000),
    dim: Color(0x66000000),
    bright: Color(0xCC000000),
    scrim: Color(0xCC000000),
    heroGradientStart: Color(0x00000000),
    heroGradientEnd: Color(0xF2F8F9FA),
  );

  @override
  CoralColors copyWith({
    Color? background,
    Color? surface,
    Color? surfaceElevated,
    Color? surfaceContainerLowest,
    Color? surfaceContainer,
    Color? surfaceContainerHigh,
    Color? primary,
    Color? primaryFixedDim,
    Color? onPrimary,
    Color? onBackground,
    Color? textMuted,
    Color? divider,
    Color? outline,
    Color? healthy,
    Color? bleached,
    Color? dead,
    Color? onTertiary,
    Color? glassThin,
    Color? glassMid,
    Color? glassStrong,
    Color? dim,
    Color? bright,
    Color? scrim,
    Color? heroGradientStart,
    Color? heroGradientEnd,
  }) {
    return CoralColors(
      background: background ?? this.background,
      surface: surface ?? this.surface,
      surfaceElevated: surfaceElevated ?? this.surfaceElevated,
      surfaceContainerLowest: surfaceContainerLowest ?? this.surfaceContainerLowest,
      surfaceContainer: surfaceContainer ?? this.surfaceContainer,
      surfaceContainerHigh: surfaceContainerHigh ?? this.surfaceContainerHigh,
      primary: primary ?? this.primary,
      primaryFixedDim: primaryFixedDim ?? this.primaryFixedDim,
      onPrimary: onPrimary ?? this.onPrimary,
      onBackground: onBackground ?? this.onBackground,
      textMuted: textMuted ?? this.textMuted,
      divider: divider ?? this.divider,
      outline: outline ?? this.outline,
      healthy: healthy ?? this.healthy,
      bleached: bleached ?? this.bleached,
      dead: dead ?? this.dead,
      onTertiary: onTertiary ?? this.onTertiary,
      glassThin: glassThin ?? this.glassThin,
      glassMid: glassMid ?? this.glassMid,
      glassStrong: glassStrong ?? this.glassStrong,
      dim: dim ?? this.dim,
      bright: bright ?? this.bright,
      scrim: scrim ?? this.scrim,
      heroGradientStart: heroGradientStart ?? this.heroGradientStart,
      heroGradientEnd: heroGradientEnd ?? this.heroGradientEnd,
    );
  }

  @override
  CoralColors lerp(ThemeExtension<CoralColors>? other, double t) {
    if (other is! CoralColors) return this;
    return CoralColors(
      background: Color.lerp(background, other.background, t)!,
      surface: Color.lerp(surface, other.surface, t)!,
      surfaceElevated: Color.lerp(surfaceElevated, other.surfaceElevated, t)!,
      surfaceContainerLowest: Color.lerp(surfaceContainerLowest, other.surfaceContainerLowest, t)!,
      surfaceContainer: Color.lerp(surfaceContainer, other.surfaceContainer, t)!,
      surfaceContainerHigh: Color.lerp(surfaceContainerHigh, other.surfaceContainerHigh, t)!,
      primary: Color.lerp(primary, other.primary, t)!,
      primaryFixedDim: Color.lerp(primaryFixedDim, other.primaryFixedDim, t)!,
      onPrimary: Color.lerp(onPrimary, other.onPrimary, t)!,
      onBackground: Color.lerp(onBackground, other.onBackground, t)!,
      textMuted: Color.lerp(textMuted, other.textMuted, t)!,
      divider: Color.lerp(divider, other.divider, t)!,
      outline: Color.lerp(outline, other.outline, t)!,
      healthy: Color.lerp(healthy, other.healthy, t)!,
      bleached: Color.lerp(bleached, other.bleached, t)!,
      dead: Color.lerp(dead, other.dead, t)!,
      onTertiary: Color.lerp(onTertiary, other.onTertiary, t)!,
      glassThin: Color.lerp(glassThin, other.glassThin, t)!,
      glassMid: Color.lerp(glassMid, other.glassMid, t)!,
      glassStrong: Color.lerp(glassStrong, other.glassStrong, t)!,
      dim: Color.lerp(dim, other.dim, t)!,
      bright: Color.lerp(bright, other.bright, t)!,
      scrim: Color.lerp(scrim, other.scrim, t)!,
      heroGradientStart: Color.lerp(heroGradientStart, other.heroGradientStart, t)!,
      heroGradientEnd: Color.lerp(heroGradientEnd, other.heroGradientEnd, t)!,
    );
  }
}

extension CoralColorsX on BuildContext {
  CoralColors get colors => Theme.of(this).extension<CoralColors>() ?? CoralColors.dark;
}

/// Backwards compatibility alias — points to dark palette for any const widgets
/// that genuinely don't need to theme (e.g., status pills with brand colors).
/// Prefer `context.colors.X` for theme-aware code.
class AppColors {
  static const background = Color(0xFF0E0E0E);
  static const surface = Color(0xFF1A1A1A);
  static const surfaceElevated = Color(0xFF2B2B2B);
  static const surfaceContainerLowest = Color(0xFF0E0E0E);
  static const surfaceContainer = Color(0xFF201F1F);
  static const primary = Color(0xFF00F5D4);
  static const primaryFixedDim = Color(0xFF00DFC1);
  static const onPrimary = Color(0xFF006C5C);
  static const onBackground = Color(0xFFE5E2E1);
  static const textMuted = Color(0xFFA1A1AA);
  static const divider = Color(0xFF27272A);
  static const healthy = Color(0xFF4ADE80);
  static const bleached = Color(0xFFFBBF24);
  static const dead = Color(0xFFF87171);
  static const onTertiary = Color(0xFF3C2F00);
}

class AppText {
  static TextStyle display = GoogleFonts.inter(
    fontSize: 32,
    height: 40 / 32,
    letterSpacing: -0.5,
    fontWeight: FontWeight.w700,
  );
  static TextStyle metricXl = GoogleFonts.inter(
    fontSize: 40,
    height: 48 / 40,
    fontWeight: FontWeight.w700,
  );
  static TextStyle headlineLgMobile = GoogleFonts.inter(
    fontSize: 20,
    height: 28 / 20,
    fontWeight: FontWeight.w600,
  );
  static TextStyle titleMd = GoogleFonts.inter(
    fontSize: 18,
    height: 24 / 18,
    fontWeight: FontWeight.w600,
  );
  static TextStyle bodyMd = GoogleFonts.inter(
    fontSize: 15,
    height: 22 / 15,
    fontWeight: FontWeight.w400,
  );
  static TextStyle labelSm = GoogleFonts.inter(
    fontSize: 12,
    height: 16 / 12,
    letterSpacing: 0.3,
    fontWeight: FontWeight.w500,
  );
  static TextStyle metricUnit = GoogleFonts.inter(
    fontSize: 14,
    height: 20 / 14,
    fontWeight: FontWeight.w400,
  );
}
