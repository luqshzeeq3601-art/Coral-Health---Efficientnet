import 'package:flutter/material.dart';
import '../theme.dart';

class InfoScreen extends StatefulWidget {
  const InfoScreen({super.key});

  @override
  State<InfoScreen> createState() => _InfoScreenState();
}

class _InfoScreenState extends State<InfoScreen> {
  final _expanded = {0: true, 1: false, 2: false};

  static final _classes = [
    _CoralClass(
      name: 'Healthy',
      color: AppColors.healthy,
      title: 'Class 0: Healthy',
      summary:
          'The neural engine identifies Healthy specimens by detecting vibrant, consistent pigmentation and complex, unbroken polyp structures, often showing strong contrast against the substrate.',
      signs: ['Intact Polyps', 'Diverse Colors', 'Rapid Growth'],
      causes: ['Stable Temps', 'Low Pollution', 'High Salinity'],
      quote:
          'A healthy reef supports 25% of all marine species despite covering less than 1% of the ocean floor.',
      imageUrl:
          'https://lh3.googleusercontent.com/aida-public/AB6AXuCQ8YEq4178-Ow0We7WV3mRUpgOZgyheQsSoWjn2u-fuX83N09Phyke-WzKlzNygquxml8Yr30R_s1IdqCSv3vIlj7f-4WH4d6Tu1tt7z8u58PiZg3T4IeNBWh76V4JjW1MytTxJ9Xwxo9fxXIdLt0RucKdSHTWSJN75buIT9wPDtKS2Nl_7idEth1LnVknSXmSLYE-g8dSG7bUKaaMRRVquxBOipUEh1aeJArEy0QbLV5PI5hPir0jKHO1PYeF1ZyEv_nuRNG7BKG2',
    ),
    _CoralClass(
      name: 'Bleached',
      color: AppColors.bleached,
      title: 'Class 1: Bleached',
      summary:
          'The model detects bleaching by identifying stark white skeletal structures and the absence of zooxanthellae pigmentation, differentiating it from light-colored healthy species.',
      signs: ['Stark White', 'Fluorescent Hues', 'Slow Polyps'],
      causes: ['Global Warming', 'Extreme Tides', 'Over-exposure'],
      quote:
          "Bleaching is not death; it's a plea for survival. If temperatures drop, the algae can return.",
      imageUrl:
          'https://lh3.googleusercontent.com/aida-public/AB6AXuAJIM7acx6pGIcHxWqADM1qtJEp9pwaGEj5uwTxgnZNPQaOpTbklhtmt7Dk3lYeYmMgQNBhFJ4AukkOlhms1CZzRCtgp7-XjQY5sxmfGcsCDyBx2e0_SczCjOSot-6ctyP0xORb5tUkQbqzJ24S0J1djJjIXkkC36vXY5nRD7vvfEmkHPh3RZCdtIeXz3j6aOoUEsHm4aSGA42C6BKzv13IhBITJUXyZc3s9QhGNfq_9eLYYXrJCRPc5MaufriNY8V7rMx94DghfDiU',
    ),
    _CoralClass(
      name: 'Dead',
      color: AppColors.dead,
      title: 'Class 2: Dead',
      summary:
          'The classifier recognizes structural collapse and overgrowth of turf algae. It looks for loss of fine coral detail and the specific textural patterns of opportunistic algal colonization.',
      signs: ['Algae Growth', 'Erosion', 'Grey Color'],
      causes: ['Starvation', 'Disease', 'Acidification'],
      quote:
          'Without the calcium carbonate structure, coastal communities lose their first line of defense against waves.',
      imageUrl:
          'https://lh3.googleusercontent.com/aida-public/AB6AXuBilSDVvkiFNcTymxLbIY-M1f7Bmh_P-dOeqhlbDKytlM2UTjfDXSyma98oHcFGsiVU9WBG6I-t7aPm9KoKPDsIJnw_5sC92KBFOqvorzNGcX75fjM9ez4dJjgX_0Go9OXYchOidvxaC1jU6ib2B7MkKEFhYkhJ8qu4g6m6ZwT0xP1nCb4nfsbpiBKL--MZWX6uVZS9YwYAXBUek27Rd94M7trmFYAq-UAy506oZIG66o6QsHY2uDAVIa71ckxQzDUUkIKoJFGhEpx9',
    ),
  ];

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
                Text('BHD Dataset Guide',
                    style: AppText.headlineLgMobile.copyWith(
                      color: context.colors.onBackground,
                      fontWeight: FontWeight.w700,
                    )),
                const SizedBox(height: 4),
                Text(
                  'Technical reference for the 3 coral health classes detected by the EfficientNetB0 model.',
                  style: AppText.bodyMd.copyWith(
                    color: context.colors.textMuted,
                    fontSize: 13,
                  ),
                ),
                const SizedBox(height: 20),
                ...List.generate(_classes.length, (i) => Padding(
                      padding: const EdgeInsets.only(bottom: 16),
                      child: _classCard(i, _classes[i]),
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
          const Icon(Icons.help_outline, color: AppColors.primary, size: 28),
          const SizedBox(width: 12),
          Text('Coral Health Guide',
              style: AppText.headlineLgMobile.copyWith(
                color: context.colors.onBackground,
                fontWeight: FontWeight.w700,
                fontSize: 18,
              )),
        ],
      ),
    );
  }

  Widget _classCard(int index, _CoralClass cls) {
    final expanded = _expanded[index] ?? false;
    return GestureDetector(
      onTap: () => setState(() => _expanded[index] = !expanded),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        decoration: BoxDecoration(
          color: context.colors.surface,
          borderRadius: BorderRadius.circular(24),
        ),
        clipBehavior: Clip.antiAlias,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Stack(
              children: [
                Image.network(
                  cls.imageUrl,
                  height: 192,
                  width: double.infinity,
                  fit: BoxFit.cover,
                  errorBuilder: (_, _, _) => Container(
                    height: 192,
                    color: context.colors.surfaceElevated,
                    child: Icon(Icons.image, color: cls.color, size: 48),
                  ),
                ),
                Positioned(
                  top: 16,
                  left: 16,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: cls.color,
                      borderRadius: BorderRadius.circular(999),
                    ),
                    child: Text(
                      cls.name,
                      style: AppText.labelSm.copyWith(
                        color: context.colors.background,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(cls.title,
                          style: AppText.titleMd
                              .copyWith(color: context.colors.onBackground)),
                      AnimatedRotation(
                        turns: expanded ? 0.5 : 0,
                        duration: const Duration(milliseconds: 250),
                        child: const Icon(Icons.expand_more,
                            color: AppColors.primary),
                      ),
                    ],
                  ),
                  const SizedBox(height: 8),
                  Text(cls.summary,
                      style: AppText.bodyMd
                          .copyWith(color: context.colors.textMuted, fontSize: 13)),
                  if (expanded) ...[
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(child: _detailBlock('Signs', cls.signs, cls.color)),
                        const SizedBox(width: 12),
                        Expanded(child: _detailBlock('Causes', cls.causes, cls.color)),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.fromLTRB(16, 8, 8, 8),
                      decoration: BoxDecoration(
                        border: Border(left: BorderSide(color: cls.color, width: 2)),
                      ),
                      child: Text(
                        '"${cls.quote}"',
                        style: AppText.bodyMd.copyWith(
                          color: context.colors.onBackground.withValues(alpha: 0.8),
                          fontStyle: FontStyle.italic,
                          fontSize: 13,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _detailBlock(String label, List<String> items, Color dotColor) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1C1B1B),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white.withValues(alpha: 0.05)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label.toUpperCase(),
              style: AppText.labelSm.copyWith(
                color: AppColors.primary,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.2,
              )),
          const SizedBox(height: 8),
          ...items.map((item) => Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(
                  children: [
                    Text('●',
                        style: TextStyle(color: dotColor, fontSize: 10)),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(item,
                          style: AppText.bodyMd.copyWith(
                            color: context.colors.onBackground,
                            fontSize: 13,
                          )),
                    ),
                  ],
                ),
              )),
        ],
      ),
    );
  }
}

class _CoralClass {
  _CoralClass({
    required this.name,
    required this.color,
    required this.title,
    required this.summary,
    required this.signs,
    required this.causes,
    required this.quote,
    required this.imageUrl,
  });

  final String name;
  final Color color;
  final String title;
  final String summary;
  final List<String> signs;
  final List<String> causes;
  final String quote;
  final String imageUrl;
}
