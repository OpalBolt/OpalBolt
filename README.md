<div align="center">

# 🚧 Welcome to OpalBolt's GitHub Profile 🚧

  
  ![Profile Status](https://img.shields.io/badge/Status-Under%20Construction-yellow)
  ![Python](https://img.shields.io/badge/Python-3.13-blue)
  ![Hobby Projects](https://img.shields.io/badge/Hobby%20Projects-In%20Progress-brightgreen)

  **Hi there! I'm OpalBolt, and I'm building something fun here!**
  
</div>

## 🎮 Coming Soon: 10,000 Dice Game via GitHub Issues

I'm working on an interactive GitHub experience that will let you play the classic 10,000 dice game directly through GitHub Issues!

## 🎮 How It Will Work

This will be an **always-running** implementation of the classic 10,000 dice game that lets players interact through GitHub Issues. The game state will be persisted in JSON files and displayed live in this README.

### 🕹️ Player Commands

| Command | Example | Description |
|---------|---------|-------------|
| `-keep` | `-keep 1 5 1` | Keep these dice and end the round |
| `-roll` | `-roll 1 5 1` | Keep these dice and roll again |
| `-help` | `-help` | Display game rules and close the issue |

## 🎲 Game Status

### Current Game

🎲 **Current Dice**: *Loading...*

✅ **Possible dice kept this turn**: *None*

💯 **Round Score**: 0 | **Game Score**: 0

### Previous Turn

🎮 **Player**: *No previous turns yet*

🎲 **Dice Rolled**: *None*

🎯 **Dice Kept**: *None*

📊 **Score Earned**: 0

## 🏆 Scoring

- Single 1: **100 points**
- Single 5: **50 points**
- Three 1s: **1000 points**
- Three of a kind (2-6): **number × 100 points**
- Four or more of a kind: **doubles for each extra die**
- Straight (1-2-3-4-5-6): **1500 points**
- Three pairs: **1000 points**

> **Note**: You must score at least 800 points in a single turn to get "on the board"

## 📋 How To Play

1. Visit this README page when the game is active
2. Comment on this repository with your move (`-roll` or `-keep` followed by dice values)
3. The GitHub Action will process your move and update the game state
4. The README will update to show the current game status
5. Player with the highest score above 10,000 wins!

## 🧠 Technical Details

This game is built using:

- Python with Pydantic for data models
- GitHub Actions for automation (coming soon)
- JSON files for state persistence
- Markdown for dynamic display

## ⚙️ Project Architecture

```
src/
├── game.py          # Main game controller
├── game_logic.py    # Core dice & scoring logic
├── models.py        # Data models
├── player_logic.py  # Player interaction
└── oponent_logic.py # Computer player logic
```

## 🔗 Links

- [Game Rules](https://github.com/OpalBolt/10000-dice-game/blob/main/game-directions.txt)
- [Project Instructions](https://github.com/OpalBolt/10000-dice-game/blob/main/instruction.txt)

---

<div align="center">
  
  Made with ❤️ by [OpalBolt](https://github.com/OpalBolt)
  
</div>