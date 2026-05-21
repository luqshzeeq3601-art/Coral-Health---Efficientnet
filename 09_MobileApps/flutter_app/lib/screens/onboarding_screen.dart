import 'dart:math';
import 'package:flutter/material.dart';

import '../theme.dart';
import 'main_shell.dart';

const _heroImageUrl =
    'https://lh3.googleusercontent.com/aida-public/AB6AXuDM6h4BWqpDJdAEns3Gboo5nkdzdhED5KKwY6kVGf9AlVq69xl722pUtGMbalDhFMzgPBymoga1iAgQKfdmz21yE_sf0X88Lot97PraI_CeNfZVfZ_NxkRuSs3Lh-96if5uI0Le2xHZeryG8q2_WquzKns66D-E0emOkUomEsbeYmOpNghWvVfzY3sac5EPEv6mXzNDm5of304E0P4-i3g4MnoLJ3w2Kg1JZPGCHkUA_T5tvOOoelgOXJzMnRdJxNl3TJlP7nDruk5p';

class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  final _particles = List<_Particle>.generate(20, (_) => _Particle.random());

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 15),
    )..repeat();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  void _onGetStarted() {
    Navigator.of(context).pushReplacement(
      PageRouteBuilder(
        transitionDuration: const Duration(milliseconds: 350),
        pageBuilder: (_, a, _) =>
            FadeTransition(opacity: a, child: const MainShell()),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: context.colors.background,
      body: Stack(
        fit: StackFit.expand,
        children: [
          Image.network(_heroImageUrl, fit: BoxFit.cover),
          const DecoratedBox(
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                stops: [0.30, 0.55, 1.0],
                colors: [
                  Colors.transparent,
                  Color(0xF20E0E0E),
                  Color(0xFF0E0E0E),
                ],
              ),
            ),
          ),
          AnimatedBuilder(
            animation: _ctrl,
            builder: (_, _) =>
                CustomPaint(painter: _ParticlePainter(_particles, _ctrl.value)),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: 24,
              ).copyWith(top: 24, bottom: 48),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(
                        Icons.coronavirus,
                        color: Colors.white,
                        size: 28,
                      ),
                      const SizedBox(width: 6),
                      Text(
                        'Coral AI',
                        style: AppText.headlineLgMobile.copyWith(
                          color: Colors.white,
                          fontSize: 22,
                          fontWeight: FontWeight.w700,
                          shadows: const [
                            Shadow(
                              color: Color(0x80000000),
                              offset: Offset(0, 2),
                              blurRadius: 4,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const Spacer(),
                  RichText(
                    textAlign: TextAlign.center,
                    text: TextSpan(
                      style: AppText.display.copyWith(
                        color: Colors.white,
                        fontSize: 28,
                        height: 36 / 28,
                      ),
                      children: [
                        const TextSpan(
                          text: 'Coral health made simple: your dive to ',
                        ),
                        TextSpan(
                          text: 'Conservation',
                          style: TextStyle(color: AppColors.primary),
                        ),
                        const TextSpan(text: ' and '),
                        TextSpan(
                          text: 'Discovery',
                          style: TextStyle(color: AppColors.primary),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    "Harness the power of AI to monitor marine vitality and protect the world's most vital ecosystems with scientific precision.",
                    textAlign: TextAlign.center,
                    style: AppText.bodyMd.copyWith(
                      color: const Color(0xFFD1D5DB),
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 28),
                  _GetStartedButton(onPressed: _onGetStarted),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _GetStartedButton extends StatefulWidget {
  const _GetStartedButton({required this.onPressed});
  final VoidCallback onPressed;

  @override
  State<_GetStartedButton> createState() => _GetStartedButtonState();
}

class _GetStartedButtonState extends State<_GetStartedButton> {
  bool _pressed = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) => setState(() => _pressed = true),
      onTapCancel: () => setState(() => _pressed = false),
      onTapUp: (_) => setState(() => _pressed = false),
      onTap: widget.onPressed,
      child: AnimatedScale(
        scale: _pressed ? 0.96 : 1,
        duration: const Duration(milliseconds: 120),
        child: Container(
          width: double.infinity,
          height: 56,
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: AppColors.primary,
            borderRadius: BorderRadius.circular(999),
            boxShadow: const [
              BoxShadow(
                color: Color(0x8000F5D4),
                blurRadius: 20,
                spreadRadius: 0,
              ),
            ],
          ),
          child: Text(
            'Get Started  →',
            style: AppText.titleMd.copyWith(
              color: const Color(0xFF0E0E0E),
              fontSize: 17,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ),
    );
  }
}

class _Particle {
  _Particle(this.x, this.size, this.delay, this.duration);
  final double x;
  final double size;
  final double delay;
  final double duration;

  factory _Particle.random() {
    final r = Random();
    return _Particle(
      r.nextDouble(),
      2 + r.nextDouble() * 4,
      r.nextDouble(),
      0.66 + r.nextDouble() * 0.33,
    );
  }
}

class _ParticlePainter extends CustomPainter {
  _ParticlePainter(this.particles, this.t);
  final List<_Particle> particles;
  final double t;

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..color = const Color(0x3300F5D4);
    for (final p in particles) {
      var phase = (t + p.delay) % p.duration / p.duration;
      final y = size.height - phase * (size.height + 60);
      double opacity = phase < 0.5 ? phase * 2 : (1 - phase) * 2;
      paint.color = Color.fromRGBO(0, 245, 212, 0.35 * opacity);
      canvas.drawCircle(Offset(p.x * size.width, y), p.size, paint);
    }
  }

  @override
  bool shouldRepaint(covariant _ParticlePainter old) => true;
}
