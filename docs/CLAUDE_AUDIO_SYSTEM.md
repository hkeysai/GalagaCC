# CLAUDE_AUDIO_SYSTEM.md

This file provides guidance to Claude Code for the audio system in Galaga.

## Audio Architecture

### Sound Loading
Location: `source/setup.py:50`

All sounds loaded at startup:
```python
SOUNDS = load_all_sfx(os.path.join(c.RESOURCE_DIR, "audio"), (".ogg",))
```

### Sound Files

Located in `resources/audio/`:

#### Game Flow Sounds
- `start.ogg`: Game start
- `theme.ogg`: Main theme music
- `theme_echoed.ogg`: Theme variation
- `wait.ogg`: Waiting/idle sound
- `game_over.ogg`: Game over
- `new_high_score.ogg`: High score achieved

#### Combat Sounds
- `fighter_fire.ogg`: Player shooting
- `enemy_fire.ogg`: Enemy shooting
- `enemy_hit_1.ogg`: Regular enemy hit
- `enemy_hit_2.ogg`: Boss Galaga damaged (not destroyed)
- `enemy_hit_3.ogg`: Boss Galaga destroyed
- `explosion.ogg`: Player destroyed

#### Special Sounds  
- `tractor_beam.ogg`: Boss Galaga capture beam
- `fighter_captured.ogg`: Player captured
- `fighter_returned.ogg`: Player rescued
- `challenge.ogg`: Challenging stage start
- `perfect_challenge.ogg`: Perfect bonus
- `stage_award.ogg`: Stage complete

#### Bonus Sounds
- `streak.ogg`: Hit streak bonus
- `flag_ship_1.ogg`: Special enemy variant 1
- `flag_ship_2.ogg`: Special enemy variant 2

## Sound Playback

### Helper Functions
Location: `source/setup.py`

```python
play_sound(name):
    - Plays sound if it exists in SOUNDS dict
    - No error if sound missing

stop_sounds():
    - Stops all currently playing sounds
```

### Usage Examples

#### In Play State
```python
# Player actions
play_sound("fighter_fire")  # When shooting

# Enemy hits
play_sound("enemy_hit_1")  # Regular enemy
play_sound("enemy_hit_2")  # Boss damaged
play_sound("enemy_hit_3")  # Boss destroyed

# Player death
play_sound("explosion")
```

## Sound Timing

### Title State
- Theme music on loop
- Start sound when game begins

### Play State  
- Stage start: Brief jingle
- Combat: Individual sound effects
- Game over: Stop all, play game over

### Challenging Stages
- Special challenge music
- Perfect clear sound if all enemies destroyed

## Implementation Details

### Sound Format
- All sounds in OGG format
- Compressed for smaller file size
- Compatible across platforms

### Volume Management
- Currently uses pygame defaults
- No in-game volume control
- Could add to settings

### Channel Management
- Pygame handles channel allocation
- Multiple sounds can play simultaneously
- No explicit channel limits

## Common Issues & Solutions

1. **Sound not playing**
   - Check file exists in resources/audio/
   - Verify .ogg extension
   - Ensure SOUNDS dict loaded

2. **Sound delays**
   - Preload all sounds at startup
   - Use smaller file sizes
   - Check system audio latency

3. **Overlapping sounds**
   - Use stop_sounds() for exclusive sounds
   - Let pygame manage concurrent effects

## Missing Sound Implementations

Currently not implemented:
- Tractor beam sequence
- Capture/rescue sounds
- Challenging stage music
- Hit streak sounds
- Transform enemy sounds

## Adding New Sounds

1. Add .ogg file to resources/audio/
2. Use descriptive filename
3. Call with play_sound("filename")
4. No code changes needed

## Audio Best Practices

1. Keep sound effects short (<1 second)
2. Use consistent volume levels
3. Avoid jarring frequency changes
4. Test on different systems
5. Provide audio feedback for all actions