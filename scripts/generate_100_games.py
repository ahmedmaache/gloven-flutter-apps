#!/usr/bin/env python3
"""
Generate 100 unique Flutter games with all required features
"""

import subprocess
import json
import os
from pathlib import Path

# 100 unique game ideas
GAMES = [
    # Puzzle Games (1-20)
    (1, "Number Slide Puzzle", "puzzle"),
    (2, "Color Match Challenge", "puzzle"),
    (3, "Word Chain", "puzzle"),
    (4, "Pattern Memory", "puzzle"),
    (5, "Block Rotation", "puzzle"),
    (6, "Sequence Master", "puzzle"),
    (7, "Logic Grid", "puzzle"),
    (8, "Tile Swap", "puzzle"),
    (9, "Path Finder", "puzzle"),
    (10, "Code Breaker", "puzzle"),
    (11, "Shape Matcher", "puzzle"),
    (12, "Number Sequence", "puzzle"),
    (13, "Color Sequence", "puzzle"),
    (14, "Pattern Repeater", "puzzle"),
    (15, "Memory Cards", "puzzle"),
    (16, "Sudoku Lite", "puzzle"),
    (17, "Cross Puzzle", "puzzle"),
    (18, "Link Connect", "puzzle"),
    (19, "Bubble Sort", "puzzle"),
    (20, "Grid Solver", "puzzle"),
    
    # Arcade Games (21-40)
    (21, "Space Shooter", "arcade"),
    (22, "Endless Runner", "arcade"),
    (23, "Snake Classic", "arcade"),
    (24, "Breakout Bricks", "arcade"),
    (25, "Flappy Bird Clone", "arcade"),
    (26, "Doodle Jump", "arcade"),
    (27, "Fruit Slicer", "arcade"),
    (28, "Ball Bounce", "arcade"),
    (29, "Rocket Launch", "arcade"),
    (30, "Asteroid Dodge", "arcade"),
    (31, "Platform Jumper", "arcade"),
    (32, "Car Racing", "arcade"),
    (33, "Helicopter Fly", "arcade"),
    (34, "Submarine Dive", "arcade"),
    (35, "Jet Pack", "arcade"),
    (36, "Space Invaders", "arcade"),
    (37, "Pac-Man Style", "arcade"),
    (38, "Tetris Style", "arcade"),
    (39, "Pong Classic", "arcade"),
    (40, "Pinball", "arcade"),
    
    # Strategy Games (41-55)
    (41, "Tower Defense", "strategy"),
    (42, "Chess Lite", "strategy"),
    (43, "Checkers", "strategy"),
    (44, "Connect Four", "strategy"),
    (45, "Tic Tac Toe Pro", "strategy"),
    (46, "Reversi", "strategy"),
    (47, "Minesweeper", "strategy"),
    (48, "Battleship", "strategy"),
    (49, "Risk Lite", "strategy"),
    (50, "Card Solitaire", "strategy"),
    (51, "Mahjong", "strategy"),
    (52, "Dominoes", "strategy"),
    (53, "Backgammon", "strategy"),
    (54, "Go Lite", "strategy"),
    (55, "Strategy Puzzle", "strategy"),
    
    # Action Games (56-70)
    (56, "Tap Reaction", "action"),
    (57, "Swipe Fighter", "action"),
    (58, "Tap Defender", "action"),
    (59, "Quick Draw", "action"),
    (60, "Target Practice", "action"),
    (61, "Speed Tap", "action"),
    (62, "Reaction Test", "action"),
    (63, "Tap Timing", "action"),
    (64, "Swipe Attack", "action"),
    (65, "Multi Tap", "action"),
    (66, "Rapid Fire", "action"),
    (67, "Combo Master", "action"),
    (68, "Beat Match", "action"),
    (69, "Rhythm Tap", "action"),
    (70, "Action Puzzle", "action"),
    
    # Casual Games (71-85)
    (71, "Bubble Pop", "casual"),
    (72, "Match Three", "casual"),
    (73, "Candy Crush Style", "casual"),
    (74, "Jewel Match", "casual"),
    (75, "Tile Match", "casual"),
    (76, "Color Pop", "casual"),
    (77, "Block Drop", "casual"),
    (78, "Falling Blocks", "casual"),
    (79, "Stack Builder", "casual"),
    (80, "Balance Game", "casual"),
    (81, "Catch Game", "casual"),
    (82, "Throw Game", "casual"),
    (83, "Aim Game", "casual"),
    (84, "Collect Game", "casual"),
    (85, "Sort Game", "casual"),
    
    # Educational Games (86-95)
    (86, "Math Quiz", "educational"),
    (87, "Word Builder", "educational"),
    (88, "Geography Quiz", "educational"),
    (89, "History Quiz", "educational"),
    (90, "Science Quiz", "educational"),
    (91, "Language Learning", "educational"),
    (92, "Memory Trainer", "educational"),
    (93, "Logic Trainer", "educational"),
    (94, "Speed Math", "educational"),
    (95, "Brain Trainer", "educational"),
    
    # Simulation Games (96-100)
    (96, "City Builder Lite", "simulation"),
    (97, "Farm Simulator", "simulation"),
    (98, "Pet Care", "simulation"),
    (99, "Restaurant Manager", "simulation"),
    (100, "Traffic Controller", "simulation"),
]

def main():
    print("Generating 100 unique Flutter games...")
    print("This will take 30-60 minutes...")
    print("")
    
    for app_num, game_name, game_type in GAMES:
        print(f"Creating game {app_num}/100: {game_name} ({game_type})...")
        try:
            subprocess.run(
                ["./scripts/create_game_template.sh", str(app_num), game_name, game_type],
                check=True,
                timeout=300
            )
        except subprocess.TimeoutExpired:
            print(f"⚠️  Timeout creating {game_name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating {game_name}: {e}")
    
    print("")
    print("✅ Game generation complete!")
    print(f"Total games: {len(GAMES)}")

if __name__ == "__main__":
    main()

