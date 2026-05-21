# Light Theme Implementation Plan

## Goal

Add a working soft-cream **light theme** to the Coral AI Flutter app that mirrors the existing dark theme pixel-for-pixel — same layout, same content, same shapes. Only the surface and text colors change. The aqua primary `#00F5D4` and status colors (Healthy / Bleached / Dead) stay identical so brand and meaning are preserved.

The existing **Dark Mode** toggle in the Settings screen wires up to actually switch themes, and the user's choice persists across app restarts via `SharedPreferences`.

## Architecture

Flutter's idiomatic `ThemeExtension` API:
- `CoralColors extends ThemeExtension<CoralColors>` — holds all custom color tokens
- Two instances: `CoralColors.dark` (existing palette) and `CoralColors.light` (new cream palette)
- Both attached to `ThemeData.extensions` for their respective `MaterialApp.theme` / `MaterialApp.darkTheme`
- `BuildContext.colors` getter for ergonomic access: `context.colors.background`
- `ThemeController extends ChangeNotifier` holds the current `ThemeMode`, persists via `SharedPreferences`, listens via `AnimatedBuilder` at the `MaterialApp` level

## Palette

See [PALETTE.md](PALETTE.md) for the full hex reference for both palettes.

## Files modified

| File | Purpose |
|---|---|
| `lib/theme.dart` | Rewritten: `CoralColors` ThemeExtension, dark + light instances, `context.colors` getter |
| `lib/services/theme_controller.dart` | New: `ChangeNotifier` with `SharedPreferences` persistence |
| `lib/main.dart` | Wire `theme` + `darkTheme` + `themeMode`; await `ThemeController.load()` before runApp |
| `lib/screens/*.dart` | All references to `AppColors.X` replaced with `context.colors.X`; hardcoded `Colors.white.withValues(...)` replaced with semantic tokens like `context.colors.glassThin` |
| `lib/widgets/app_bottom_nav.dart` | Same migration |
| `lib/screens/settings_screen.dart` | Dark Mode switch wires to `ThemeController.setMode()` |
| `pubspec.yaml` | Adds `shared_preferences` dependency |

## Verification

1. `flutter analyze` — 0 errors
2. `flutter run -d emulator-5554`, hot restart (`R`)
3. Toggle Dark Mode in Settings → entire app transitions to cream/white
4. Tap each tab — light theme applies everywhere
5. Push Result screen via Analyze → hero card still readable
6. Force-close + re-open → theme persists
7. Toggle back → full app returns to dark
