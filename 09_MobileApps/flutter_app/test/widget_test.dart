import 'package:flutter_test/flutter_test.dart';

import 'package:coral_ai/main.dart';

void main() {
  testWidgets('App boots into onboarding', (WidgetTester tester) async {
    await tester.pumpWidget(const CoralAiApp());
    await tester.pump();
    expect(find.text('Get Started  →'), findsOneWidget);
  });
}
