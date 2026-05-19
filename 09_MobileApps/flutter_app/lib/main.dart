import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'app_state.dart';
import 'screens/analysis_screen.dart';
import 'screens/history_screen.dart';
import 'screens/home_screen.dart';
import 'screens/info_screen.dart';
import 'screens/settings_screen.dart';
import 'theme/app_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final appState = AppState();
  await appState.initialize();
  runApp(CoralHealthAiApp(appState: appState));
}

class CoralHealthAiApp extends StatelessWidget {
  const CoralHealthAiApp({super.key, required this.appState});

  final AppState appState;

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider.value(
      value: appState,
      child: Consumer<AppState>(
        builder: (context, state, _) {
          return MaterialApp(
            debugShowCheckedModeBanner: false,
            title: 'Coral Health AI',
            theme: AppTheme.lightTheme,
            darkTheme: AppTheme.darkTheme,
            themeMode: state.darkMode ? ThemeMode.dark : ThemeMode.light,
            home: const ShellScreen(),
            routes: {SettingsScreen.routeName: (_) => const SettingsScreen()},
          );
        },
      ),
    );
  }
}

class ShellScreen extends StatefulWidget {
  const ShellScreen({super.key});

  @override
  State<ShellScreen> createState() => _ShellScreenState();
}

class _ShellScreenState extends State<ShellScreen> {
  int _index = 0;

  static const _pages = [
    HomeScreen(),
    AnalysisScreen(),
    HistoryScreen(),
    InfoScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _index, children: _pages),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (value) => setState(() => _index = value),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.camera_alt_outlined),
            selectedIcon: Icon(Icons.camera_alt),
            label: 'Analyze',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_outlined),
            selectedIcon: Icon(Icons.history),
            label: 'History',
          ),
          NavigationDestination(
            icon: Icon(Icons.info_outline),
            selectedIcon: Icon(Icons.info),
            label: 'Info',
          ),
        ],
      ),
    );
  }
}
