import 'package:flutter/material.dart';
import '../theme.dart';

enum NavTab { home, analyze, history, info, settings }

class AppBottomNav extends StatelessWidget {
  const AppBottomNav({
    super.key,
    required this.active,
    required this.onChanged,
  });

  final NavTab active;
  final ValueChanged<NavTab> onChanged;

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 80,
      decoration: BoxDecoration(
        color: context.colors.surfaceContainerLowest,
        border: Border(top: BorderSide(color: context.colors.divider)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          _NavItem(icon: Icons.home, label: 'Home', active: active == NavTab.home, onTap: () => onChanged(NavTab.home)),
          _NavItem(icon: Icons.biotech, label: 'Analyze', active: active == NavTab.analyze, onTap: () => onChanged(NavTab.analyze)),
          _NavItem(icon: Icons.history, label: 'History', active: active == NavTab.history, onTap: () => onChanged(NavTab.history)),
          _NavItem(icon: Icons.info_outline, label: 'Info', active: active == NavTab.info, onTap: () => onChanged(NavTab.info)),
          _NavItem(icon: Icons.settings, label: 'Settings', active: active == NavTab.settings, onTap: () => onChanged(NavTab.settings)),
        ],
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  const _NavItem({
    required this.icon,
    required this.label,
    required this.active,
    required this.onTap,
  });
  final IconData icon;
  final String label;
  final bool active;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      behavior: HitTestBehavior.opaque,
      child: SizedBox(
        width: 64,
        height: 80,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (active) ...[
              Container(
                width: 56,
                height: 56,
                decoration: BoxDecoration(
                  color: AppColors.primary,
                  shape: BoxShape.circle,
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.primary.withValues(alpha: 0.4),
                      blurRadius: 16,
                    ),
                  ],
                ),
                child: Icon(icon, color: context.colors.onPrimary, size: 28),
              ),
              const SizedBox(height: 2),
              Text(label,
                  style: AppText.labelSm.copyWith(
                    fontSize: 10,
                    color: AppColors.primary,
                    fontWeight: FontWeight.w600,
                  )),
            ] else ...[
              Icon(icon, color: context.colors.textMuted.withValues(alpha: 0.6), size: 24),
              const SizedBox(height: 4),
              Text(label,
                  style: AppText.labelSm.copyWith(
                    fontSize: 10,
                    color: context.colors.textMuted.withValues(alpha: 0.6),
                  )),
            ],
          ],
        ),
      ),
    );
  }
}
