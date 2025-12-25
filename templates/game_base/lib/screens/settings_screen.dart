import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final settingsProvider = Provider.of<SettingsProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Dark Mode
          Card(
            child: SwitchListTile(
              title: const Text('Dark Mode'),
              subtitle: const Text('Toggle dark theme'),
              value: settingsProvider.darkMode,
              onChanged: (_) => settingsProvider.toggleDarkMode(),
            ),
          ),
          const SizedBox(height: 8),
          
          // Sound
          Card(
            child: SwitchListTile(
              title: const Text('Sound'),
              subtitle: const Text('Enable/disable sound effects'),
              value: settingsProvider.soundEnabled,
              onChanged: (_) => settingsProvider.toggleSound(),
            ),
          ),
          const SizedBox(height: 8),
          
          // Vibration
          Card(
            child: SwitchListTile(
              title: const Text('Vibration'),
              subtitle: const Text('Enable/disable vibration'),
              value: settingsProvider.vibrationEnabled,
              onChanged: (_) => settingsProvider.toggleVibration(),
            ),
          ),
          const SizedBox(height: 8),
          
          // Difficulty
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Difficulty Level',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  SegmentedButton<String>(
                    segments: const [
                      ButtonSegment(value: 'easy', label: Text('Easy')),
                      ButtonSegment(value: 'medium', label: Text('Medium')),
                      ButtonSegment(value: 'hard', label: Text('Hard')),
                    ],
                    selected: {settingsProvider.difficulty},
                    onSelectionChanged: (Set<String> newSelection) {
                      settingsProvider.setDifficulty(newSelection.first);
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

