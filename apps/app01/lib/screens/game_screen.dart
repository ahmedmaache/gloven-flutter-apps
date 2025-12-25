import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../utils/sound_manager.dart';
import '../utils/vibration_manager.dart';
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
  List<int> _puzzle = []; int _emptyIndex = 0; int _size = 3;
  
  @override
  void initState() {
    super.initState();
    _loadBestScore();
    _initializePuzzle();
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
      
      setState(() {
        _score++;
        _gameStatus = 'Score: $_score';
      });
      
      await SoundManager.playSound('tap', context);
      await VibrationManager.vibrate(context, duration: 50);
    } catch (e) {
      debugPrint('Game error: $e');
    }
  }
  
  
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
  
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Number Slide Puzzle'),
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
