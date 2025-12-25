import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
import 'dart:math';
import 'dart:async';

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
  
  // Game-specific variables
  // Game state variables
  
  @override
  void initState() {
    super.initState();
    _loadBestScore();
    // Initialize game
  }
  
  Future<void> _loadBestScore() async {
    // Load from SharedPreferences
    setState(() => _bestScore = 0);
  }
  
  Future<void> _saveBestScore() async {
    if (_score > _bestScore) {
      setState(() => _bestScore = _score);
    }
  }
  
  void _startGame() {
    setState(() {
      _gameActive = true;
      _score = 0;
      _gameStatus = 'Playing...';
    });
    // Start game logic
    SoundManager.playSound('success', context);
    VibrationManager.vibrate(context, duration: 100);
  }
  
  void _gameAction() async {
    if (!_gameActive) {
      _startGame();
      return;
    }
    
    try {
      final settings = Provider.of<SettingsProvider>(context, listen: false);
      setState(() { _score++; });
      
      await SoundManager.playSound('tap', context);
      await VibrationManager.vibrate(context, duration: 50);
    } catch (e) {
      debugPrint('Game error: $e');
    }
  }
  
  // Game-specific methods
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Asteroid Dodge'),
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
                    
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _scoreCard(String label, int value) {
    return Column(
      children: [
        Text(label),
        Text(
          '$value',
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }
}
