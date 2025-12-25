import 'package:shared_preferences/shared_preferences.dart';

class GameSettings {
  bool darkMode;
  bool soundEnabled;
  bool vibrationEnabled;
  String difficulty; // 'easy', 'medium', 'hard'
  
  GameSettings({
    this.darkMode = false,
    this.soundEnabled = true,
    this.vibrationEnabled = true,
    this.difficulty = 'medium',
  });
  
  Future<void> save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('darkMode', darkMode);
    await prefs.setBool('soundEnabled', soundEnabled);
    await prefs.setBool('vibrationEnabled', vibrationEnabled);
    await prefs.setString('difficulty', difficulty);
  }
  
  static Future<GameSettings> load() async {
    final prefs = await SharedPreferences.getInstance();
    return GameSettings(
      darkMode: prefs.getBool('darkMode') ?? false,
      soundEnabled: prefs.getBool('soundEnabled') ?? true,
      vibrationEnabled: prefs.getBool('vibrationEnabled') ?? true,
      difficulty: prefs.getString('difficulty') ?? 'medium',
    );
  }
}

