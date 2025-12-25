import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/settings_provider.dart';
import 'screens/home_screen.dart';
import 'screens/game_screen.dart';
import 'screens/settings_screen.dart';
import 'screens/tutorial_screen.dart';
import 'utils/sound_manager.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SoundManager.initialize();
  
  runApp(
    ChangeNotifierProvider(
      create: (_) => SettingsProvider()..loadSettings(),
      child: const GameApp(),
    ),
  );
}

class GameApp extends StatelessWidget {
  const GameApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<SettingsProvider>(
      builder: (context, settingsProvider, _) {
        return MaterialApp(
          title: 'Game Template',
          debugShowCheckedModeBanner: false,
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
            useMaterial3: true,
          ),
          darkTheme: ThemeData(
            colorScheme: ColorScheme.fromSeed(
              seedColor: Colors.blue,
              brightness: Brightness.dark,
            ),
            useMaterial3: true,
          ),
          themeMode: settingsProvider.darkMode ? ThemeMode.dark : ThemeMode.light,
          home: const HomeScreen(),
          routes: {
            '/game': (context) => const GameScreen(),
            '/settings': (context) => const SettingsScreen(),
            '/tutorial': (context) => TutorialScreen(
              gameName: 'Game Template',
              gameType: 'puzzle',
              instructions: [
                'Tap to interact',
                'Follow the on-screen prompts',
                'Try to achieve the highest score',
                'Use settings to customize your experience',
              ],
            ),
          },
        );
      },
    );
  }
}

