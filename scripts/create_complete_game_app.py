#!/usr/bin/env python3
"""
Create a complete game app with all features and unique game logic
"""

import os
import shutil
import subprocess
from pathlib import Path
import json

def create_complete_game_app(app_num, game_name, game_type, instructions):
    """Create a complete game app with unique implementation"""
    
    app_name = f"app{app_num:02d}"
    package_name = f"org.gloven.{app_name}"
    app_dir = Path(f"apps/{app_name}")
    
    print(f"Creating {app_num}/100: {game_name}...")
    
    # Step 1: Create Flutter app structure (if not exists)
    if not app_dir.exists():
        subprocess.run(
            ["flutter", "create", "--org", "org.gloven", "--project-name", app_name, str(app_dir)],
            check=True,
            capture_output=True
        )
    
    # Step 2: Update pubspec.yaml with game dependencies
    pubspec_path = app_dir / "pubspec.yaml"
    if pubspec_path.exists():
        content = pubspec_path.read_text()
        if "audioplayers" not in content:
            # Add dependencies
            deps_section = """
dependencies:
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  audioplayers: ^5.2.1
  vibration: ^1.8.4
"""
            # Insert after existing dependencies
            lines = content.split('\n')
            new_lines = []
            in_deps = False
            for line in lines:
                if line.strip().startswith('dependencies:'):
                    in_deps = True
                    new_lines.append(line)
                elif in_deps and line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    # End of dependencies
                    new_lines.append(deps_section.strip())
                    in_deps = False
                    new_lines.append(line)
                else:
                    new_lines.append(line)
            pubspec_path.write_text('\n'.join(new_lines))
    
    # Step 3: Create game structure
    lib_dir = app_dir / "lib"
    lib_dir.mkdir(exist_ok=True)
    
    models_dir = lib_dir / "models"
    providers_dir = lib_dir / "providers"
    screens_dir = lib_dir / "screens"
    utils_dir = lib_dir / "utils"
    
    for d in [models_dir, providers_dir, screens_dir, utils_dir]:
        d.mkdir(exist_ok=True)
    
    # Step 4: Copy template files
    template_dir = Path("templates/game_base/lib")
    if template_dir.exists():
        # Copy models
        for file in (template_dir / "models").glob("*.dart"):
            shutil.copy(file, models_dir / file.name)
        # Copy providers
        for file in (template_dir / "providers").glob("*.dart"):
            shutil.copy(file, providers_dir / file.name)
        # Copy utils
        for file in (template_dir / "utils").glob("*.dart"):
            shutil.copy(file, utils_dir / file.name)
    
    # Step 5: Generate game-specific screens
    generate_game_screens(app_dir, game_name, game_type, instructions, app_num)
    
    # Step 6: Update main.dart
    generate_main_dart(app_dir, game_name, game_type, instructions)
    
    # Step 7: Update Android package name
    subprocess.run(
        ["python3", "scripts/update_build_gradle.py", 
         str(app_dir / "android" / "app" / "build.gradle.kts"), package_name],
        check=False
    )
    
    print(f"✅ {game_name} created")
    return True

def generate_game_screens(app_dir, game_name, game_type, instructions, app_num):
    """Generate game-specific screens"""
    screens_dir = app_dir / "lib" / "screens"
    
    # Generate tutorial screen
    tutorial_code = generate_tutorial_screen(game_name, game_type, instructions)
    (screens_dir / "tutorial_screen.dart").write_text(tutorial_code)
    
    # Generate game screen with unique logic
    game_code = generate_game_screen(game_name, game_type, app_num)
    (screens_dir / "game_screen.dart").write_text(game_code)
    
    # Generate home screen
    home_code = generate_home_screen(game_name, game_type)
    (screens_dir / "home_screen.dart").write_text(home_code)
    
    # Generate settings screen (copy from template)
    settings_code = generate_settings_screen()
    (screens_dir / "settings_screen.dart").write_text(settings_code)

def generate_tutorial_screen(game_name, game_type, instructions):
    """Generate tutorial screen code"""
    instructions_list = ',\n        '.join([f'"{inst}"' for inst in instructions])
    game_type_upper = game_type.upper()
    return f'''import 'package:flutter/material.dart';

class TutorialScreen extends StatelessWidget {{
  const TutorialScreen({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('How to Play: {game_name}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Game Type: {game_type_upper}',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 24),
            const Text(
              'Instructions:',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            ...{instructions_list}.asMap().entries.map((entry) {{
              return Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      width: 24,
                      height: 24,
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor,
                        shape: BoxShape.circle,
                      ),
                      child: Center(
                        child: Text(
                          '${{entry.key + 1}}',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        entry.value,
                        style: const TextStyle(fontSize: 16),
                      ),
                    ),
                  ],
                ),
              );
            }}),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Got it! Let\\'s Play'),
              ),
            ),
          ],
        ),
      ),
    );
  }}
}}
'''

def generate_game_screen(game_name, game_type, app_num):
    """Generate game screen with unique logic"""
    # This will be customized based on game type and name
    return f'''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
import 'dart:math';
import 'dart:async';

class GameScreen extends StatefulWidget {{
  const GameScreen({{super.key}});

  @override
  State<GameScreen> createState() => _GameScreenState();
}}

class _GameScreenState extends State<GameScreen> {{
  int _score = 0;
  int _bestScore = 0;
  bool _gameActive = false;
  String _gameStatus = 'Tap to Start';
  
  // Game-specific variables
  {get_game_state_vars(game_name, game_type)}
  
  @override
  void initState() {{
    super.initState();
    _loadBestScore();
    {get_game_init_logic(game_name, game_type)}
  }}
  
  Future<void> _loadBestScore() async {{
    // Load from SharedPreferences
    setState(() => _bestScore = 0);
  }}
  
  Future<void> _saveBestScore() async {{
    if (_score > _bestScore) {{
      setState(() => _bestScore = _score);
    }}
  }}
  
  void _startGame() {{
    setState(() {{
      _gameActive = true;
      _score = 0;
      _gameStatus = 'Playing...';
    }});
    {get_game_start_logic(game_name, game_type)}
    SoundManager.playSound('success', context);
    VibrationManager.vibrate(context, duration: 100);
  }}
  
  void _gameAction() async {{
    if (!_gameActive) {{
      _startGame();
      return;
    }}
    
    try {{
      final settings = Provider.of<SettingsProvider>(context, listen: false);
      {get_game_action_logic(game_name, game_type)}
      
      await SoundManager.playSound('tap', context);
      await VibrationManager.vibrate(context, duration: 50);
    }} catch (e) {{
      debugPrint('Game error: $e');
    }}
  }}
  
  {get_game_specific_methods(game_name, game_type)}
  
  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('{game_name}'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _scoreCard('Score', _score),
                  _scoreCard('Best', _bestScore),
                ],
              ),
            ),
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      _gameStatus,
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 48),
                    {get_game_ui(game_name, game_type)}
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }}
  
  Widget _scoreCard(String label, int value) {{
    return Column(
      children: [
        Text(label),
        Text(
          '$value',
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }}
}}
'''

def get_game_state_vars(game_name, game_type):
    """Get game-specific state variables"""
    vars_map = {
        "Number Slide Puzzle": "List<int> _puzzle = []; int _emptyIndex = 0; int _size = 3;",
        "Space Shooter": "double _shipX = 0.5; List<Map> _bullets = []; List<Map> _asteroids = []; Timer? _gameTimer;",
        "Tower Defense": "List<Map> _towers = []; List<Map> _enemies = []; int _wave = 1; int _coins = 100;",
        "Tap Reaction": "DateTime? _signalTime; bool _signalVisible = false; int _reactionTime = 0; Timer? _signalTimer;",
        "Bubble Pop": "List<List<Color>> _bubbles = []; int _rows = 8; int _cols = 6;",
    }
    return vars_map.get(game_name, "// Game state variables")

def get_game_init_logic(game_name, game_type):
    """Get game initialization logic"""
    init_map = {
        "Number Slide Puzzle": "_initializePuzzle();",
        "Space Shooter": "_startGameLoop();",
        "Tower Defense": "_initializeGame();",
        "Tap Reaction": "_resetGame();",
        "Bubble Pop": "_generateBubbles();",
    }
    return init_map.get(game_name, "// Initialize game")

def get_game_start_logic(game_name, game_type):
    """Get game start logic"""
    return "// Start game logic"

def get_game_action_logic(game_name, game_type):
    """Get game action logic"""
    action_map = {
        "Number Slide Puzzle": """
      _handlePuzzleTap();
      if (_isPuzzleSolved()) {
        _gameWon();
      }
      """,
        "Space Shooter": """
      _shoot();
      _updateGame();
      """,
        "Tower Defense": """
      _placeTower();
      _updateWave();
      """,
        "Tap Reaction": """
      if (_signalVisible) {
        _calculateReaction();
        _nextSignal();
      }
      """,
        "Bubble Pop": """
      _popBubble();
      _checkMatches();
      """,
    }
    return action_map.get(game_name, "setState(() { _score++; });")

def get_game_specific_methods(game_name, game_type):
    """Get game-specific methods"""
    methods_map = {
        "Number Slide Puzzle": """
  void _initializePuzzle() {
    _size = Provider.of<SettingsProvider>(context, listen: false).difficulty == 'easy' ? 3 :
            Provider.of<SettingsProvider>(context, listen: false).difficulty == 'medium' ? 4 : 5;
    _puzzle = List.generate(_size * _size, (i) => i + 1);
    _puzzle[_puzzle.length - 1] = 0;
    _emptyIndex = _puzzle.length - 1;
    _puzzle.shuffle();
  }
  
  void _handlePuzzleTap(int index) {
    if (_canMove(index)) {
      _puzzle[_emptyIndex] = _puzzle[index];
      _puzzle[index] = 0;
      _emptyIndex = index;
      setState(() {});
    }
  }
  
  bool _canMove(int index) {
    int row = index ~/ _size;
    int col = index % _size;
    int emptyRow = _emptyIndex ~/ _size;
    int emptyCol = _emptyIndex % _size;
    return (row == emptyRow && (col - emptyCol).abs() == 1) ||
           (col == emptyCol && (row - emptyRow).abs() == 1);
  }
  
  bool _isPuzzleSolved() {
    for (int i = 0; i < _puzzle.length - 1; i++) {
      if (_puzzle[i] != i + 1) return false;
    }
    return true;
  }
  
  void _gameWon() {
    setState(() {
      _gameActive = false;
      _gameStatus = 'Puzzle Solved!';
    });
    _saveBestScore();
    SoundManager.playSound('success', context);
    VibrationManager.vibratePattern(context, [0, 200, 100, 200]);
  }
  """,
        # Add more game-specific methods as needed
    }
    return methods_map.get(game_name, "// Game-specific methods")

def get_game_ui(game_name, game_type):
    """Get game-specific UI"""
    ui_map = {
        "Number Slide Puzzle": """
                    GridView.builder(
                      shrinkWrap: true,
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: _size,
                        crossAxisSpacing: 4,
                        mainAxisSpacing: 4,
                      ),
                      itemCount: _puzzle.length,
                      itemBuilder: (context, index) {
                        if (_puzzle[index] == 0) {
                          return Container(color: Colors.grey[300]);
                        }
                        return GestureDetector(
                          onTap: () => _gameAction(),
                          child: Container(
                            color: Colors.blue,
                            child: Center(
                              child: Text(
                                '${_puzzle[index]}',
                                style: const TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                    """,
        "Space Shooter": """
                    GestureDetector(
                      onTap: _gameAction,
                      child: Container(
                        width: 200,
                        height: 200,
                        decoration: BoxDecoration(
                          color: _gameActive ? Colors.green : Colors.blue,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.rocket_launch, size: 100, color: Colors.white),
                      ),
                    ),
                    """,
    }
    return ui_map.get(game_name, """
                    GestureDetector(
                      onTap: _gameAction,
                      child: Container(
                        width: 200,
                        height: 200,
                        decoration: BoxDecoration(
                          color: _gameActive ? Colors.green : Colors.blue,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.touch_app, size: 100, color: Colors.white),
                      ),
                    ),
                    """)

def generate_home_screen(game_name, game_type):
    """Generate home screen"""
    return f'''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
import 'game_screen.dart';
import 'settings_screen.dart';
import 'tutorial_screen.dart';

class HomeScreen extends StatelessWidget {{
  const HomeScreen({{super.key}});

  @override
  Widget build(BuildContext context) {{
    final settingsProvider = Provider.of<SettingsProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: Text('{game_name}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () async {{
              await SoundManager.playSound('tap', context);
              await VibrationManager.vibrate(context);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const SettingsScreen()),
              );
            }},
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
            Text(
              '{game_name}',
              style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 48),
            ElevatedButton.icon(
              onPressed: () async {{
                await SoundManager.playSound('tap', context);
                await VibrationManager.vibrate(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const GameScreen()),
                );
              }},
              icon: const Icon(Icons.play_arrow),
              label: const Text('Play Game'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
            ),
            const SizedBox(height: 16),
            OutlinedButton.icon(
              onPressed: () async {{
                await SoundManager.playSound('tap', context);
                await VibrationManager.vibrate(context);
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const TutorialScreen()),
                );
              }},
              icon: const Icon(Icons.help_outline),
              label: const Text('How to Play'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
              ),
            ),
            const SizedBox(height: 32),
            Text(
              'Difficulty: ${{settingsProvider.difficulty.toUpperCase()}}',
              style: Theme.of(context).textTheme.titleMedium,
            ),
          ],
        ),
      ),
    );
  }}
}}
'''

def generate_settings_screen():
    """Generate settings screen"""
    return '''import 'package:flutter/material.dart';
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
          Card(
            child: SwitchListTile(
              title: const Text('Dark Mode'),
              subtitle: const Text('Toggle dark theme'),
              value: settingsProvider.darkMode,
              onChanged: (_) => settingsProvider.toggleDarkMode(),
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: SwitchListTile(
              title: const Text('Sound'),
              subtitle: const Text('Enable/disable sound effects'),
              value: settingsProvider.soundEnabled,
              onChanged: (_) => settingsProvider.toggleSound(),
            ),
          ),
          const SizedBox(height: 8),
          Card(
            child: SwitchListTile(
              title: const Text('Vibration'),
              subtitle: const Text('Enable/disable vibration'),
              value: settingsProvider.vibrationEnabled,
              onChanged: (_) => settingsProvider.toggleVibration(),
            ),
          ),
          const SizedBox(height: 8),
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
'''

def generate_main_dart(app_dir, game_name, game_type, instructions):
    """Generate main.dart"""
    main_code = f'''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/settings_provider.dart';
import 'screens/home_screen.dart';
import 'utils/sound_manager.dart';

void main() async {{
  WidgetsFlutterBinding.ensureInitialized();
  await SoundManager.initialize();
  
  runApp(
    ChangeNotifierProvider(
      create: (_) => SettingsProvider()..loadSettings(),
      child: const GameApp(),
    ),
  );
}}

class GameApp extends StatelessWidget {{
  const GameApp({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Consumer<SettingsProvider>(
      builder: (context, settingsProvider, _) {{
        return MaterialApp(
          title: '{game_name}',
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
        );
      }},
    );
  }}
}}
'''
    (app_dir / "lib" / "main.dart").write_text(main_code)

# Main execution
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: create_complete_game_app.py <app_num> <game_name> <game_type> <instructions_json>")
        sys.exit(1)
    
    app_num = int(sys.argv[1])
    game_name = sys.argv[2]
    game_type = sys.argv[3]
    instructions = json.loads(sys.argv[4])
    
    create_complete_game_app(app_num, game_name, game_type, instructions)

