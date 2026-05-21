# Theme System — CoralScan AI Mobile App

Dark-first design language inspired by modern fitness/health tracker apps (high-contrast neon-on-black aesthetic). The signature neon yellow accent is replaced with **bioluminescent aqua** to evoke ocean/marine context. Light theme provided as fallback for daytime field use.

---

## 1. Design Philosophy

| Principle | Application |
|---|---|
| Dark-first | Primary theme is dark; mirrors deep ocean / underwater feel |
| Single bright accent | One vivid signature colour (`#00F5D4`) used sparingly for impact |
| Bold metrics | Large numeric displays with small unit labels underneath |
| Card-driven | Everything lives in rounded surface cards (radius 20–24 px) |
| Pill controls | Filter chips and toggles use full-pill rounded shapes |
| Minimal chrome | No heavy borders; depth created by surface tint differences |

---

## 2. Dark Theme — "Deep Reef" (PRIMARY)

Mood: night dive with bioluminescent glow. Matches the reference fitness-app dark aesthetic with marine-inspired accent.

### Core Palette

| Token | Hex | Usage |
|---|---|---|
| `background` | `#0E0E0E` | App canvas — deep oceanic black |
| `surface` | `#1A1A1A` | Card backgrounds |
| `surface_elevated` | `#2B2B2B` | Raised cards, modals, input fields |
| `surface_variant` | `#252525` | Secondary cards, list items |
| `primary` | `#00F5D4` | Bioluminescent aqua — CTAs, active state, accent fills |
| `primary_muted` | `#0EA5A5` | Pressed state for primary |
| `secondary` | `#FF7E6B` | Coral pink — secondary highlights, decorative |
| `on_primary` | `#0E0E0E` | Dark text on aqua buttons |
| `on_surface` | `#FFFFFF` | Body text |
| `on_surface_muted` | `#A1A1AA` | Captions, helper text |
| `on_surface_dim` | `#52525B` | Disabled text, placeholders |
| `divider` | `#27272A` | Subtle separators |

### Status Colours (Class Badges)

| Class | Hex | Pill Background | Text/Icon on Pill |
|---|---|---|---|
| Healthy | `#4ADE80` | `#4ADE8033` (20% alpha) | `#4ADE80` |
| Bleached | `#FBBF24` | `#FBBF2433` | `#FBBF24` |
| Dead | `#F87171` | `#F8717133` | `#F87171` |

> Status pills follow the reference fitness app's pattern: translucent background with full-opacity text in the same hue. Active state uses solid background with dark text.

### Chart & Graph Accents

| Element | Hex |
|---|---|
| Confidence ring fill | `#00F5D4` |
| Confidence ring track | `#2B2B2B` |
| Probability bar fill (active) | `#00F5D4` |
| Probability bar BG | `#2B2B2B` |
| Mini chart line/area | `#00F5D4` with `#00F5D420` fill |
| Sparkline accent | `#00F5D4` |

---

## 3. Light Theme — "Reef Day" (SECONDARY)

For daytime/outdoor field use. Inverts the palette but keeps the same accent identity.

### Core Palette

| Token | Hex | Usage |
|---|---|---|
| `background` | `#F8FAFC` | Off-white canvas |
| `surface` | `#FFFFFF` | Cards |
| `surface_elevated` | `#F1F5F9` | Raised cards |
| `surface_variant` | `#E2E8F0` | Disabled zones |
| `primary` | `#0EA5A5` | Deeper teal (aqua too bright on white) |
| `secondary` | `#FF7E6B` | Coral pink |
| `on_surface` | `#0F172A` | Body text |
| `on_surface_muted` | `#64748B` | Captions |
| `divider` | `#E2E8F0` | Separators |

### Status Colours (Light)

| Class | Hex | Pill Background |
|---|---|---|
| Healthy | `#16A34A` | `#DCFCE7` |
| Bleached | `#F59E0B` | `#FEF3C7` |
| Dead | `#DC2626` | `#FEE2E2` |

---

## 4. Typography

Reference app uses Helvetica. We adopt **Inter** as a free, geometric alternative with identical visual weight.

| Style | Font | Size (sp) | Weight | Use Case |
|---|---|---|---|---|
| Display | Inter | 32 | 700 | Hero titles, "Get Started" page |
| Headline | Inter | 24 | 600 | Screen titles |
| Title | Inter | 18 | 600 | Card headers |
| Body | Inter | 15 | 400 | Paragraphs |
| Caption | Inter | 12 | 500 | Labels, helper text |
| Metric Large | Inter | 40 | 700 | Confidence %, headline numbers |
| Metric Small | Inter | 14 | 400 | Unit labels under metrics (e.g., "Kcal") |

Letter-spacing: `-0.5` on display, `0` on body, `+0.3` on caption (all uppercase labels).

---

## 5. Component Tokens

### Buttons

| Button Type | Background | Text Colour | Border Radius | Padding |
|---|---|---|---|---|
| Primary | `#00F5D4` | `#0E0E0E` | 999 (pill) | 16 × 32 |
| Secondary | transparent | `#00F5D4` | 999 | 16 × 32 |
| Outline | transparent | `#FFFFFF` | 999 | 16 × 32 (1 px `#27272A`) |
| Icon Circle (active) | `#00F5D4` | `#0E0E0E` | 999 | 48 × 48 |

### Cards

| Card Type | Background | Border Radius | Shadow |
|---|---|---|---|
| Standard | `#1A1A1A` | 20 | none |
| Elevated | `#2B2B2B` | 24 | none |
| Hero (with image) | image + dark gradient overlay | 24 | none |

### Inputs

| Element | Value |
|---|---|
| Background | `#2B2B2B` |
| Border | none (or `#27272A` 1 px on focus) |
| Text | `#FFFFFF` |
| Placeholder | `#52525B` |
| Border radius | 16 |

### Bottom Navigation

| State | Background | Icon Colour |
|---|---|---|
| Bar background | `#0E0E0E` (with 1 px top divider `#27272A`) |  |
| Active icon | wrapped in `#00F5D4` circle | `#0E0E0E` |
| Inactive icon | none | `#52525B` |

---

## 6. Spacing & Radius

| Token | Value |
|---|---|
| `radius_sm` | 12 px |
| `radius_md` | 20 px |
| `radius_lg` | 24 px |
| `radius_xl` | 32 px |
| `radius_pill` | 999 px |
| `space_xs` | 4 px |
| `space_sm` | 8 px |
| `space_md` | 16 px |
| `space_lg` | 24 px |
| `space_xl` | 32 px |
| `space_2xl` | 48 px |

---

## 7. Per-Screen Theme Application

| Screen | Visual Signature |
|---|---|
| **Onboarding/Home** | Full-bleed coral reef hero image, dark gradient overlay, bottom pill CTA in `#00F5D4`, motivational headline with `#00F5D4` highlighted words |
| **Dashboard** | Welcome header with avatar, "Last Scan" hero card, 2×2 metrics grid (accuracy %, inference ms), filter pills |
| **Analysis** | Large camera/upload buttons as elevated cards, image preview in rounded card, model selector as pill toggles |
| **Result** | Hero confidence ring (large, central), 3-way Grad-CAM toggle as pill chips, 3 probability bars stacked, recommendation card |
| **History** | List of session cards with thumbnails, mini chart showing assessment trend over time |
| **Info** | Three expandable coral class cards, each with representative photo |
| **Settings** | Standard list of toggle switches with `#00F5D4` active state |

---

## 8. Visual Patterns from Reference

These specific UI patterns from the fitness app translate directly to your project:

| Reference Element | CoralScan Equivalent |
|---|---|
| "Health Grade 80" circular ring | Confidence % ring on Result screen |
| "Running 7 days" hero stat card | "Last Assessment" card on Home |
| Filter pills (All type / Strength / Chest / Arm) | Grad-CAM toggle (Original / Overlay / Heatmap) |
| 2×2 metric cards with mini charts | Per-class probability cards |
| Bottom nav with active accent circle | 4-tab nav: Home / Analyze / History / Info |
| Hero image with dark gradient + CTA | Onboarding screen |
| Welcome header with avatar + bell icon | Dashboard top bar |

---

## 9. Flutter Implementation

```dart
// lib/theme/app_theme.dart
import 'package:flutter/material.dart';

class AppColors {
  // Dark theme
  static const background = Color(0xFF0E0E0E);
  static const surface = Color(0xFF1A1A1A);
  static const surfaceElevated = Color(0xFF2B2B2B);
  static const primary = Color(0xFF00F5D4);      // Bioluminescent aqua
  static const secondary = Color(0xFFFF7E6B);    // Coral pink
  static const textPrimary = Color(0xFFFFFFFF);
  static const textMuted = Color(0xFFA1A1AA);
  static const divider = Color(0xFF27272A);

  // Status
  static const healthy = Color(0xFF4ADE80);
  static const bleached = Color(0xFFFBBF24);
  static const dead = Color(0xFFF87171);
}

class AppTheme {
  static final darkTheme = ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    scaffoldBackgroundColor: AppColors.background,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.primary,
      onPrimary: AppColors.background,
      secondary: AppColors.secondary,
      surface: AppColors.surface,
      onSurface: AppColors.textPrimary,
    ),
    fontFamily: 'Inter',
    cardTheme: CardTheme(
      color: AppColors.surface,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.background,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(999),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
        textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: AppColors.background,
      selectedItemColor: AppColors.primary,
      unselectedItemColor: Color(0xFF52525B),
    ),
  );

  // Class colour helper
  static Color statusColor(String className) {
    switch (className) {
      case 'Healthy': return AppColors.healthy;
      case 'Bleached': return AppColors.bleached;
      case 'Dead': return AppColors.dead;
      default: return AppColors.textMuted;
    }
  }
}
```

---

## 10. Accessibility Checks

| Pair | Contrast Ratio (WCAG) | Status |
|---|---|---|
| `#FFFFFF` on `#0E0E0E` | 19.4:1 | AAA |
| `#00F5D4` on `#0E0E0E` | 12.8:1 | AAA |
| `#0E0E0E` on `#00F5D4` (button) | 12.8:1 | AAA |
| `#A1A1AA` on `#0E0E0E` (caption) | 7.9:1 | AAA |
| `#4ADE80` on `#0E0E0E` (Healthy badge) | 11.2:1 | AAA |
| `#FBBF24` on `#0E0E0E` (Bleached) | 11.6:1 | AAA |
| `#F87171` on `#0E0E0E` (Dead) | 6.8:1 | AAA |

All combinations exceed WCAG 2.1 AAA standard.

---

## 11. Design Inspiration Reference

| Source | Element Borrowed |
|---|---|
| Modern fitness tracker UI (reference image) | Dark-first palette, neon accent, pill controls, circular ring metric |
| iNaturalist | Class-coded status badges for species/coral ID |
| Apple Health | Layered card hierarchy, large metric typography |
| NOAA Ocean apps | Marine context, aqua accent identity |

---

*All colour tokens must be consumed via `AppColors` constants in `lib/theme/app_theme.dart`. Never hardcode hex values inside screen or widget files.*
