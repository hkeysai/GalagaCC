# CLAUDE_SCALING.md

This file documents the display scaling system for Galaga.

## Display Scaling System

The game now supports display scaling to accommodate modern high-resolution screens.

### Configuration
Location: `source/constants.py`

```python
DISPLAY_SCALE = 3  # Scale factor (1-5 recommended)
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
   - 2x (448x576) - Small laptops
   - 3x (672x864) - 13" MacBook Pro (default)
   - 4x (896x1152) - Larger displays
   - 5x (1120x1440) - 4K displays

### Technical Details

- Scaling uses `pygame.transform.scale()`
- Integer scaling preserves pixel art
- All game logic uses original coordinates
- Mouse/input automatically scaled (if needed)

### Performance

- Minimal overhead from scaling
- Hardware accelerated on most systems
- No impact on 30 FPS target