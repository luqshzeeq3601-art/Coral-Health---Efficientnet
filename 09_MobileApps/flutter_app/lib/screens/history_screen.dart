import 'package:flutter/material.dart';
import '../theme.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  int _range = 1;
  int _filter = 0;

  static const _ranges = ['Day', 'Week', 'Month'];
  static const _filters = ['All', 'Healthy', 'Bleached', 'Dead'];

  static final _items = [
    _SessionItem(
      title: 'Great Barrier Section A12',
      status: 'Healthy',
      statusColor: AppColors.healthy,
      confidence: 98.4,
      date: 'Nov 24, 2024 • 14:20',
      imageUrl:
          'https://lh3.googleusercontent.com/aida-public/AB6AXuCQ8YEq4178-Ow0We7WV3mRUpgOZgyheQsSoWjn2u-fuX83N09Phyke-WzKlzNygquxml8Yr30R_s1IdqCSv3vIlj7f-4WH4d6Tu1tt7z8u58PiZg3T4IeNBWh76V4JjW1MytTxJ9Xwxo9fxXIdLt0RucKdSHTWSJN75buIT9wPDtKS2Nl_7idEth1LnVknSXmSLYE-g8dSG7bUKaaMRRVquxBOipUEh1aeJArEy0QbLV5PI5hPir0jKHO1PYeF1ZyEv_nuRNG7BKG2',
    ),
    _SessionItem(
      title: 'Reef Outpost B-44',
      status: 'Bleached',
      statusColor: AppColors.bleached,
      confidence: 87.1,
      date: 'Nov 22, 2024 • 09:15',
      imageUrl:
          'https://lh3.googleusercontent.com/aida-public/AB6AXuAJIM7acx6pGIcHxWqADM1qtJEp9pwaGEj5uwTxgnZNPQaOpTbklhtmt7Dk3lYeYmMgQNBhFJ4AukkOlhms1CZzRCtgp7-XjQY5sxmfGcsCDyBx2e0_SczCjOSot-6ctyP0xORb5tUkQbqzJ24S0J1djJjIXkkC36vXY5nRD7vvfEmkHPh3RZCdtIeXz3j6aOoUEsHm4aSGA42C6BKzv13IhBITJUXyZc3s9QhGNfq_9eLYYXrJCRPc5MaufriNY8V7rMx94DghfDiU',
    ),
    _SessionItem(
      title: 'Coral Triangle Site 7',
      status: 'Dead',
      statusColor: AppColors.dead,
      confidence: 94.8,
      date: 'Nov 19, 2024 • 11:42',
      imageUrl:
          'https://lh3.googleusercontent.com/aida-public/AB6AXuBilSDVvkiFNcTymxLbIY-M1f7Bmh_P-dOeqhlbDKytlM2UTjfDXSyma98oHcFGsiVU9WBG6I-t7aPm9KoKPDsIJnw_5sC92KBFOqvorzNGcX75fjM9ez4dJjgX_0Go9OXYchOidvxaC1jU6ib2B7MkKEFhYkhJ8qu4g6m6ZwT0xP1nCb4nfsbpiBKL--MZWX6uVZS9YwYAXBUek27Rd94M7trmFYAq-UAy506oZIG66o6QsHY2uDAVIa71ckxQzDUUkIKoJFGhEpx9',
    ),
  ];

  List<_SessionItem> get _filtered {
    if (_filter == 0) return _items;
    final label = _filters[_filter];
    return _items.where((i) => i.status == label).toList();
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
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 110),
              children: [
                _trendCard(),
                const SizedBox(height: 24),
                _filterPills(),
                const SizedBox(height: 16),
                ..._filtered.map((item) => Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: _sessionCard(item),
                    )),
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
      color: context.colors.background.withValues(alpha: 0.9),
      child: Row(
        children: [
          const Icon(Icons.history, color: AppColors.primary, size: 28),
          const SizedBox(width: 12),
          Text('History',
              style: AppText.headlineLgMobile.copyWith(
                color: context.colors.onBackground,
                fontWeight: FontWeight.w700,
              )),
          const Spacer(),
          Container(
            width: 40,
            height: 40,
            decoration: const BoxDecoration(
              color: context.colors.surface,
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.filter_list, color: context.colors.textMuted, size: 20),
          ),
        ],
      ),
    );
  }

  Widget _trendCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: context.colors.surface,
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Assessment Activity',
                        style: AppText.titleMd.copyWith(color: context.colors.onBackground)),
                    const SizedBox(height: 2),
                    Text('Tracking reef health scans',
                        style: AppText.labelSm.copyWith(color: context.colors.textMuted)),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(
                  color: const Color(0xFF1C1B1B),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: List.generate(_ranges.length, (i) {
                    final active = _range == i;
                    return GestureDetector(
                      onTap: () => setState(() => _range = i),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: active ? AppColors.primary : Colors.transparent,
                          borderRadius: BorderRadius.circular(999),
                        ),
                        child: Text(
                          _ranges[i],
                          style: AppText.labelSm.copyWith(
                            color: active ? context.colors.onPrimary : context.colors.textMuted,
                            fontWeight: active ? FontWeight.w700 : FontWeight.w500,
                          ),
                        ),
                      ),
                    );
                  }),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 128,
            child: CustomPaint(painter: _LineChartPainter(), size: Size.infinite),
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                .map((d) => Text(d,
                    style: AppText.labelSm.copyWith(color: context.colors.textMuted)))
                .toList(),
          ),
        ],
      ),
    );
  }

  Widget _filterPills() {
    return SizedBox(
      height: 36,
      child: ListView.separated(
        scrollDirection: Axis.horizontal,
        itemCount: _filters.length,
        separatorBuilder: (_, _) => const SizedBox(width: 8),
        itemBuilder: (_, i) {
          final active = _filter == i;
          return GestureDetector(
            onTap: () => setState(() => _filter = i),
            child: Container(
              alignment: Alignment.center,
              padding: const EdgeInsets.symmetric(horizontal: 20),
              decoration: BoxDecoration(
                color: active ? AppColors.primary : Colors.white.withValues(alpha: 0.05),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: Colors.white.withValues(alpha: 0.1)),
                boxShadow: active
                    ? [BoxShadow(color: AppColors.primary.withValues(alpha: 0.2), blurRadius: 12)]
                    : null,
              ),
              child: Text(
                _filters[i],
                style: AppText.labelSm.copyWith(
                  color: active ? context.colors.onPrimary : context.colors.textMuted,
                  fontWeight: active ? FontWeight.w700 : FontWeight.w500,
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _sessionCard(_SessionItem item) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1C1B1B).withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Row(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(12),
            child: Image.network(
              item.imageUrl,
              width: 64,
              height: 64,
              fit: BoxFit.cover,
              errorBuilder: (_, _, _) => Container(
                width: 64,
                height: 64,
                color: context.colors.surface,
                child: const Icon(Icons.image, color: context.colors.textMuted),
              ),
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(item.title,
                    style: AppText.bodyMd.copyWith(
                      color: context.colors.onBackground,
                      fontWeight: FontWeight.w600,
                    )),
                const SizedBox(height: 4),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: BoxDecoration(
                        color: item.statusColor.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(999),
                        border: Border.all(color: item.statusColor.withValues(alpha: 0.2)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 6,
                            height: 6,
                            decoration: BoxDecoration(
                              color: item.statusColor,
                              shape: BoxShape.circle,
                            ),
                          ),
                          const SizedBox(width: 6),
                          Text(
                            item.status,
                            style: AppText.labelSm.copyWith(
                              color: item.statusColor,
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('${item.confidence}%',
                            style: AppText.bodyMd.copyWith(
                              color: context.colors.onBackground,
                              fontWeight: FontWeight.w700,
                              height: 1,
                            )),
                        Text('CONFIDENCE',
                            style: AppText.labelSm.copyWith(
                              color: context.colors.textMuted,
                              fontSize: 9,
                              letterSpacing: 1,
                              fontWeight: FontWeight.w600,
                            )),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(item.date,
                    style: AppText.labelSm
                        .copyWith(color: context.colors.textMuted.withValues(alpha: 0.7))),
              ],
            ),
          ),
          Icon(Icons.chevron_right, color: context.colors.textMuted.withValues(alpha: 0.4)),
        ],
      ),
    );
  }
}

class _SessionItem {
  _SessionItem({
    required this.title,
    required this.status,
    required this.statusColor,
    required this.confidence,
    required this.date,
    required this.imageUrl,
  });
  final String title;
  final String status;
  final Color statusColor;
  final double confidence;
  final String date;
  final String imageUrl;
}

class _LineChartPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final ys = [0.8, 0.45, 0.6, 0.2, 0.55, 0.15, 0.3];
    final points = <Offset>[];
    for (var i = 0; i < ys.length; i++) {
      points.add(Offset(i / (ys.length - 1) * size.width, ys[i] * size.height));
    }
    final path = Path()..moveTo(points.first.dx, points.first.dy);
    for (var i = 1; i < points.length; i++) {
      final p1 = points[i - 1];
      final p2 = points[i];
      final mid = Offset((p1.dx + p2.dx) / 2, (p1.dy + p2.dy) / 2);
      path.quadraticBezierTo(p1.dx, p1.dy, mid.dx, mid.dy);
    }
    path.lineTo(points.last.dx, points.last.dy);

    final fillPath = Path.from(path)
      ..lineTo(size.width, size.height)
      ..lineTo(0, size.height)
      ..close();
    final fillPaint = Paint()
      ..shader = const LinearGradient(
        colors: [Color(0x4D00F5D4), Color(0x0000F5D4)],
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
      ).createShader(Offset.zero & size);
    canvas.drawPath(fillPath, fillPaint);

    final stroke = Paint()
      ..color = AppColors.primary
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3
      ..strokeCap = StrokeCap.round;
    canvas.drawPath(path, stroke);

    final dot = Paint()..color = AppColors.primary;
    canvas.drawCircle(points[2], 4, dot);
    canvas.drawCircle(points[5], 4, dot);
  }

  @override
  bool shouldRepaint(covariant CustomPainter old) => false;
}
