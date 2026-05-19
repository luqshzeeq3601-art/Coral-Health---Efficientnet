import 'dart:math';

import 'package:flutter/material.dart';

class ConfidenceRing extends StatelessWidget {
  const ConfidenceRing({super.key, required this.value, required this.color});

  final double value;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0, end: value.clamp(0, 100)),
      duration: const Duration(milliseconds: 900),
      curve: Curves.easeOutCubic,
      builder: (context, animatedValue, _) {
        return SizedBox(
          width: 172,
          height: 172,
          child: CustomPaint(
            painter: _RingPainter(
              progress: animatedValue / 100,
              color: color,
              trackColor: Theme.of(context).colorScheme.outlineVariant,
            ),
            child: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    '${animatedValue.toStringAsFixed(1)}%',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Confidence',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}

class _RingPainter extends CustomPainter {
  const _RingPainter({
    required this.progress,
    required this.color,
    required this.trackColor,
  });

  final double progress;
  final Color color;
  final Color trackColor;

  @override
  void paint(Canvas canvas, Size size) {
    const stroke = 16.0;
    final center = size.center(Offset.zero);
    final rect = Rect.fromCircle(
      center: center,
      radius: (size.width - stroke) / 2,
    );

    final trackPaint = Paint()
      ..color = trackColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = stroke
      ..strokeCap = StrokeCap.round;

    final activePaint = Paint()
      ..shader = SweepGradient(
        colors: [color.withValues(alpha: 0.32), color],
        startAngle: -pi / 2,
        endAngle: 3 * pi / 2,
      ).createShader(rect)
      ..style = PaintingStyle.stroke
      ..strokeWidth = stroke
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(rect, 0, 2 * pi, false, trackPaint);
    canvas.drawArc(rect, -pi / 2, 2 * pi * progress, false, activePaint);
  }

  @override
  bool shouldRepaint(covariant _RingPainter oldDelegate) {
    return oldDelegate.progress != progress ||
        oldDelegate.color != color ||
        oldDelegate.trackColor != trackColor;
  }
}
