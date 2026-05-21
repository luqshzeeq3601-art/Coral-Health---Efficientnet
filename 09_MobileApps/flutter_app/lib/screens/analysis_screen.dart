import 'package:flutter/material.dart';
import '../theme.dart';
import 'result_screen.dart';

class AnalysisScreen extends StatefulWidget {
  const AnalysisScreen({super.key});

  @override
  State<AnalysisScreen> createState() => _AnalysisScreenState();
}

class _AnalysisScreenState extends State<AnalysisScreen> {
  int _modelIndex = 0;
  bool _gradcam = false;
  bool _hasImage = false;

  @override
  Widget build(BuildContext context) {
    final modelLabels = ['Ensemble', 'Base'];
    return SafeArea(
      bottom: false,
      child: Column(
        children: [
          _TopBar(),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(24, 16, 24, 110),
              children: [
                _datePill(),
                const SizedBox(height: 20),
                _actionCards(),
                const SizedBox(height: 20),
                _imagePreview(),
                const SizedBox(height: 20),
                _modelSelector(modelLabels),
                const SizedBox(height: 20),
                _gradcamRow(),
                const SizedBox(height: 20),
                _analyzeButton(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _datePill() {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: const Color(0xFF1C1B1B),
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: context.colors.divider),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.calendar_today, size: 18, color: context.colors.textMuted),
            const SizedBox(width: 8),
            Text('October 24, 2023',
                style: AppText.labelSm.copyWith(color: context.colors.textMuted)),
            const SizedBox(width: 8),
            const Icon(Icons.expand_more, size: 16, color: context.colors.textMuted),
          ],
        ),
      ),
    );
  }

  Widget _actionCards() {
    return Row(
      children: [
        Expanded(child: _actionCard(Icons.photo_camera, 'Take Photo', () { setState(() => _hasImage = true); })),
        const SizedBox(width: 20),
        Expanded(child: _actionCard(Icons.collections, 'From Gallery', () { setState(() => _hasImage = true); })),
      ],
    );
  }

  Widget _actionCard(IconData icon, String label, VoidCallback onTap) {
    return InkWell(
      borderRadius: BorderRadius.circular(20),
      onTap: onTap,
      child: Container(
        height: 110,
        decoration: BoxDecoration(
          color: context.colors.surfaceElevated,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 32, color: AppColors.primary),
            const SizedBox(height: 8),
            Text(label, style: AppText.titleMd.copyWith(color: Colors.white)),
          ],
        ),
      ),
    );
  }

  Widget _imagePreview() {
    return AspectRatio(
      aspectRatio: 16 / 9,
      child: Container(
        decoration: BoxDecoration(
          color: context.colors.surfaceContainerLowest,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: AppColors.primary.withValues(alpha: 0.2)),
        ),
        child: _hasImage
            ? Center(
                child: Icon(Icons.image, size: 48, color: AppColors.primary),
              )
            : Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.water_drop, size: 48, color: AppColors.primary),
                  const SizedBox(height: 16),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 32),
                    child: Text(
                      'Upload or capture a reef image to begin',
                      textAlign: TextAlign.center,
                      style: AppText.bodyMd.copyWith(color: context.colors.textMuted),
                    ),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _modelSelector(List<String> labels) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('AI ANALYSIS MODEL',
            style: AppText.labelSm.copyWith(
              color: context.colors.textMuted,
              fontSize: 14,
              fontWeight: FontWeight.w600,
            )),
        const SizedBox(height: 12),
        Container(
          height: 56,
          padding: const EdgeInsets.all(4),
          decoration: BoxDecoration(
            color: context.colors.surfaceElevated,
            borderRadius: BorderRadius.circular(999),
          ),
          child: Stack(
            children: [
              AnimatedAlign(
                duration: const Duration(milliseconds: 250),
                alignment: _modelIndex == 0 ? Alignment.centerLeft : Alignment.centerRight,
                child: FractionallySizedBox(
                  widthFactor: 0.5,
                  heightFactor: 1,
                  child: Container(
                    decoration: BoxDecoration(
                      color: AppColors.primary,
                      borderRadius: BorderRadius.circular(999),
                    ),
                  ),
                ),
              ),
              Row(
                children: List.generate(labels.length, (i) {
                  final active = _modelIndex == i;
                  return Expanded(
                    child: GestureDetector(
                      onTap: () => setState(() => _modelIndex = i),
                      behavior: HitTestBehavior.opaque,
                      child: Center(
                        child: Text(
                          labels[i],
                          style: AppText.titleMd.copyWith(
                            color: active ? context.colors.onPrimary : context.colors.textMuted,
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                    ),
                  );
                }),
              ),
            ],
          ),
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Text(
            'Ensemble model uses multi-spectral validation for 98.4% accuracy.',
            textAlign: TextAlign.center,
            style: AppText.labelSm.copyWith(color: context.colors.textMuted, fontSize: 12),
          ),
        ),
      ],
    );
  }

  Widget _gradcamRow() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: context.colors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: context.colors.divider),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Grad-CAM Visualisation',
                    style: AppText.titleMd.copyWith(color: Colors.white, fontSize: 16)),
                const SizedBox(height: 2),
                Text('Show heatmap overlay on result',
                    style: AppText.bodyMd.copyWith(color: context.colors.textMuted, fontSize: 12)),
              ],
            ),
          ),
          Switch(
            value: _gradcam,
            onChanged: (v) => setState(() => _gradcam = v),
            activeThumbColor: context.colors.onPrimary,
            activeTrackColor: AppColors.primary,
            inactiveThumbColor: context.colors.textMuted,
            inactiveTrackColor: context.colors.surfaceElevated,
          ),
        ],
      ),
    );
  }

  Widget _analyzeButton() {
    final enabled = _hasImage;
    return GestureDetector(
      onTap: enabled
          ? () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const ResultScreen()),
              )
          : null,
      child: Container(
        height: 60,
        decoration: BoxDecoration(
          color: enabled ? AppColors.primary : context.colors.surfaceElevated,
          borderRadius: BorderRadius.circular(999),
          boxShadow: enabled
              ? [
                  BoxShadow(
                    color: AppColors.primary.withValues(alpha: 0.4),
                    blurRadius: 15,
                  ),
                ]
              : null,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Analyze',
              style: AppText.headlineLgMobile.copyWith(
                color: enabled ? context.colors.background : context.colors.textMuted,
                fontSize: 22,
                fontWeight: FontWeight.w700,
              ),
            ),
            const SizedBox(width: 12),
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: enabled ? context.colors.background : Colors.transparent,
                shape: BoxShape.circle,
              ),
              child: Icon(Icons.psychology,
                  color: enabled ? AppColors.primary : context.colors.textMuted,
                  size: 24),
            ),
          ],
        ),
      ),
    );
  }
}

class _TopBar extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      height: 64,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      color: context.colors.background,
      child: Row(
        children: [
          const Icon(Icons.coronavirus, color: AppColors.primary, size: 28),
          const SizedBox(width: 8),
          Text(
            'Coral AI',
            style: AppText.headlineLgMobile.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.w700,
            ),
          ),
          const Spacer(),
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: context.colors.surfaceContainer,
              shape: BoxShape.circle,
              border: Border.all(color: context.colors.divider),
            ),
            child: const Icon(Icons.account_circle,
                color: context.colors.textMuted, size: 32),
          ),
        ],
      ),
    );
  }
}
