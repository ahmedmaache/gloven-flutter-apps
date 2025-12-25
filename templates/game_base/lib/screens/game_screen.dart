import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
import 'dart:math';

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  int _score = 0;
  int _bestScore = 0;
  bool _gameActive = false;
  String _gameStatus = 'Tap to Start';
  
  @override
  void initState() {
    super.initState();
    _loadBestScore();
  }
  
  Future<void> _loadBestScore() async {
    // Load best score from SharedPreferences
    // For now, using 0
    setState(() {
      _bestScore = 0;
    });
  }
  
  Future<void> _saveBestScore() async {
    if (_score > _bestScore) {
      // Save to SharedPreferences
      setState(() {
        _bestScore = _score;
      });
    }
  }
  
  void _startGame() {
    setState(() {
      _gameActive = true;
      _score = 0;
      _gameStatus = 'Game Active';
    });
    SoundManager.playSound('success', context);
    VibrationManager.vibrate(context, duration: 100);
  }
  
  void _gameAction() async {
    if (!_gameActive) {
      _startGame();
      return;
    }
    
    try {
      final settingsProvider = Provider.of<SettingsProvider>(context, listen: false);
      
      // Game logic here - this is template
      setState(() {
        _score++;
        _gameStatus = 'Score: $_score';
      });
      
      // Play sound and vibrate
      await SoundManager.playSound('tap', context);
      await VibrationManager.vibrate(context, duration: 50);
      
      // Adjust difficulty
      int targetScore = settingsProvider.difficulty == 'easy' ? 10 :
                        settingsProvider.difficulty == 'medium' ? 20 : 30;
      
      if (_score >= targetScore) {
        _gameWon();
      }
    } catch (e) {
      // Error handling - don't crash
      debugPrint('Game action error: $e');
    }
  }
  
  void _gameWon() async {
    setState(() {
      _gameActive = false;
      _gameStatus = 'You Won!';
    });
    await _saveBestScore();
    await SoundManager.playSound('success', context);
    await VibrationManager.vibratePattern(context, [0, 200, 100, 200]);
  }
  
  void _gameOver() async {
    setState(() {
      _gameActive = false;
      _gameStatus = 'Game Over';
    });
    await _saveBestScore();
    await SoundManager.playSound('gameOver', context);
    await VibrationManager.vibratePattern(context, [0, 500]);
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Game'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () async {
            await SoundManager.playSound('tap', context);
            Navigator.pop(context);
          },
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Score Display
            Container(
              padding: const EdgeInsets.all(16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Column(
                    children: [
                      const Text('Score'),
                      Text(
                        '$_score',
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  Column(
                    children: [
                      const Text('Best'),
                      Text(
                        '$_bestScore',
                        style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            
            // Game Area
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
                    GestureDetector(
                      onTap: _gameAction,
                      child: Container(
                        width: 200,
                        height: 200,
                        decoration: BoxDecoration(
                          color: _gameActive ? Colors.green : Colors.blue,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.touch_app,
                          size: 100,
                          color: Colors.white,
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                    const Text('Tap to play'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

