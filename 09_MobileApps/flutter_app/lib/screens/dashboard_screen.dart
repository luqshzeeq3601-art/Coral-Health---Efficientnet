import 'package:flutter/material.dart';

import '../theme.dart';
import '../services/weather_service.dart';

const _heroImageUrl =
    'https://lh3.googleusercontent.com/aida-public/AB6AXuDmOD1OHucMrra_AxLjJx_4eOvMIFLDC6dhDtmJoByKE0KUo8ERZT9jWF250dvhNtLpy-kSU6PbwzaI7hkZn7lGZrrwcSBHjOOIhN824IGhab499iyPa1ZpGkHvqDEgoSVowPhaJYTMl-MUCyt5b-O36qyqOr2yxgtpp8B-OnFtpP6ZTuwFk763wtEvvaHmXu2ikHqCwkSz1GH_my3fxIIR3f5o1Ty_dQw7hbZUNpI2s7uWyPlTVz-m43eYSdRYHxjddz_6gkuy32uZ';

const _featuredCoralUrl =
    'https://lh3.googleusercontent.com/aida-public/AB6AXuBkH_TRZ0rQo6KrWtodQdhh9BU6qkJnUF8OOL2Hu3GFX0MfuufqBupKhIutcimgFMCfQFI0qKCLj4shii0tOzZws-V24Z9QtpG0gNjDMkwsVETKlPhxYA4IXxs_A_Y7LKDqvITf6OoK2kh_1LG7w3prwBP9URijCt6QazSXh7pUH10zZs7ZS0YQhxO7jL7PsAiLGtRO7gvh_pOr4vU4QIRockpYiaVWDWgrbT4vq-m95Z2W3ozTgUGofwufQKBpbg9ciWyCA7NV8J0Z';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _filter = 0;
  static const _filters = ['All', 'Healthy', 'Bleached', 'Dead'];

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      bottom: false,
      child: Column(
        children: [
          const _TopAppBar(),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.fromLTRB(24, 16, 24, 110),
              children: [
                _WelcomeSection(),
                const SizedBox(height: 24),
                const _HeroAssessmentCard(),
                const SizedBox(height: 32),
                _SectionHeader(title: 'Model Performance', onSeeAll: () {}),
                const SizedBox(height: 16),
                const _MetricGrid(),
                const SizedBox(height: 32),
                _SectionHeader(title: 'Coral Classes', onSeeAll: () {}),
                const SizedBox(height: 16),
                _FilterPills(
                  items: _filters,
                  selectedIndex: _filter,
                  onChanged: (i) => setState(() => _filter = i),
                ),
                const SizedBox(height: 16),
                const _FeaturedCoralCard(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _TopAppBar extends StatelessWidget {
  const _TopAppBar();

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 64,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      color: context.colors.background.withValues(alpha: 0.9),
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
              color: context.colors.surfaceElevated,
              shape: BoxShape.circle,
              border: Border.all(color: context.colors.surfaceElevated, width: 2),
            ),
            child: const Icon(
              Icons.account_circle,
              color: context.colors.textMuted,
              size: 32,
            ),
          ),
        ],
      ),
    );
  }
}

class _WelcomeSection extends StatefulWidget {
  @override
  State<_WelcomeSection> createState() => _WelcomeSectionState();
}

class _WelcomeSectionState extends State<_WelcomeSection> {
  WeatherData? _weather;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadWeather();
  }

  Future<void> _loadWeather() async {
    final data = await WeatherService.fetch();
    if (mounted) setState(() { _weather = data; _loading = false; });
  }

  Color _uvColor(String label) {
    switch (label) {
      case 'LOW': return AppColors.healthy;
      case 'MODERATE': return AppColors.bleached;
      case 'HIGH': return AppColors.bleached;
      default: return AppColors.dead;
    }
  }

  @override
  Widget build(BuildContext context) {
    final tempText = _loading
        ? '...'
        : _weather == null
            ? '--'
            : '${_weather!.temperature.toStringAsFixed(1)}°C';

    final uvLabel = _loading
        ? '...'
        : _weather == null
            ? '--'
            : WeatherService.uvLabel(_weather!.uvIndex);

    final uvColor = _loading || _weather == null ? context.colors.textMuted : _uvColor(uvLabel);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Welcome Back! 👋',
          style: AppText.headlineLgMobile.copyWith(color: context.colors.onBackground),
        ),
        const SizedBox(height: 4),
        Text(
          '3 classes · 159 test samples · 98.11% accuracy',
          style: AppText.labelSm.copyWith(color: context.colors.textMuted),
        ),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: Colors.white.withValues(alpha: 0.05),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.thermostat, size: 14, color: AppColors.primary),
              const SizedBox(width: 6),
              _statText('Temp: ', tempText, context.colors.onBackground),
              const SizedBox(width: 12),
              Container(width: 1, height: 12, color: Colors.white12),
              const SizedBox(width: 12),
              const Icon(Icons.wb_sunny, size: 14, color: AppColors.bleached),
              const SizedBox(width: 6),
              _statText('UV Index: ', uvLabel, uvColor),
            ],
          ),
        ),
      ],
    );
  }

  Widget _statText(String label, String value, Color valueColor) {
    return Text.rich(
      TextSpan(
        style: AppText.labelSm.copyWith(
          fontSize: 11,
          color: context.colors.onBackground,
          letterSpacing: 0.5,
        ),
        children: [
          TextSpan(text: label.toUpperCase()),
          TextSpan(
            text: value,
            style: TextStyle(color: valueColor, fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }
}

class _HeroAssessmentCard extends StatelessWidget {
  const _HeroAssessmentCard();

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(24),
      child: Container(
        height: 260,
        decoration: BoxDecoration(
          image: const DecorationImage(
            image: NetworkImage(_heroImageUrl),
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
          children: [
            const DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [Color(0x1A0E0E0E), Color(0xF20E0E0E)],
                ),
              ),
              child: SizedBox.expand(),
            ),
            Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: AppColors.bleached,
                          borderRadius: BorderRadius.circular(999),
                          border: Border.all(color: Colors.white24),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Container(
                              width: 6,
                              height: 6,
                              decoration: const BoxDecoration(
                                color: AppColors.onTertiary,
                                shape: BoxShape.circle,
                              ),
                            ),
                            const SizedBox(width: 6),
                            Text(
                              'BLEACHED',
                              style: AppText.labelSm.copyWith(
                                fontSize: 11,
                                color: AppColors.onTertiary,
                                fontWeight: FontWeight.w700,
                                letterSpacing: 1,
                              ),
                            ),
                          ],
                        ),
                      ),
                      Text(
                        'Oct 21, 2025 · 14:32',
                        style: AppText.labelSm.copyWith(color: Colors.white60),
                      ),
                    ],
                  ),
                  const Spacer(),
                  Text(
                    'Last Assessment',
                    style: AppText.titleMd.copyWith(
                      color: Colors.white.withValues(alpha: 0.8),
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    '87%',
                    style: AppText.metricXl.copyWith(color: AppColors.primary),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      SizedBox(
                        width: 80,
                        child: Text(
                          'Confidence',
                          style: AppText.labelSm.copyWith(
                            color: Colors.white54,
                          ),
                        ),
                      ),
                      Expanded(
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(999),
                          child: Stack(
                            children: [
                              Container(height: 4, color: Colors.white12),
                              FractionallySizedBox(
                                widthFactor: 0.87,
                                child: Container(
                                  height: 4,
                                  decoration: BoxDecoration(
                                    color: AppColors.primary,
                                    borderRadius: BorderRadius.circular(999),
                                    boxShadow: const [
                                      BoxShadow(
                                        color: Color(0x9900F5D4),
                                        blurRadius: 8,
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    decoration: BoxDecoration(
                      color: Colors.white.withValues(alpha: 0.1),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(
                          Icons.ios_share,
                          color: Colors.white,
                          size: 18,
                        ),
                        const SizedBox(width: 8),
                        Text(
                          'Export Report & Alert',
                          style: AppText.labelSm.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.w600,
                            letterSpacing: 0.5,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({required this.title, required this.onSeeAll});
  final String title;
  final VoidCallback onSeeAll;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Text(
            title,
            style: AppText.titleMd.copyWith(color: context.colors.onBackground),
          ),
          GestureDetector(
            onTap: onSeeAll,
            child: Text(
              'See All',
              style: AppText.labelSm.copyWith(color: AppColors.primary),
            ),
          ),
        ],
      ),
    );
  }
}

class _MetricGrid extends StatelessWidget {
  const _MetricGrid();

  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(
                child: SizedBox(
                  height: 120,
                  child: _MetricCard(
                    label: 'Test Accuracy',
                    value: '98.11%',
                    icon: Icons.speed,
                    valueColor: AppColors.primary,
                  ),
                ),
              ),
              SizedBox(width: 20),
              Expanded(
                child: SizedBox(
                  height: 120,
                  child: _MetricCard(
                    label: 'Inference',
                    value: '10ms',
                    icon: Icons.timer,
                  ),
                ),
              ),
            ],
          ),
        ),
        SizedBox(height: 20),
        IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(
                child: SizedBox(
                  height: 120,
                  child: _MetricCard(
                    label: 'Total Scans',
                    value: '7',
                    unit: 'Images',
                    icon: Icons.folder_open,
                  ),
                ),
              ),
              SizedBox(width: 20),
              Expanded(child: SizedBox(height: 120, child: _SparklineCard())),
            ],
          ),
        ),
      ],
    );
  }
}

class _MetricCard extends StatelessWidget {
  const _MetricCard({
    required this.label,
    required this.value,
    required this.icon,
    this.unit,
    this.valueColor,
  });
  final String label;
  final String value;
  final String? unit;
  final IconData icon;
  final Color? valueColor;

  @override
  Widget build(BuildContext context) {
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
            child: Icon(
              icon,
              size: 20,
              color: (valueColor ?? context.colors.onBackground).withValues(
                alpha: valueColor != null ? 0.2 : 0.1,
              ),
            ),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                label,
                style: AppText.labelSm.copyWith(color: context.colors.textMuted),
              ),
              Row(
                crossAxisAlignment: CrossAxisAlignment.baseline,
                textBaseline: TextBaseline.alphabetic,
                children: [
                  Flexible(
                    child: FittedBox(
                      fit: BoxFit.scaleDown,
                      alignment: Alignment.centerLeft,
                      child: Text(
                        value,
                        style: AppText.display.copyWith(
                          color: valueColor ?? context.colors.onBackground,
                        ),
                      ),
                    ),
                  ),
                  if (unit != null) ...[
                    const SizedBox(width: 4),
                    Text(
                      unit!,
                      style: AppText.metricUnit.copyWith(
                        color: context.colors.textMuted,
                      ),
                    ),
                  ],
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _SparklineCard extends StatelessWidget {
  const _SparklineCard();

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: context.colors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            '30-DAY HEALTH TREND',
            style: AppText.labelSm.copyWith(
              fontSize: 11,
              color: context.colors.textMuted,
              letterSpacing: 1,
            ),
          ),
          SizedBox(
            height: 48,
            width: double.infinity,
            child: CustomPaint(painter: _SparklinePainter()),
          ),
        ],
      ),
    );
  }
}

class _SparklinePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final pts = <Offset>[];
    final ys = [35.0, 15, 25, 10, 30, 5, 20];
    for (var i = 0; i < ys.length; i++) {
      pts.add(
        Offset(i / (ys.length - 1) * size.width, ys[i] / 40 * size.height),
      );
    }
    final path = Path()..moveTo(pts.first.dx, pts.first.dy);
    for (var i = 1; i < pts.length; i++) {
      final prev = pts[i - 1];
      final curr = pts[i];
      final mid = Offset((prev.dx + curr.dx) / 2, (prev.dy + curr.dy) / 2);
      path.quadraticBezierTo(prev.dx, prev.dy, mid.dx, mid.dy);
    }
    path.lineTo(pts.last.dx, pts.last.dy);

    final fillPath = Path.from(path)
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();
    final fillPaint = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [Color(0x3300F5D4), Color(0x0000F5D4)],
      ).createShader(Offset.zero & size);
    canvas.drawPath(fillPath, fillPaint);

    final stroke = Paint()
      ..color = AppColors.primary
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2
      ..strokeCap = StrokeCap.round;
    canvas.drawPath(path, stroke);
  }

  @override
  bool shouldRepaint(covariant CustomPainter old) => false;
}

class _FilterPills extends StatelessWidget {
  const _FilterPills({
    required this.items,
    required this.selectedIndex,
    required this.onChanged,
  });
  final List<String> items;
  final int selectedIndex;
  final ValueChanged<int> onChanged;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 36,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: items.length,
        separatorBuilder: (_, _) => const SizedBox(width: 8),
        itemBuilder: (_, i) {
          final active = i == selectedIndex;
          return GestureDetector(
            onTap: () => onChanged(i),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              padding: const EdgeInsets.symmetric(horizontal: 24),
              alignment: Alignment.center,
              decoration: BoxDecoration(
                gradient: active
                    ? const LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [AppColors.primary, context.colors.primaryFixedDim],
                      )
                    : null,
                color: active ? null : Colors.white.withValues(alpha: 0.05),
                borderRadius: BorderRadius.circular(999),
                boxShadow: active
                    ? const [
                        BoxShadow(color: Color(0x3300F5D4), blurRadius: 12),
                      ]
                    : null,
              ),
              child: Text(
                items[i],
                style: AppText.labelSm.copyWith(
                  color: active ? context.colors.onPrimary : context.colors.onBackground,
                  fontWeight: active ? FontWeight.w700 : FontWeight.w500,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _FeaturedCoralCard extends StatelessWidget {
  const _FeaturedCoralCard();

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(20),
      child: Container(
        height: 180,
        decoration: BoxDecoration(
          color: context.colors.surface,
          image: const DecorationImage(
            image: NetworkImage(_featuredCoralUrl),
            fit: BoxFit.cover,
          ),
          border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
        ),
        child: Stack(
          children: [
            const DecoratedBox(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.bottomCenter,
                  end: Alignment.topCenter,
                  colors: [
                    context.colors.surfaceContainerLowest,
                    Color(0x990E0E0E),
                    Colors.transparent,
                  ],
                ),
              ),
              child: SizedBox.expand(),
            ),
            Positioned(
              left: 20,
              right: 20,
              bottom: 20,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Row(
                    children: [
                      Container(
                        width: 8,
                        height: 8,
                        decoration: const BoxDecoration(
                          color: AppColors.healthy,
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(color: Color(0x994ADE80), blurRadius: 8),
                          ],
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'Acropora Cervicornis',
                        style: AppText.headlineLgMobile.copyWith(
                          color: context.colors.onBackground,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Healthy staghorn coral specimen exhibiting normal growth patterns and strong pigmentation across all branches.',
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: AppText.labelSm.copyWith(color: context.colors.textMuted),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

