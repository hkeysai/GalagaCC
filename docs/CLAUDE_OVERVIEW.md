# CLAUDE_OVERVIEW.md

This file provides a comprehensive overview of the Galaga clone architecture for Claude Code.

## Project Structure

```
Galaga/
├── galaga.py              # Entry point
├── source/
│   ├── main.py           # Game loop and state management
│   ├── constants.py      # Game constants and configuration
│   ├── states.py         # Base state class and menu states
│   ├── play.py           # Main gameplay state
│   ├── sprites.py        # All sprite classes
│   ├── formation.py      # Enemy formation management
│   ├── patterns.py       # Movement pattern generation
│   ├── setup.py          # Resource loading and initialization
│   ├── tools.py          # Utility functions
│   ├── hud.py            # HUD rendering
│   ├── scoring.py        # High score management
│   └── stars.py          # Background star field
├── resources/
│   ├── graphics/
│   │   └── sheet.png     # Main sprite sheet
│   └── audio/            # Sound effects (OGG format)
└── docs/                 # Claude.md documentation

```

## Core Game Flow

1. **Startup**: `galaga.py` → `main.main()` → `Control` class
2. **State Machine**: Title → Play → GameOver/ScoreEntry → Title
3. **Play State Flow**:
   - Show "START" message
   - Initialize stage
   - Show "STAGE X" 
   - Spawn enemies with entrance patterns
   - Show "READY"
   - Gameplay loop
   - Stage clear → Next stage
   - Game over → State transition

## Key Systems

### Enemy System
- **Types**: Zako (bees), Goei (butterflies), BossGalaga
- **Formation**: 10x5 grid with breathing animation
- **Patterns**: 3 entrance types, enemy-specific dive patterns
- **AI**: Periodic attack waves, targeted firing

### Combat System
- Player missiles: Single shot with cooldown
- Enemy missiles: Aimed at player position
- Collision detection: Rectangle-based
- Scoring: Variable points based on enemy state

### Progression System
- Stages increment when all enemies destroyed
- Difficulty scaling: Faster attacks, more frequent firing
- Enemy variants: Yellow Zako after stage 5
- Stage badges: Visual progression indicator

## Key Classes

### Sprites (`source/sprites.py`)
- `GalagaSprite`: Base class with centered positioning
- `Player`: Arrow key movement, firing
- `Enemy`: Base with pattern following
- `Zako`, `Goei`, `BossGalaga`: Enemy variants
- `Missile`: Velocity-based projectiles
- `Explosion`: Animated destruction effect

### Formation (`source/formation.py`)
- Manages 10x5 enemy grid
- Handles breathing/movement animation
- Triggers attack waves
- Spawns enemies with delays

### Patterns (`source/patterns.py`)
- Creates mathematical movement paths
- Entrance patterns: Left/right sweep, top cascade
- Attack patterns: Enemy-specific dives
- Smooth bezier/sine curve interpolation

### Play State (`source/play.py`)
- Main gameplay logic
- Sub-state management via flags
- Update/display separation
- Collision and scoring

## Data Flow

1. **Input**: pygame events → state.get_event() → player control
2. **Update**: delta_time → state.update() → all game objects
3. **Display**: state.display() → layered rendering → screen
4. **Persist**: State data passed between transitions

## Resource Management

- **Graphics**: Single sprite sheet, coordinate-based extraction
- **Audio**: Preloaded OGG files, played on demand
- **Fonts**: Sprite-based custom font rendering
- **Scores**: Text file persistence

## Common Patterns

### State Blocking
```python
self.blocking_timer = 0
self.should_show_message = True
# In update_timers:
if self.should_show_message:
    self.blocking_timer += delta_time
    if self.blocking_timer >= DURATION:
        self.done_showing_message()
```

### Animation Timing
```python
self.animation_timer += delta_time
if self.animation_timer >= ANIMATION_FREQ:
    self.animation_flag = not self.animation_flag
    self.animation_timer = 0
```

### Object Pooling
- Sprites added/removed from groups
- Reusable explosion/text sprites
- Missile recycling via kill()

## Performance Considerations

- Fixed 30 FPS target
- Sprite groups for batch operations
- Pre-calculated paths
- Minimal file I/O during gameplay

## Extension Points

1. **New Enemy Types**: Inherit from Enemy class
2. **New States**: Inherit from State, add to state_dict
3. **New Patterns**: Add to PatternEngine
4. **Power-ups**: Extend collision system
5. **Multiplayer**: Add second player in Play state

## Debug Features

- K key: Kill player (debug only)
- Score manipulation via persist
- Stage jumping via stage_num
- God mode flags (not implemented)

## Known Limitations

- No pause functionality
- Single player only
- No difficulty settings
- Limited audio channels
- No fullscreen support

This overview provides the essential context for understanding and modifying the Galaga clone codebase.