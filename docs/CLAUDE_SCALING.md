# CLAUDE_SCALING.md

This file documents the display scaling system for Galaga.

## Recent Updates
- Fixed 10-second crash issue by improving scaling implementation
- Changed default scale from 3x to 2x for better stability
- Updated scaling to use `pygame.transform.scale()` with destination surface
- Added `pygame.event.pump()` for macOS compatibility

## Display Scaling System

The game now supports display scaling to accommodate modern high-resolution screens.

### Configuration
Location: `source/constants.py`

```python
DISPLAY_SCALE = 2  # Scale factor (1-5 recommended, default now 2x)
```

### How It Works

1. **Original Resolution**: 224x288 pixels (classic arcade)
2. **Scaled Display**: DISPLAY_SCALE × original (default 3x = 672x864)
3. **Rendering Pipeline**:
   - Game renders to GAME_SURFACE at original resolution
   - GAME_SURFACE scaled up to display resolution
   - Final output shown on SCREEN

### Benefits

- Pixel-perfect scaling (no blurring)
- Maintains original game logic coordinates
- Easy to adjust for different displays
- No impact on gameplay mechanics

### Changing Scale

To adjust for your display:
1. Edit `DISPLAY_SCALE` in constants.py
2. Recommended values:
   - 2x (448x576) - Default, stable on all systems
   - 3x (672x864) - Larger displays
   - 4x (896x1152) - Very large displays
   - 5x (1120x1440) - 4K displays

### Technical Details

- Scaling uses `pygame.transform.scale(GAME_SURFACE, size, SCREEN)`
- Direct destination surface rendering (more stable)
- Integer scaling preserves pixel art
- All game logic uses original coordinates
- Added `pygame.event.pump()` for macOS event handling
- Changed from `pygame.display.update()` to `pygame.display.flip()`

### Performance

- Minimal overhead from scaling
- Hardware accelerated on most systems
- No impact on 30 FPS target
- Fixed delta time clamping to prevent runaway values

### Implementation (source/main.py)

```python
# Render to game surface at original resolution
self.state.display(setup.GAME_SURFACE)

# Scale directly to screen (stable method)
pygame.transform.scale(setup.GAME_SURFACE, c.DEFAULT_SCREEN_SIZE, self.screen)
pygame.display.flip()

# Keep macOS happy
pygame.event.pump()
```