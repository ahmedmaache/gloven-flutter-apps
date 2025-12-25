// Template for puzzle games
// This will be customized for each puzzle game

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
import 'dart:math';

class PuzzleGameScreen extends StatefulWidget {
  final String gameName;
  final List<String> instructions;
  final Function(BuildContext, SettingsProvider) gameLogic;
  
  const PuzzleGameScreen({
    super.key,
    required this.gameName,
    required this.instructions,
    required this.gameLogic,
  });

  @override
  State<PuzzleGameScreen> createState() => _PuzzleGameScreenState();
}

class _PuzzleGameScreenState extends State<PuzzleGameScreen> {
  int _score = 0;
  int _bestScore = 0;
  bool _gameActive = false;
  String _status = 'Tap to Start';
  
  @override
  void initState() {
    super.initState();
    _loadBestScore();
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
      _status = 'Playing...';
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
      final settings = Provider.of<SettingsProvider>(context, listen: false);
      await widget.gameLogic(context, settings);
      
      setState(() {
        _score++;
        _status = 'Score: $_score';
      });
      
      await SoundManager.playSound('tap', context);
      await VibrationManager.vibrate(context, duration: 50);
    } catch (e) {
      debugPrint('Game error: $e');
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.gameName),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
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
                  _scoreCard('Score', _score),
                  _scoreCard('Best', _bestScore),
                ],
              ),
            ),
            // Game Area
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(_status, style: Theme.of(context).textTheme.headlineMedium),
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
        Text('$value', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
      ],
    );
  }
}

