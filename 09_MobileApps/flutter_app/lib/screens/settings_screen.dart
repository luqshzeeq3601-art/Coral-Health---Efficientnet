import 'package:flutter/material.dart';
import '../theme.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final TextEditingController _urlCtrl = TextEditingController(text: 'http://10.0.2.2:8000');
  bool _darkMode = true;
  int _modelIndex = 0;
  double _threshold = 75;

  @override
  void dispose() {
    _urlCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      bottom: false,
      child: Column(
        children: [
          _topBar(),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(16, 24, 16, 110),
              children: [
                _sectionTitle(Icons.settings_ethernet, 'CONNECTION'),
                const SizedBox(height: 16),
                _connectionCard(),
                const SizedBox(height: 24),
                _sectionTitle(Icons.tune, 'PREFERENCES'),
                const SizedBox(height: 16),
                _preferencesCard(),
                const SizedBox(height: 24),
                _sectionTitle(Icons.info, 'ABOUT'),
                const SizedBox(height: 16),
                _aboutCards(),
                const SizedBox(height: 16),
                _developerCredits(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _topBar() {
    return Container(
      height: 64,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      decoration: BoxDecoration(
        color: context.colors.background.withValues(alpha: 0.9),
        border: Border(bottom: BorderSide(color: Colors.white.withValues(alpha: 0.05))),
      ),
      child: Row(
        children: [
          const Icon(Icons.settings, color: AppColors.primary, size: 28),
          const SizedBox(width: 12),
          Text('Settings',
              style: AppText.headlineLgMobile.copyWith(
                color: context.colors.onBackground,
                fontWeight: FontWeight.w700,
              )),
          const Spacer(),
          IconButton(
            icon: const Icon(Icons.help_outline, color: AppColors.primary),
            onPressed: () {},
          ),
        ],
      ),
    );
  }

  Widget _sectionTitle(IconData icon, String text) {
    return Row(
      children: [
        Icon(icon, color: AppColors.primary, size: 20),
        const SizedBox(width: 8),
        Text(text,
            style: AppText.labelSm.copyWith(
              color: AppColors.primary,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.5,
              fontSize: 13,
            )),
      ],
    );
  }

  Widget _connectionCard() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: context.colors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('BACKEND API URL',
              style: AppText.labelSm.copyWith(
                color: context.colors.textMuted,
                fontSize: 11,
                fontWeight: FontWeight.w600,
                letterSpacing: 1,
              )),
          const SizedBox(height: 8),
          TextField(
            controller: _urlCtrl,
            style: AppText.bodyMd.copyWith(color: context.colors.onBackground),
            decoration: InputDecoration(
              filled: true,
              fillColor: Colors.black.withValues(alpha: 0.4),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.white.withValues(alpha: 0.1)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: AppColors.primary),
              ),
            ),
          ),
          const SizedBox(height: 16),
          GestureDetector(
            onTap: () {},
            child: Container(
              height: 52,
              decoration: BoxDecoration(
                color: AppColors.primary,
                borderRadius: BorderRadius.circular(999),
                boxShadow: [
                  BoxShadow(
                    color: AppColors.primary.withValues(alpha: 0.2),
                    blurRadius: 12,
                  ),
                ],
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('Test Connection',
                      style: AppText.titleMd.copyWith(
                        color: context.colors.background,
                        fontSize: 15,
                        fontWeight: FontWeight.w700,
                      )),
                  const SizedBox(width: 8),
                  const Icon(Icons.bolt, color: context.colors.background, size: 20),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _preferencesCard() {
    return Container(
      decoration: BoxDecoration(
        color: context.colors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          _prefRow(
            title: 'Default Model',
            subtitle: 'High-precision ensemble processing',
            trailing: _modelToggle(),
          ),
          _divider(),
          _prefRow(
            title: 'Dark Mode',
            subtitle: 'OLED optimized reef depth aesthetic',
            trailing: Switch(
              value: _darkMode,
              onChanged: (v) => setState(() => _darkMode = v),
              activeThumbColor: context.colors.background,
              activeTrackColor: AppColors.primary,
              inactiveThumbColor: context.colors.textMuted,
              inactiveTrackColor: context.colors.surfaceElevated,
            ),
          ),
          _divider(),
          Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Confidence Threshold',
                            style: AppText.bodyMd.copyWith(
                              color: context.colors.onBackground,
                              fontWeight: FontWeight.w700,
                              fontSize: 15,
                            )),
                        Text('Minimum AI certainty for alerts',
                            style: AppText.labelSm.copyWith(
                              color: context.colors.textMuted.withValues(alpha: 0.7),
                            )),
                      ],
                    ),
                    Text('${_threshold.toInt()}%',
                        style: AppText.headlineLgMobile.copyWith(
                          color: AppColors.primary,
                          fontWeight: FontWeight.w700,
                          fontSize: 22,
                        )),
                  ],
                ),
                const SizedBox(height: 12),
                SliderTheme(
                  data: SliderTheme.of(context).copyWith(
                    activeTrackColor: AppColors.primary,
                    inactiveTrackColor: context.colors.surfaceElevated,
                    thumbColor: AppColors.primary,
                    overlayColor: AppColors.primary.withValues(alpha: 0.2),
                    trackHeight: 4,
                  ),
                  child: Slider(
                    value: _threshold,
                    min: 0,
                    max: 100,
                    onChanged: (v) => setState(() => _threshold = v),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _modelToggle() {
    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: Colors.black.withValues(alpha: 0.4),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: List.generate(2, (i) {
          final labels = ['Ensemble', 'Base'];
          final active = _modelIndex == i;
          return GestureDetector(
            onTap: () => setState(() => _modelIndex = i),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: active ? AppColors.primary : Colors.transparent,
                borderRadius: BorderRadius.circular(999),
              ),
              child: Text(
                labels[i],
                style: AppText.labelSm.copyWith(
                  color: active ? context.colors.background : context.colors.textMuted,
                  fontWeight: active ? FontWeight.w700 : FontWeight.w500,
                ),
              ),
            ),
          );
        }),
      ),
    );
  }

  Widget _prefRow({required String title, required String subtitle, required Widget trailing}) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: AppText.bodyMd.copyWith(
                      color: context.colors.onBackground,
                      fontWeight: FontWeight.w700,
                      fontSize: 15,
                    )),
                Text(subtitle,
                    style: AppText.labelSm.copyWith(
                      color: context.colors.textMuted.withValues(alpha: 0.7),
                    )),
              ],
            ),
          ),
          trailing,
        ],
      ),
    );
  }

  Widget _divider() {
    return Container(height: 1, color: Colors.white.withValues(alpha: 0.05));
  }

  Widget _aboutCards() {
    return Row(
      children: [
        Expanded(child: _aboutCard(label: 'Accuracy', value: '98.11', unit: '%', icon: Icons.verified)),
        const SizedBox(width: 12),
        Expanded(child: _versionCard()),
      ],
    );
  }

  Widget _aboutCard({required String label, required String value, required String unit, required IconData icon}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: context.colors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Stack(
        children: [
          Positioned(
            top: 0,
            right: 0,
            child: Icon(icon, color: AppColors.primary.withValues(alpha: 0.3), size: 24),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label.toUpperCase(),
                  style: AppText.labelSm.copyWith(
                    color: context.colors.textMuted.withValues(alpha: 0.7),
                    fontSize: 11,
                    letterSpacing: 1,
                  )),
              const SizedBox(height: 8),
              Row(
                crossAxisAlignment: CrossAxisAlignment.baseline,
                textBaseline: TextBaseline.alphabetic,
                children: [
                  Text(value,
                      style: AppText.headlineLgMobile.copyWith(
                        color: context.colors.onBackground,
                        fontWeight: FontWeight.w700,
                        fontSize: 24,
                      )),
                  Text(unit,
                      style: AppText.labelSm.copyWith(
                        color: context.colors.textMuted.withValues(alpha: 0.5),
                      )),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _versionCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: context.colors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('VERSION',
              style: AppText.labelSm.copyWith(
                color: context.colors.textMuted.withValues(alpha: 0.7),
                fontSize: 11,
                letterSpacing: 1,
              )),
          const SizedBox(height: 8),
          Text('v1.4.2-stable',
              style: AppText.bodyMd.copyWith(
                color: context.colors.onBackground,
                fontWeight: FontWeight.w700,
              )),
          const SizedBox(height: 6),
          Row(
            children: [
              Container(
                width: 6,
                height: 6,
                decoration: const BoxDecoration(
                  color: AppColors.healthy,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 6),
              Text('Optimized',
                  style: AppText.labelSm.copyWith(
                    color: AppColors.healthy,
                    fontWeight: FontWeight.w700,
                  )),
            ],
          ),
        ],
      ),
    );
  }

  Widget _developerCredits() {
    return GestureDetector(
      onTap: () {},
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: context.colors.surface,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
        ),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Developer Credits',
                      style: AppText.bodyMd.copyWith(
                        color: context.colors.onBackground,
                        fontWeight: FontWeight.w700,
                        fontSize: 15,
                      )),
                  const SizedBox(height: 2),
                  Text(
                    '"Preserving the Great Barrier through Neural Intelligence"',
                    style: AppText.labelSm.copyWith(
                      color: context.colors.textMuted,
                      fontStyle: FontStyle.italic,
                      fontSize: 11,
                    ),
                  ),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: context.colors.textMuted),
          ],
        ),
      ),
    );
  }
}
