# CLAUDE_FORMATION.md

This file provides guidance to Claude Code for the enemy formation system in Galaga.

## Formation Architecture

### Core Class: Formation
Location: `source/formation.py:8`

Manages the 10x5 enemy grid and coordinated movements.

## Grid Layout

```
Row 0: [-, -, -, B, B, B, B, -, -, -]  (Boss Galagas in center)
Row 1: [G, G, G, G, G, G, G, G, G, G]  (Goei - red/white alternating)
Row 2: [G, G, G, G, G, G, G, G, G, G]  (Goei - red/white alternating)
Row 3: [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]  (Zako - blue/yellow)
Row 4: [Z, Z, Z, Z, Z, Z, Z, Z, Z, Z]  (Zako - blue/yellow)
```

- B = Boss Galaga (positions 3-6 only)
- G = Goei (full rows)
- Z = Zako (full rows)

## Movement System

### Formation Breathing
- Horizontal spread oscillates between `FORMATION_MIN_SPREAD` (4) and `FORMATION_MAX_SPREAD` (8)
- Cycle time: 8000ms (`FORMATION_CYCLE_TIME`)
- Spread calculation based on column distance from center

### Horizontal Movement
- Sinusoidal movement with amplitude `FORMATION_MAX_X` (16 pixels)
- Synchronized with breathing cycle

### Position Calculation
```python
get_position(row, col) -> (x, y)
```
- Base position + formation offsets + spread effect
- Only applies to enemies not attacking or entering

## Entrance System

### Pattern Types
1. `PATTERN_LEFT_SWEEP` (0): Enemies enter from left with arc motion
2. `PATTERN_RIGHT_SWEEP` (1): Enemies enter from right with arc motion  
3. `PATTERN_TOP_CASCADE` (2): Enemies cascade from top with sine wave

### Spawn Timing
- Boss Galagas: 100ms delay between spawns
- Regular enemies: 50ms delay between spawns
- Managed through `enemies_to_spawn` queue

### Stage Pattern Selection
```python
pattern_type = (stage_num - 1) % 3
```

## Attack System

### Attack Waves
- Triggered every `attack_frequency` ms (3000ms base)
- Frequency increases with difficulty
- 1-3 enemies attack per wave

### Attack Types
1. **Boss Attack** (1/3 chance when available)
   - Boss Galaga + 0-2 Goei escorts
   - Coordinated dive patterns
   - Escort count affects Boss points

2. **Regular Attack**
   - Random selection of 1-3 available enemies
   - Individual dive patterns per enemy type

### Attack Selection Logic
```python
trigger_attack_wave(player_pos):
    1. Get available enemies (not attacking/entering)
    2. Check for Boss attack opportunity
    3. Otherwise select random enemies
    4. Create dive patterns targeting player
```

## Difficulty Scaling

### set_difficulty(stage_num)
Adjusts two parameters:

1. **Attack Frequency**
   - Base: 3000ms
   - Reduction: 100ms per stage
   - Minimum: 1000ms

2. **Enemy Fire Rates**
   - Reduction: 50ms per stage (max 500ms)
   - Minimum cooldown: 500ms

## Enemy Management

### Grid Operations
- `get_enemy_at(row, col)`: Safe grid access
- `remove_enemy(enemy)`: Removes from grid and sprite group
- `get_escort_candidates(boss)`: Finds nearby Goei for escort

### Formation States
- `is_empty()`: Check if all enemies destroyed
- `clear()`: Reset formation (between stages)

## Integration Points

### With Play State
- Called from `play.py:update_enemies()`
- Receives player position for targeting
- Manages all enemy movement when not individually controlled

### With Pattern Engine
- Uses `PatternEngine` for entrance/attack paths
- Delegates path creation to pattern system

### With Sprites
- Sets `is_entering`/`is_attacking` flags
- Assigns paths via `set_entrance_path()`/`start_attack()`
- Updates positions only for idle enemies

## Common Issues & Solutions

1. **Enemies stuck entering**: Check `enemies_to_spawn` cleared properly
2. **No attacks**: Verify `attack_timer` incrementing after spawns complete
3. **Formation drift**: Ensure `cycle_time` not reset inadvertently
4. **Escort selection**: Confirm Goei in correct rows (1-2) for Boss escorts