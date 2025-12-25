import 'package:audioplayers/audioplayers.dart';
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import '../models/settings.dart';

class SoundManager {
  static final AudioPlayer _player = AudioPlayer();
  static bool _initialized = false;
  
  static Future<void> initialize() async {
    if (!_initialized) {
      await _player.setReleaseMode(ReleaseMode.loop);
      _initialized = true;
    }
  }
  
  static Future<void> playSound(String soundType, BuildContext context) async {
    try {
      final settings = Provider.of<GameSettings>(context, listen: false);
      if (!settings.soundEnabled) return;
      
      // Generate sound based on type
      // In production, load actual sound files
      switch (soundType) {
        case 'tap':
        case 'click':
        case 'success':
        case 'fail':
        case 'gameOver':
        case 'levelUp':
          // Play system sound or loaded audio file
          break;
      }
    } catch (e) {
      // Silent fail - don't crash on sound errors
      debugPrint('Sound error: $e');
    }
  }
  
  static void dispose() {
    _player.dispose();
  }
}

