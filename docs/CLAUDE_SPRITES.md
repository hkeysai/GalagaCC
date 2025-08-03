# CLAUDE_SPRITES.md

This file provides guidance to Claude Code for the sprite system in Galaga.

## Recent Updates
- Implemented continuous shooting when holding spacebar
- Added enemy firing pause when player dies
- Boss Galaga now requires 2 hits to destroy

## Sprite Architecture

### Base Class: GalagaSprite
Location: `source/sprites.py:8`

Core features:
- Centered positioning system (x,y properties map to rect.centerx/centery)
- Image offset support for sprite alignment
- Visibility toggling
- Horizontal/vertical flipping
- Base for all game sprites

### Player Sprite
Location: `source/sprites.py:60`

- Size: 14x12 hitbox (16x16 sprite)
- Movement: Controlled by arrow keys with speed `c.PLAYER_SPEED`
- Sprite sheet position: (96, 0)

### Enemy System

#### Base Enemy Class
Location: `source/sprites.py:75`

Key properties:
- `is_attacking`: Whether enemy is diving
- `is_entering`: Whether enemy is entering formation
- `formation_pos`: (row, col) grid position
- `entrance_path`/`attack_path`: Movement patterns
- `fire_cooldown`: Time between shots
- Pattern following with path interpolation

#### Enemy Types

**Zako** (source/sprites.py:206)
- Bee-like enemies, most common
- Points: 50 (formation) / 100 (attacking)
- Variants: blue (stages 1-5), yellow (stage 6+)
- Fire cooldown: 2000ms base

**Goei** (source/sprites.py:233)
- Butterfly escorts for Boss Galaga
- Points: 80 (formation) / 160 (attacking)
- Variants: red, white (alternating)
- Fire cooldown: 1500ms base
- Can escort Boss Galaga

**BossGalaga** (source/sprites.py:261)
- Large enemies, top formation row
- Points: 150 (formation) / 400-1600 (based on escorts)
- Takes 2 hits: green → purple → destroyed
  - Implemented with `hits_remaining` counter
  - Color changes on first hit
- Cannot fire missiles (uses tractor beam)
- Tracks captured fighters

### Projectiles

**Missile** (source/sprites.py:309)
- Size: 2x10 hitbox (3x8 sprite)
- Velocity-based movement
- Different sprites for player/enemy missiles
- Enemy missiles: (246, 51), Player missiles: (246, 67)

### Effects

**Explosion** (source/sprites.py:317)
- Player explosions: 4 frames @ 140ms each
- Enemy explosions: 5 frames @ 120ms each
- Auto-removes after animation

**ScoreText** (source/sprites.py:314)
- Displays point values for high-value targets
- Rises and fades over 60 frames

## Sprite Sheet Layout

The game uses a single sprite sheet (`resources/graphics/sheet.png`) with:
- Enemy sprites: rows starting at y=80, y=96
- Player sprite: (96, 0)
- Missiles: x=246
- Explosions: various positions
- Font characters: y=224-240

## Animation System

- Enemies animate on `animation_flag` (toggles every 800ms)
- 2-frame animations for all enemy types
- Frame switching handled in Enemy.update()

## Key Methods

### Enemy Pattern Following
- `set_entrance_path()`: Initialize entrance animation
- `start_attack()`: Begin dive attack
- `_follow_entrance_path()`: Smooth path interpolation
- `should_fire()`: Firing logic based on position/cooldown

### Collision Detection
All sprites use pygame.Rect for collision:
- Player: 14x12 centered hitbox
- Enemies: 16x16 hitbox
- Missiles: 2x10 hitbox

## Common Issues & Solutions

1. **Sprite alignment**: Use `image_offset_x/y` for fine-tuning
2. **Animation sync**: Check `animation_flag` timing in constants
3. **Path following**: Ensure `path_speed` is appropriate for frame rate
4. **Firing accuracy**: Account for player movement in targeting