import 'package:flutter/material.dart';
import '../theme.dart';
import '../widgets/app_bottom_nav.dart';
import 'dashboard_screen.dart';
import 'analysis_screen.dart';
import 'history_screen.dart';
import 'info_screen.dart';
import 'settings_screen.dart';

class MainShell extends StatefulWidget {
  const MainShell({super.key, this.initialTab = NavTab.home});
  final NavTab initialTab;

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  late NavTab _active;

  @override
  void initState() {
    super.initState();
    _active = widget.initialTab;
  }

  int get _index => NavTab.values.indexOf(_active);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.colors.background,
      extendBody: true,
      body: IndexedStack(
        index: _index,
        children: const [
          DashboardScreen(),
          AnalysisScreen(),
          HistoryScreen(),
          InfoScreen(),
          SettingsScreen(),
        ],
      ),
      bottomNavigationBar: AppBottomNav(
        active: _active,
        onChanged: (t) => setState(() => _active = t),
      ),
    );
  }
}
