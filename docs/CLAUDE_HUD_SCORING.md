# CLAUDE_HUD_SCORING.md

This file provides guidance to Claude Code for the HUD and scoring systems in Galaga.

## HUD System

### HUD Module
Location: `source/hud.py`

Main function:
```python
display(screen, one_up_score, high_score, offset_y, 
        num_extra_lives, stage_badges, stage_badge_animation_step, 
        show_1up)
```

### HUD Elements

#### Score Display
- Position: Top of screen
- Format: Right-aligned, 6 digits with spaces
- Colors: 
  - "1UP": Flashing red/white
  - Score numbers: White
  - "HI-SCORE": Red label, yellow number

#### Lives Display  
- Position: Bottom left
- Shows ship icons for extra lives
- Maximum display: 7 ships

#### Stage Badges
- Position: Bottom right
- Badge types with point values:
  - Stage 1: 10 points
  - Stage 5: 50 points  
  - Stage 10: 100 points
  - Stage 20: 200 points
  - Stage 30: 300 points
  - Stage 50: 500 points
- Animated appearance

## Scoring System

### Score Values

#### Enemy Points
In Formation / While Attacking:
- Zako: 50 / 100
- Goei: 80 / 160  
- Boss Galaga: 150 / 400-1600

Boss Galaga scoring:
- No escorts: 400
- 1 escort: 800
- 2 escorts: 1600

#### Bonus Points
- Challenging stage per enemy: 100
- Perfect challenging stage: 10,000
- Special transforms: 1000-3000

### Score Management

#### Score Tracking
Location: `source/play.py`

Variables:
- `self.score`: Current score
- `self.high_score`: Session high score
- `self.one_up_score`: Next extra life threshold

#### Score Display
- Uses custom sprite font
- Right-aligned with space padding
- Updates immediately on point award

### High Score System

#### Score File
Location: `scores.txt`

Format:
```
name score
ABC 20000
DEF 15000
...
```

#### Score Loading
Location: `source/scoring.py:load_scores()`
- Reads top 5 scores
- Returns list of Score namedtuples
- Creates default scores if file missing

#### Score Saving  
Location: `source/scoring.py:save_scores()`
- Sorts by score descending
- Saves top 5 only
- Overwrites file completely

### Extra Lives

#### Thresholds
- Default: Every 30,000 points
- Configurable via constants

#### Award Logic
```python
if self.score >= self.one_up_score:
    self.extra_lives += 1
    self.one_up_score += 30000
    play_sound("extra_life")
```

## Visual Effects

### Score Popup Text
Location: `source/sprites.py:ScoreText`

Features:
- Shows points for high-value kills
- Rises and fades over 60 frames
- Yellow color
- Only for 800+ point values

### Stage Badge Animation
- Sequential appearance
- 200ms per badge (`STAGE_BADGE_DURATION`)
- Right-to-left order

### Flashing 1UP
- Controlled by `show_1up_text` flag
- Toggles every 300ms (`TEXT_FLASH_FREQ`)
- Red when visible

## Integration Points

### With Play State
- HUD updated every frame
- Score incremented on enemy kills
- Lives decremented on death
- Badges updated on stage change

### With Game Over State
- Final statistics displayed:
  - Shots fired
  - Number of hits
  - Hit-miss ratio
- Color coded messages

## Number Formatting

### Format Strings
```python
ONE_UP_NUM_FORMAT = '{: =6}'      # Right-align, space-pad
HI_SCORE_NUM_FORMAT = '{: =6}'    # Same format
STAGE_FORMAT_STR = 'STAGE {: =3}' # 3-digit stage
```

### Custom Font
- Sprite-based rendering
- Fixed-width characters
- Supports 0-9, A-Z, some symbols

## Common Issues & Solutions

1. **Score not updating**: Check score assignment after enemy.get_points()
2. **Lives not showing**: Verify num_extra_lives passed to HUD
3. **Badges wrong**: Check calc_stage_badges() logic
4. **Text not flashing**: Verify timer increments and TEXT_FLASH_FREQ

## Future Enhancements

Potential improvements:
- Combo multipliers
- Score achievement popups
- Detailed statistics tracking
- Difficulty-based scoring
- Online leaderboards