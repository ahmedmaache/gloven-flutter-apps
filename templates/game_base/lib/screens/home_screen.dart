import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
import 'game_screen.dart';
import 'settings_screen.dart';
import 'tutorial_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final settingsProvider = Provider.of<SettingsProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Game Template'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () async {
              await SoundManager.playSound('tap', context);
              await VibrationManager.vibrate(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.sports_esports,
              size: 100,
              color: Colors.blue,
            ),
            const SizedBox(height: 24),
            const Text(
              'Game Template',
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 48),
            ElevatedButton.icon(
              onPressed: () async {
                await SoundManager.playSound('tap', context);
                await VibrationManager.vibrate(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const GameScreen()),
                );
              },
              icon: const Icon(Icons.play_arrow),
              label: const Text('Play Game'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
            ),
            const SizedBox(height: 16),
            OutlinedButton.icon(
              onPressed: () async {
                await SoundManager.playSound('tap', context);
                await VibrationManager.vibrate(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => TutorialScreen(
                      gameName: 'Game Template',
                      gameType: 'puzzle',
                      instructions: [
                        'Tap to interact',
                        'Follow the on-screen prompts',
                        'Try to achieve the highest score',
                        'Use settings to customize your experience',
                      ],
                    ),
                  ),
                );
              },
              icon: const Icon(Icons.help_outline),
              label: const Text('How to Play'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
            ),
            const SizedBox(height: 32),
            Text(
              'Difficulty: ${settingsProvider.difficulty.toUpperCase()}',
              style: Theme.of(context).textTheme.titleMedium,
            ),
          ],
        ),
      ),
    );
  }
}

