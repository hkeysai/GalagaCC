# CLAUDE_GAME_STATES.md

This file provides guidance to Claude Code for the game state system in Galaga.

## State Architecture

### Base State Class
Location: `source/states.py:37`

Core properties:
- `persist`: Data that carries between states
- `next_state_name`: Where to transition
- `is_done`: Ready to switch states
- `is_quit`: Exit game
- `current_time`: pygame tick time

Required methods:
- `cleanup()`: Return persist data
- `get_event(event)`: Handle pygame events
- `update(delta_time, keys)`: Update logic
- `display(surface)`: Render state

## State Types

### Title State
Location: `source/states.py:63`

Purpose: Main menu and attract mode
- Shows animated title logo
- Displays high scores
- Handles game start
- Transitions to: PLAY_STATE or DEMO_STATE

Key features:
- Logo color cycling (3 variants)
- Scrolling score display
- Start button flash (12 times @ 150ms)

### Play State  
Location: `source/play.py:22`

Purpose: Main gameplay
- Manages player, enemies, formation
- Handles all game mechanics
- Multiple sub-states via flags

Sub-states managed by flags:
- `is_starting`: Shows "START" message
- `should_show_stage`: Shows "STAGE X"
- `should_show_ready`: Shows "READY"
- `is_ready`: Gameplay active
- `should_show_game_over`: Shows "GAME OVER"

Transitions to:
- GAME_OVER_STATE: When game ends
- SCORE_ENTRY_STATE: For high scores

### Game Over State
Location: `source/states.py` (GameOver class)

Purpose: Show final statistics
- Displays shots fired/hits/ratio
- Duration: 14.5 seconds
- Transitions to: TITLE_STATE

### Score Entry State
Location: `source/states.py` (ScoreEntry class)

Purpose: High score name entry
- 3-letter name input
- Updates score file
- Transitions to: GAME_OVER_STATE

### Demo State
Location: `source/states.py` (Demo class)

Purpose: Attract mode gameplay
- AI-controlled demonstration
- Shows game mechanics
- Transitions to: TITLE_STATE

## State Management

### Control Class
Location: `source/main.py:10`

Manages state transitions:
```python
state_dict = {
    c.TITLE_STATE: Title,
    c.PLAY_STATE: Play,
    c.SCORE_ENTRY_STATE: ScoreEntry,
    c.GAME_OVER_STATE: GameOver,
    c.DEMO_STATE: Demo
}
```

### State Switching
```python
flip_state():
    1. Call cleanup() on current state
    2. Get persist data
    3. Create new state instance
    4. Pass persist data to new state
```

## Persistent Data

### Persist NamedTuple
Location: `source/constants.py:5`

Fields:
- `stars`: StarField instance (background)
- `scores`: List of high scores
- `current_score`: Player's score
- `one_up_score`: Next extra life threshold
- `high_score`: Current session high
- `num_shots`: Total shots fired
- `num_hits`: Total hits
- `stage_num`: Current stage

## Play State Details

### Initialization Sequence
1. `__init__`: Setup game objects
2. `is_starting = True`: Show START
3. `done_starting()`: Spawn player, load stage
4. `should_show_stage = True`: Show stage number
5. `done_showing_stage()`: Start ready sequence
6. `should_show_ready = True`: Show READY
7. `done_with_ready()`: Enable gameplay

### Update Priority
1. Check blocking states (messages)
2. Update timers
3. Update game objects (if not blocked)
4. Check state transitions

### Display Layers (bottom to top)
1. Black background
2. Scrolling stars
3. Enemies
4. Player
5. Player missiles
6. Enemy missiles
7. Explosions
8. Score text sprites
9. HUD (scores, lives, badges)
10. State messages (START, READY, etc.)

## Common State Patterns

### Blocking Messages
Use `blocking_timer` pattern:
```python
self.blocking_timer = DURATION
# In update:
if self.blocking_timer > 0:
    self.blocking_timer -= delta_time
    if self.blocking_timer <= 0:
        self.done_with_message()
```

### Flashing Text
```python
self.flashing_text_timer += delta_time
if self.flashing_text_timer >= TEXT_FLASH_FREQ:
    self.show_text = not self.show_text
    self.flashing_text_timer = 0
```

## State Debugging

Check these when states misbehave:
1. `is_done` flag set properly
2. `next_state_name` assigned
3. `persist` data complete
4. Blocking timers cleared
5. Sub-state flags reset

## Adding New States

1. Create class inheriting from State
2. Implement required methods
3. Add to state_dict in main.py
4. Add constant to constants.py
5. Set up transitions from other states