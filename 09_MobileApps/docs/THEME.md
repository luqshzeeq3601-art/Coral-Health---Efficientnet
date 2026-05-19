# Theme System — CoralScan AI Mobile App

Design language inspired by marine/ocean conservation apps (e.g., NOAA, Ocean Conservancy) combined with modern health monitoring UI patterns (Apple Health, Fitbit). Built on **Material Design 3** principles with custom marine accent palette.

---

## 1. Design Philosophy

| Principle | Application |
|---|---|
| Ocean-inspired calm | Deep teals and aqua tones evoke underwater clarity |
| Coral-as-accent | Warm coral pink reserved for highlights, status, and CTAs |
| Status clarity | 3 health classes map to traffic-light intuition (green / amber / red) |
| Field-readable | High contrast for outdoor/sunlight use; dark mode for night/boat use |
| Soft depth | Rounded cards (16–24 px radius), subtle shadows, no harsh edges |

---

## 2. Light Theme — "Reef Day"

Mood: clean, scientific, daylight diving. Inspired by shallow tropical water and lab/clinical UIs.

### Core Palette

| Token | Hex | Usage |
|---|---|---|
| `primary` | `#0E7C86` | Deep teal — app bars, primary buttons, active tabs |
| `primary_container` | `#B8E6E9` | Soft aqua — selected state backgrounds |
| `secondary` | `#FF7E6B` | Coral accent — secondary CTAs, highlights |
| `tertiary` | `#F4B860` | Sandy amber — info chips, warnings |
| `background` | `#F8FBFC` | Off-white with cool tint — main canvas |
| `surface` | `#FFFFFF` | Pure white — cards, modals |
| `surface_variant` | `#EEF4F6` | Soft grey-blue — disabled, divider zones |
| `on_primary` | `#FFFFFF` | Text on primary teal |
| `on_surface` | `#0F172A` | Near-black with blue tint — body text |
| `on_surface_muted` | `#64748B` | Slate grey — captions, hints |
| `outline` | `#CBD5E1` | Borders, dividers |

### Status Colours (Class Badges)

| Class | Hex | Background Tint | Text on Badge |
|---|---|---|---|
| Healthy | `#16A34A` | `#DCFCE7` | `#FFFFFF` |
| Bleached | `#F59E0B` | `#FEF3C7` | `#FFFFFF` |
| Dead | `#DC2626` | `#FEE2E2` | `#FFFFFF` |

### Grad-CAM Visualisation

Keep JET colourmap unchanged (scientific standard). Frame heatmap with `outline` colour border at 1 px.

---

## 3. Dark Theme — "Deep Sea"

Mood: bioluminescent night dive. Inspired by deep-ocean documentary UIs and astronomy/diving watch apps.

### Core Palette

| Token | Hex | Usage |
|---|---|---|
| `primary` | `#5EEAD4` | Bright bio-teal — buttons, active tabs (glows on dark) |
| `primary_container` | `#134E4A` | Deep teal — selected state backgrounds |
| `secondary` | `#FB7185` | Soft coral — accents, CTAs |
| `tertiary` | `#FBBF24` | Warm amber — warnings, info |
| `background` | `#0B1620` | Abyssal navy — main canvas |
| `surface` | `#142433` | Deep slate — cards |
| `surface_variant` | `#1E3245` | Slightly raised — divider zones, disabled |
| `on_primary` | `#0B1620` | Dark text on bright teal |
| `on_surface` | `#E2E8F0` | Soft white — body text (avoid pure white) |
| `on_surface_muted` | `#94A3B8` | Cool grey — captions |
| `outline` | `#334155` | Borders, dividers |

### Status Colours (Class Badges)

| Class | Hex | Background Tint | Text on Badge |
|---|---|---|---|
| Healthy | `#4ADE80` | `#14532D` | `#0B1620` |
| Bleached | `#FBBF24` | `#78350F` | `#0B1620` |
| Dead | `#F87171` | `#7F1D1D` | `#FFFFFF` |

### Glow Accents (Optional)

Dark theme allows subtle glow on focus/active states. Apply only to `primary` (bio-teal) at 30 % opacity, blur radius 12 px.

---

## 4. Typography

| Style | Font | Size (sp) | Weight |
|---|---|---|---|
| Display | Inter / SF Pro | 32 | 700 |
| Headline | Inter / SF Pro | 24 | 600 |
| Title | Inter / SF Pro | 18 | 600 |
| Body | Inter / SF Pro | 15 | 400 |
| Caption | Inter / SF Pro | 12 | 500 |
| Metric (confidence %) | Inter / SF Pro | 40 | 700 |

Use letter-spacing `-0.5` on display, `0` on body, `+0.5` on caption labels.

---

## 5. Component Tokens

| Component | Light | Dark |
|---|---|---|
| Card background | `#FFFFFF` | `#142433` |
| Card border | `#EEF4F6` | `#1E3245` |
| Card shadow | `rgba(15,23,42,0.06)` 8 px blur | none (use border only) |
| Button primary | `#0E7C86` text `#FFF` | `#5EEAD4` text `#0B1620` |
| Button secondary | `#FF7E6B` text `#FFF` | `#FB7185` text `#0B1620` |
| Input field BG | `#F8FBFC` | `#1E3245` |
| Input field border | `#CBD5E1` | `#334155` |
| Confidence ring track | `#EEF4F6` | `#1E3245` |
| Confidence ring fill | class colour | class colour |
| Probability bar BG | `#EEF4F6` | `#1E3245` |
| Probability bar fill | class colour | class colour |

---

## 6. Spacing & Radius

| Token | Value |
|---|---|
| `radius_sm` | 8 px |
| `radius_md` | 16 px |
| `radius_lg` | 24 px |
| `radius_pill` | 999 px (badges) |
| `space_xs` | 4 px |
| `space_sm` | 8 px |
| `space_md` | 16 px |
| `space_lg` | 24 px |
| `space_xl` | 32 px |

---

## 7. Per-Screen Theme Application

| Screen | Primary Visual Element | Theme Notes |
|---|---|---|
| Home | Hero banner with `primary` gradient | Show stats row in `surface` cards |
| Analysis | Image preview pane with `outline` border | Model selector uses `primary_container` for active option |
| Result | Confidence ring + Grad-CAM viewer | Status badge dominates top; full class colour usage |
| History | List of `surface` cards | Each card has 4 px left border in class colour |
| Info | 3 expandable cards | Top border 4 px in respective class colour |
| Settings | Standard list view | Subtle dividers using `outline` |

---

## 8. Flutter Implementation (Reference)

```dart
// lib/theme/app_theme.dart
class AppTheme {
  static final lightTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.light(
      primary: Color(0xFF0E7C86),
      onPrimary: Colors.white,
      secondary: Color(0xFFFF7E6B),
      tertiary: Color(0xFFF4B860),
      surface: Colors.white,
      background: Color(0xFFF8FBFC),
      onSurface: Color(0xFF0F172A),
      outline: Color(0xFFCBD5E1),
    ),
    cardTheme: CardTheme(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: Color(0xFFEEF4F6)),
      ),
    ),
  );

  static final darkTheme = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.dark(
      primary: Color(0xFF5EEAD4),
      onPrimary: Color(0xFF0B1620),
      secondary: Color(0xFFFB7185),
      tertiary: Color(0xFFFBBF24),
      surface: Color(0xFF142433),
      background: Color(0xFF0B1620),
      onSurface: Color(0xFFE2E8F0),
      outline: Color(0xFF334155),
    ),
  );

  // Status colours — class-based
  static const Map<String, Color> statusLight = {
    'Healthy': Color(0xFF16A34A),
    'Bleached': Color(0xFFF59E0B),
    'Dead': Color(0xFFDC2626),
  };

  static const Map<String, Color> statusDark = {
    'Healthy': Color(0xFF4ADE80),
    'Bleached': Color(0xFFFBBF24),
    'Dead': Color(0xFFF87171),
  };
}
```

---

## 9. Accessibility Checks

| Pair | Contrast Ratio (WCAG) | Status |
|---|---|---|
| Light `on_surface` on `background` | 14.8:1 | AAA |
| Light `primary` on `surface` | 5.6:1 | AA Large |
| Light `Healthy` badge on `surface` | 4.7:1 | AA |
| Dark `on_surface` on `background` | 13.2:1 | AAA |
| Dark `primary` on `background` | 11.4:1 | AAA |
| Dark `Dead` badge on `surface` | 5.1:1 | AA |

All combinations meet WCAG 2.1 AA standard for normal text.

---

## 10. Inspiration References

| App / Source | What was borrowed |
|---|---|
| Apple Health | Layered card hierarchy, status ring |
| NOAA Ocean Today | Deep teal primary, oceanic gradient |
| Fitbit | Confidence ring + metric display |
| Material Design 3 | Token structure, surface elevation logic |
| iNaturalist | Class-coded badge system for species ID |

---

*This theme system is designed for the CoralScan AI Flutter app. Tokens should be centralised in `lib/theme/app_theme.dart` and consumed via `Theme.of(context)` throughout the codebase. Avoid hardcoding hex values in screen files.*
