import 'package:flutter/foundation.dart';
import '../models/settings.dart';

class SettingsProvider with ChangeNotifier {
  GameSettings _settings = GameSettings();
  
  GameSettings get settings => _settings;
  
  bool get darkMode => _settings.darkMode;
  bool get soundEnabled => _settings.soundEnabled;
  bool get vibrationEnabled => _settings.vibrationEnabled;
  String get difficulty => _settings.difficulty;
  
  Future<void> loadSettings() async {
    _settings = await GameSettings.load();
    notifyListeners();
  }
  
  Future<void> toggleDarkMode() async {
    _settings.darkMode = !_settings.darkMode;
    await _settings.save();
    notifyListeners();
  }
  
  Future<void> toggleSound() async {
    _settings.soundEnabled = !_settings.soundEnabled;
    await _settings.save();
    notifyListeners();
  }
  
  Future<void> toggleVibration() async {
    _settings.vibrationEnabled = !_settings.vibrationEnabled;
    await _settings.save();
    notifyListeners();
  }
  
  Future<void> setDifficulty(String difficulty) async {
    _settings.difficulty = difficulty;
    await _settings.save();
    notifyListeners();
  }
}

