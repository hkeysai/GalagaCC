# CLAUDE_FORMATION.md

This file provides guidance to Claude Code for the enemy formation system in Galaga.

## Recent Updates
- Added stage-specific entrance patterns based on STAGES.MD documentation
- Implemented Stage 1 and Stage 2 unique entrance groups
- Added challenging stage support (stages 3, 7, 11, etc.)
- Patterns now cycle with increased difficulty after stage 2

## Formation Architecture

### Core Classes
1. **Formation** (`source/formation.py:8`) - Manages the 10x5 enemy grid
2. **StagePatterns** (`source/stage_patterns.py`) - Stage-specific entrance patterns
3. **ChallengingStage** (`source/challenging_stage.py`) - Bonus round patterns

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

### Stage 1 Groups (source/stage_patterns.py)
1. **Group 1**: Boss & Escorts (Left) - Clockwise loop from top-left
2. **Group 2**: Boss & Escorts (Right) - Counter-clockwise from top-right
3. **Group 3**: Bee Squadron (Left) - Enter top-left, bank right
4. **Group 4**: Bee Squadron (Right) - Enter top-right, bank left
5. **Group 5**: Butterfly Squadron - Single file loop from left
6. **Group 6**: Final Bosses - Pairs from top center

### Stage 2 Groups
1. **Group 1**: Bee Squadron - Enter from bottom-left, fly up edge
2. **Group 2**: Bee Squadron - Enter from bottom-right, fly up edge
3. **Group 3**: Butterfly Squadron - Top-left with sharp loop
4. **Group 4**: Butterfly Squadron - Top-right with sharp loop
5. **Group 5**: The Bosses - Single file from top, split into pairs

### Stage Cycling
- Stages 1-2: Unique patterns
- Stage 3: Challenging stage (bonus)
- Stage 4+: Cycle patterns with increased difficulty
- Pattern formula: `((stage_num - 4) % 10) + 1`

### Spawn Timing
- Group-based delays (0-2500ms)
- Within-group stagger: 50ms between enemies
- Managed through `enemies_to_spawn` queue

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

## Challenging Stages

### Stage Numbers
- First: Stage 3
- Pattern: Every 4 stages (3, 7, 11, 15...)
- Formula: `stage_num == 3 or (stage_num - 3) % 4 == 0`

### Wave Structure (40 enemies total)
1. **Wave 1**: Left-Side Weave (8 enemies)
2. **Wave 2**: Right-Side Weave (8 enemies)
3. **Wave 3**: Center Loop Left (4 enemies)
4. **Wave 4**: Center Loop Right (4 enemies)
5. **Wave 5**: Boss Escort Columns (8 enemies)

### Special Rules
- No enemy firing
- No tractor beams
- No player collision
- Perfect bonus: 10,000 points for all 40 destroyed
- Fixed point values: 100 (Bee/Butterfly), 200 (Boss)

## Common Issues & Solutions

1. **Enemies stuck entering**: Check `enemies_to_spawn` cleared properly
2. **No attacks**: Verify `attack_timer` incrementing after spawns complete
3. **Formation drift**: Ensure `cycle_time` not reset inadvertently
4. **Escort selection**: Confirm Goei in correct rows (1-2) for Boss escorts
5. **Stage patterns wrong**: Verify stage cycling formula accounts for challenging stages