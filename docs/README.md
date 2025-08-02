# Galaga Documentation for Claude Code

This directory contains comprehensive documentation specifically designed for Claude Code to understand and work with the Galaga codebase efficiently.

## Documentation Files

### [CLAUDE_OVERVIEW.md](CLAUDE_OVERVIEW.md)
High-level architecture overview, project structure, and core game flow.

### [CLAUDE_SPRITES.md](CLAUDE_SPRITES.md) 
Complete sprite system documentation including all sprite classes, animation, and collision detection.

### [CLAUDE_FORMATION.md](CLAUDE_FORMATION.md)
Enemy formation grid system, movement patterns, and attack wave management.

### [CLAUDE_PATTERNS.md](CLAUDE_PATTERNS.md)
Mathematical movement pattern generation for entrance and attack behaviors.

### [CLAUDE_GAME_STATES.md](CLAUDE_GAME_STATES.md)
State machine architecture, state transitions, and persistent data management.

### [CLAUDE_AUDIO_SYSTEM.md](CLAUDE_AUDIO_SYSTEM.md)
Sound effect loading, playback, and audio resource management.

### [CLAUDE_HUD_SCORING.md](CLAUDE_HUD_SCORING.md)
HUD rendering, scoring system, and high score persistence.

## Quick Reference

### Key Files
- Entry: `galaga.py`
- Main Loop: `source/main.py`
- Gameplay: `source/play.py`
- Enemies: `source/sprites.py`, `source/formation.py`
- Patterns: `source/patterns.py`

### Important Constants
- Game Size: 224x288 pixels
- FPS: 30
- Formation: 10x5 grid
- Player Speed: 0.085 pixels/ms

### Common Tasks
- Add enemy type: Extend Enemy class in sprites.py
- New pattern: Add to PatternEngine in patterns.py
- New state: Inherit from State, add to state_dict
- Sound effect: Add .ogg to resources/audio/

### Testing
Run `python qa_checker.py` to perform automated quality checks.

## Implementation Status

### Completed ✅
- Enemy types (Zako, Goei, BossGalaga)
- Formation system with breathing
- Entrance patterns (3 types)
- Diving attack patterns
- Enemy firing mechanics
- Collision detection
- Scoring system
- Stage progression
- Difficulty scaling

### Not Implemented ❌
- Boss Galaga tractor beam
- Dual-fighter mode
- Challenging stages
- Enemy transformations
- Pause functionality

## Resources
- Sprite Sheet: `resources/graphics/sheet.png`
- Audio Files: `resources/audio/*.ogg`
- High Scores: `scores.txt`