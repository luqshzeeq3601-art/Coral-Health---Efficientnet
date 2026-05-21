import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'screens/onboarding_screen.dart';
import 'services/theme_controller.dart';
import 'theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await ThemeController.instance.load();
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
    systemNavigationBarColor: Color(0xFF0E0E0E),
    systemNavigationBarIconBrightness: Brightness.light,
  ));
  runApp(const CoralAiApp());
}

class CoralAiApp extends StatelessWidget {
  const CoralAiApp({super.key});

  ThemeData _build({required Brightness brightness, required CoralColors colors}) {
    final base = brightness == Brightness.dark
        ? ThemeData.dark(useMaterial3: true)
        : ThemeData.light(useMaterial3: true);
    return base.copyWith(
      scaffoldBackgroundColor: colors.background,
      colorScheme: (brightness == Brightness.dark
              ? ColorScheme.dark(primary: colors.primary, surface: colors.surface)
              : ColorScheme.light(primary: colors.primary, surface: colors.surface))
          .copyWith(brightness: brightness),
      extensions: [colors],
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: ThemeController.instance,
      builder: (context, _) {
        return MaterialApp(
          title: 'Coral AI',
          debugShowCheckedModeBanner: false,
          themeMode: ThemeController.instance.themeMode,
          theme: _build(brightness: Brightness.light, colors: CoralColors.light),
          darkTheme: _build(brightness: Brightness.dark, colors: CoralColors.dark),
          home: const OnboardingScreen(),
        );
      },
    );
  }
}
