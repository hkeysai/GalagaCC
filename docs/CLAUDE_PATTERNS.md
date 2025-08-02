# CLAUDE_PATTERNS.md

This file provides guidance to Claude Code for the enemy movement pattern system in Galaga.

## Pattern Engine Architecture

### Core Class: PatternEngine
Location: `source/patterns.py:6`

Manages creation of entrance and attack movement patterns using mathematical curves.

## Entrance Patterns

### Pattern Types
1. **PATTERN_LEFT_SWEEP** (0)
   - Start: Off-screen left (-20, 50 + row*20)
   - Path: Quadratic Bezier curve
   - Control point: 30% screen width, 70% screen height
   - Used for stages: 1, 4, 7, 10...

2. **PATTERN_RIGHT_SWEEP** (1)
   - Start: Off-screen right (width+20, 50 + row*20)
   - Path: Quadratic Bezier curve
   - Control point: 70% screen width, 70% screen height
   - Used for stages: 2, 5, 8, 11...

3. **PATTERN_TOP_CASCADE** (2)
   - Start: Off-screen top (center + col offset, -20)
   - Path: Sine wave with decreasing amplitude
   - Wave frequency: 2 cycles
   - Used for stages: 3, 6, 9, 12...

### Path Generation
```python
create_entrance_path(pattern_type, enemy_index, formation_pos)
```
- Returns list of (x, y) coordinates
- 60-80 steps depending on pattern
- Smooth interpolation using parametric equations

## Attack Patterns

### Dive Pattern Types

#### Zako Dive
```python
_create_zako_dive(start_x, start_y, player_x)
```
- Phase 1 (40%): Dive toward player
- Phase 2 (60%): Loop back up
- Total steps: 120
- Simple, predictable pattern

#### Goei Dive  
```python
_create_goei_dive(start_x, start_y)
```
- Figure-8 pattern with feints
- 4 full sine loops
- Vertical drift toward bottom
- Total steps: 150
- More complex, harder to predict

#### Boss Galaga Dive
```python
_create_boss_dive(start_x, start_y, player_x)
```
- Wide circular arc (1.5π radians)
- Centers between start and player positions
- Descends to 70% screen height
- Total steps: 100
- Sets up for tractor beam position

## Mathematical Foundations

### Bezier Curves (Entrance)
Quadratic Bezier formula:
```
P(t) = (1-t)²P₀ + 2(1-t)t·P₁ + t²P₂
```
Where:
- P₀ = start position
- P₁ = control point
- P₂ = formation position
- t ∈ [0, 1]

### Sine Waves (Cascading/Attacks)
```python
x = base_x + sin(t * π * frequency) * amplitude
y = base_y + t * vertical_distance
```

### Path Following
Enemies follow paths using:
1. Linear interpolation between points
2. Speed-based advancement (2.0 pixels/frame default)
3. Distance threshold checking

## Integration with Formation

### Entrance Integration
1. Formation creates spawn list with delays
2. Each enemy gets unique path based on:
   - Stage pattern type
   - Enemy index (for variety)
   - Target formation position

### Attack Integration  
1. Formation triggers attack waves
2. Pattern engine creates dive path
3. Path considers:
   - Enemy type capabilities
   - Current position
   - Player position (for targeting)

## Pattern Timing

### Entrance Timing
- Path steps spaced for smooth 2-3 second entrance
- Staggered spawning creates wave effect
- All enemies in formation within 10 seconds

### Attack Timing
- Dive duration: 2-4 seconds
- Return to formation if not destroyed
- Cooldown before next attack eligibility

## Customization Points

### Adding New Patterns
1. Define new PATTERN_* constant
2. Add case in `create_entrance_path()`
3. Implement `_create_*_path()` method
4. Update stage rotation logic

### Modifying Existing Patterns
Key parameters to adjust:
- Step count (smoothness vs performance)
- Control points (curve shape)
- Amplitude/frequency (movement intensity)
- Speed factor (pattern duration)

## Common Issues & Solutions

1. **Jerky movement**: Increase step count or check path_speed
2. **Enemies overshoot**: Verify distance threshold in sprite following
3. **Patterns too predictable**: Add randomization to control points
4. **Performance issues**: Reduce step count or pre-calculate paths

## Future Enhancements

Potential improvements:
- Challenging stage patterns (8 unique types)
- Transform patterns (for enemy morphing)
- Capture/rescue patterns
- Dynamic difficulty adjustment