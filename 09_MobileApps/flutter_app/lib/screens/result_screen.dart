import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../theme.dart';

const _heroImageUrl =
    'https://lh3.googleusercontent.com/aida-public/AB6AXuA1rds56htsgdzveygsHbxCiWDN2-knMkcZjHznyo3MGzC4MoN7QZglE_18Ef_PTCWzn654Pehiogt5s8hzZJXLlE7lzrzRXgzkP0eI7D5SSQFpGutPUW8OMsgcIorR35mxy_PMbUWBCOZn8N8zExIt7SW7SoqcaK_TjRMFDxEytzoxqNVTETrxPqmAfgOMLRo_F_hrcbJmvd3GuyoilQ23zG0pDHa1Y4BGXeuZDN3BROE81KmOHNdi1zMQ8cVYXCSuKoioPczTdytK';

class ResultScreen extends StatefulWidget {
  const ResultScreen({super.key});

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> {
  int _gradTab = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.colors.background,
      appBar: AppBar(
        backgroundColor: context.colors.background.withValues(alpha: 0.8),
        elevation: 0,
        scrolledUnderElevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.of(context).pop(),
        ),
        centerTitle: true,
        title: Text(
          'Assessment Result',
          style: AppText.titleMd.copyWith(color: Colors.white, fontSize: 17),
        ),
        shape: const Border(bottom: BorderSide(color: Colors.white12, width: 1)),
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 16, 16, 32),
        children: [
          _heroCard(),
          const SizedBox(height: 24),
          _gradCamSection(),
          const SizedBox(height: 24),
          _classProbabilitiesSection(),
          const SizedBox(height: 24),
          _recommendationCard(),
          const SizedBox(height: 16),
          _modelInfoChip(),
          const SizedBox(height: 16),
          _actionGrid(),
        ],
      ),
    );
  }

  Widget _heroCard() {
    return ClipRRect(
      borderRadius: BorderRadius.circular(28),
      child: Container(
        height: 224,
        decoration: const BoxDecoration(
          image: DecorationImage(
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
                  colors: [Colors.transparent, Color(0x66000000), Color(0xFF000000)],
                ),
              ),
              child: SizedBox.expand(),
            ),
            Padding(
              padding: const EdgeInsets.all(24),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.black.withValues(alpha: 0.4),
                            borderRadius: BorderRadius.circular(999),
                            border: Border.all(color: AppColors.healthy.withValues(alpha: 0.3)),
                          ),
                          child: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Container(
                                width: 8,
                                height: 8,
                                decoration: const BoxDecoration(
                                  color: AppColors.healthy,
                                  shape: BoxShape.circle,
                                ),
                              ),
                              const SizedBox(width: 6),
                              Text(
                                'HEALTHY',
                                style: AppText.labelSm.copyWith(
                                  color: AppColors.healthy,
                                  fontSize: 11,
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: 1.5,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(height: 12),
                        Text('Classification:',
                            style: AppText.headlineLgMobile.copyWith(
                              color: Colors.white,
                              fontWeight: FontWeight.w700,
                              fontSize: 22,
                            )),
                        Text('Healthy',
                            style: AppText.headlineLgMobile.copyWith(
                              color: AppColors.healthy,
                              fontWeight: FontWeight.w700,
                              fontSize: 22,
                            )),
                        const SizedBox(height: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(999),
                            border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
                          ),
                          child: Text(
                            'Species: Acropora cervicornis (88%)',
                            style: AppText.labelSm.copyWith(
                              color: AppColors.primary.withValues(alpha: 0.8),
                              fontSize: 10,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 12),
                  SizedBox(
                    width: 96,
                    height: 96,
                    child: CustomPaint(
                      painter: _ConfidenceRingPainter(value: 0.92),
                      child: Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text('92',
                                style: AppText.headlineLgMobile.copyWith(
                                  color: Colors.white,
                                  fontWeight: FontWeight.w700,
                                  fontSize: 28,
                                  height: 1,
                                )),
                            Text('% AI',
                                style: AppText.labelSm.copyWith(
                                  color: AppColors.primary,
                                  fontSize: 9,
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: -0.5,
                                )),
                          ],
                        ),
                      ),
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

  Widget _gradCamSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.visibility, size: 18, color: AppColors.primary),
            const SizedBox(width: 8),
            Text('Grad-CAM Viewer',
                style: AppText.titleMd.copyWith(color: Colors.white, fontSize: 15)),
          ],
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: context.colors.surface,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: context.colors.divider),
          ),
          child: Column(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Container(
                  height: 220,
                  decoration: const BoxDecoration(
                    image: DecorationImage(
                      image: NetworkImage(_heroImageUrl),
                      fit: BoxFit.cover,
                    ),
                  ),
                  child: Stack(
                    children: [
                      Positioned(
                        top: 12,
                        left: 12,
                        child: _tag('ORIGINAL', Colors.black.withValues(alpha: 0.6), Colors.white),
                      ),
                      Positioned(
                        top: 12,
                        right: 12,
                        child: _tag('OVERLAY', AppColors.primary.withValues(alpha: 0.2), AppColors.primary),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.05),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: Row(
                  children: List.generate(3, (i) {
                    final labels = ['Original', 'Overlay', 'Heatmap'];
                    final active = _gradTab == i;
                    return Expanded(
                      child: GestureDetector(
                        behavior: HitTestBehavior.opaque,
                        onTap: () => setState(() => _gradTab = i),
                        child: Container(
                          padding: const EdgeInsets.symmetric(vertical: 8),
                          decoration: BoxDecoration(
                            color: active ? AppColors.primary : Colors.transparent,
                            borderRadius: BorderRadius.circular(999),
                          ),
                          child: Center(
                            child: Text(
                              labels[i],
                              style: AppText.labelSm.copyWith(
                                color: active ? Colors.black : Colors.white.withValues(alpha: 0.4),
                                fontWeight: active ? FontWeight.w700 : FontWeight.w500,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        ),
                      ),
                    );
                  }),
                ),
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('Low Activation',
                      style: AppText.labelSm.copyWith(
                        color: Colors.white.withValues(alpha: 0.4),
                        fontSize: 10,
                        letterSpacing: -0.3,
                      )),
                  Text('High Activation',
                      style: AppText.labelSm.copyWith(
                        color: Colors.white.withValues(alpha: 0.4),
                        fontSize: 10,
                        letterSpacing: -0.3,
                      )),
                ],
              ),
              const SizedBox(height: 4),
              Container(
                height: 8,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(999),
                  gradient: const LinearGradient(
                    colors: [
                      Color(0xFF2563EB),
                      Color(0xFF4ADE80),
                      Color(0xFFFACC15),
                      Color(0xFFDC2626),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _tag(String text, Color bg, Color fg) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
      ),
      child: Text(text,
          style: AppText.labelSm.copyWith(
            color: fg,
            fontSize: 10,
            fontWeight: FontWeight.w700,
            letterSpacing: 1,
          )),
    );
  }

  Widget _classProbabilitiesSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.list_alt, size: 18, color: Color(0xFFD7FFF3)),
            const SizedBox(width: 8),
            Text('Class Probabilities',
                style: AppText.titleMd.copyWith(color: Colors.white, fontSize: 15)),
          ],
        ),
        const SizedBox(height: 12),
        _probabilityRow('Healthy', 92.4, AppColors.healthy, Icons.eco),
        const SizedBox(height: 8),
        _probabilityRow('Bleached', 6.2, AppColors.bleached, Icons.wb_sunny),
        const SizedBox(height: 8),
        _probabilityRow('Dead', 1.4, AppColors.dead, Icons.warning),
      ],
    );
  }

  Widget _probabilityRow(String label, double value, Color color, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: context.colors.surface.withValues(alpha: 0.6),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: color.withValues(alpha: 0.2)),
            ),
            child: Icon(icon, color: color, size: 20),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(label,
                        style: AppText.bodyMd.copyWith(
                          color: Colors.white.withValues(alpha: 0.9),
                          fontWeight: FontWeight.w600,
                        )),
                    Text('${value.toStringAsFixed(1)}%',
                        style: AppText.titleMd.copyWith(
                          color: color,
                          fontWeight: FontWeight.w700,
                          fontSize: 16,
                        )),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(999),
                  child: Stack(
                    children: [
                      Container(
                        height: 10,
                        color: Colors.white.withValues(alpha: 0.05),
                      ),
                      FractionallySizedBox(
                        widthFactor: value / 100,
                        child: Container(
                          height: 10,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [color, color.withValues(alpha: 0.6)],
                            ),
                            borderRadius: BorderRadius.circular(999),
                            boxShadow: [
                              BoxShadow(
                                color: color.withValues(alpha: 0.5),
                                blurRadius: 8,
                              ),
                            ],
                          ),
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
    );
  }

  Widget _recommendationCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: context.colors.surface.withValues(alpha: 0.6),
        borderRadius: BorderRadius.circular(24),
        border: const Border(left: BorderSide(color: AppColors.healthy, width: 4)),
      ),
      child: Stack(
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('RECOMMENDATION',
                  style: AppText.labelSm.copyWith(
                    color: AppColors.primary,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.5,
                    fontSize: 12,
                  )),
              const SizedBox(height: 8),
              Padding(
                padding: const EdgeInsets.only(right: 24),
                child: Text(
                  'Coral appears healthy with vibrant pigmentation and full polyp extension. Continue routine monitoring. No immediate bleaching threat detected.',
                  style: AppText.bodyMd.copyWith(
                    color: Colors.white.withValues(alpha: 0.8),
                    fontSize: 14,
                    height: 1.5,
                  ),
                ),
              ),
            ],
          ),
          Positioned(
            top: 0,
            right: 0,
            child: Icon(Icons.copy,
                size: 20, color: Colors.white.withValues(alpha: 0.3)),
          ),
        ],
      ),
    );
  }

  Widget _modelInfoChip() {
    return Center(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.05),
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('EfficientNetB0 SWA · 5-seed Ensemble · 10 ms',
                style: AppText.labelSm.copyWith(
                  color: context.colors.textMuted,
                  fontSize: 10,
                  letterSpacing: 1,
                )),
            const SizedBox(width: 6),
            Icon(Icons.info_outline,
                size: 14, color: Colors.white.withValues(alpha: 0.3)),
          ],
        ),
      ),
    );
  }

  Widget _actionGrid() {
    return Row(
      children: [
        Expanded(child: _actionBtn(Icons.favorite, 'SAVE', AppColors.primary, true)),
        const SizedBox(width: 12),
        Expanded(child: _actionBtn(Icons.share, 'SHARE', Colors.white, false)),
        const SizedBox(width: 12),
        Expanded(child: _actionBtn(Icons.refresh, 'RETRY', Colors.white, false)),
      ],
    );
  }

  Widget _actionBtn(IconData icon, String label, Color color, bool emphasis) {
    return Container(
      height: 48,
      decoration: BoxDecoration(
        color: emphasis ? AppColors.primary.withValues(alpha: 0.2) : Colors.white.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: emphasis ? AppColors.primary.withValues(alpha: 0.3) : Colors.white.withValues(alpha: 0.1),
        ),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(height: 2),
          Text(label,
              style: AppText.labelSm.copyWith(
                color: color.withValues(alpha: emphasis ? 1.0 : 0.8),
                fontSize: 10,
                fontWeight: FontWeight.w700,
                letterSpacing: -0.3,
              )),
        ],
      ),
    );
  }
}

class _ConfidenceRingPainter extends CustomPainter {
  _ConfidenceRingPainter({required this.value});
  final double value;

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.width / 2 - 6;
    final track = Paint()
      ..color = Colors.white.withValues(alpha: 0.1)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 8
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(center, radius, track);

    final progress = Paint()
      ..shader = const LinearGradient(
        colors: [AppColors.primary, AppColors.healthy],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ).createShader(Rect.fromCircle(center: center, radius: radius))
      ..style = PaintingStyle.stroke
      ..strokeWidth = 8
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -math.pi / 2,
      2 * math.pi * value,
      false,
      progress,
    );
  }

  @override
  bool shouldRepaint(covariant _ConfidenceRingPainter old) => old.value != value;
}
