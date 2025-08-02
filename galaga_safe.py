#!/usr/bin/env python3
"""
Safe launcher for Galaga with crash protection
"""

import os
import sys

# Set SDL audio driver to avoid macOS issues
os.environ['SDL_AUDIODRIVER'] = 'coreaudio'

# Ensure we're in the right directory
if os.path.exists('galaga.py'):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    import pygame
    
    # Pre-initialize mixer with safe settings for macOS
    pygame.mixer.pre_init(
        frequency=22050,    # Lower frequency for compatibility
        size=-16,           # 16-bit
        channels=2,         # Stereo
        buffer=1024         # Larger buffer to prevent underruns
    )
    
    from source import main
    
    print("Starting Galaga...")
    print(f"Pygame version: {pygame.version.ver}")
    print(f"SDL version: {pygame.version.SDL}")
    
    main.main()
    
except KeyboardInterrupt:
    print("\nGame interrupted by user")
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        pygame.quit()
    except:
        pass
    sys.exit()