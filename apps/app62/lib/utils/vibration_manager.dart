import 'package:vibration/vibration.dart';
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import '../models/settings.dart';

class VibrationManager {
  static Future<void> vibrate(BuildContext context, {int duration = 50}) async {
    try {
      final settings = Provider.of<GameSettings>(context, listen: false);
      if (!settings.vibrationEnabled) return;
      
      if (await Vibration.hasVibrator() ?? false) {
        await Vibration.vibrate(duration: duration);
      }
    } catch (e) {
      // Silent fail - don't crash on vibration errors
      debugPrint('Vibration error: $e');
    }
  }
  
  static Future<void> vibratePattern(BuildContext context, List<int> pattern) async {
    try {
      final settings = Provider.of<GameSettings>(context, listen: false);
      if (!settings.vibrationEnabled) return;
      
      if (await Vibration.hasVibrator() ?? false) {
        await Vibration.vibrate(pattern: pattern);
      }
    } catch (e) {
      debugPrint('Vibration pattern error: $e');
    }
  }
}

