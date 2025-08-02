# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running the Game
```bash
python galaga.py
```

### Dependencies
- Python 3.8 or greater
- pygame v1.9.6

Install dependencies:
```bash
pip install pygame==1.9.6
```

## Architecture

### State-Based Game Architecture
The game uses a state machine pattern with the following states:
- **Title State** (Title): Main menu screen
- **Play State** (Play): Main gameplay
- **Game Over State** (GameOver): Shows final score and statistics
- **Score Entry State** (ScoreEntry): High score entry
- **Demo State** (Demo): Attract mode

State transitions are managed by the `Control` class in source/main.py:10, which handles the main game loop, event polling, and state switching.

### Core Components

**Entry Point**: galaga.py - Simple launcher that calls main.main()

**State Management**: 
- Base State class (source/states.py:37) defines interface for all game states
- Persistent data between states via `Persist` namedtuple (source/constants.py:5)
- States communicate through cleanup() returning persist data

**Game Loop** (source/main.py:46):
- Fixed 30 FPS (constants.py:56)
- Delta time based updates
- Event polling and key state tracking
- Automatic state transitions when state.is_done = True

**Sprite System**:
- Base class `GalagaSprite` (source/sprites.py:8) provides centered positioning and image flipping
- Player sprite with keyboard controls (source/sprites.py:60)
- Enemy sprites with animation frames

**Resource Loading** (source/setup.py):
- Loads all graphics from resources/graphics/
- Loads all sounds from resources/audio/
- Sprite sheet based graphics (sheet.png)
- Font rendering from sprite sheet

**Game Constants** (source/constants.py):
- Game dimensions: 224x288 pixels
- Named tuples for Point, Rectangle, Area
- Color definitions
- Timing constants

### Key Gameplay Elements

**Play State** (source/play.py:22):
- Player lives and respawning
- Enemy formation with spread/offset animation
- Missile collision detection
- Stage progression
- Score tracking

**Scoring System**:
- Persistent high scores in scores.txt
- Hit/miss ratio tracking
- Stage badges for milestones

**Controls**:
- Arrow keys: Move ship
- Space: Fire missile
- Enter: Start/select