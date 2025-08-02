#!/usr/bin/env python3
"""
Debug runner for Galaga - captures and logs all errors
"""

import sys
import traceback
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('galaga_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Galaga in debug mode...")
    
    try:
        import pygame
        logger.info(f"Pygame version: {pygame.version.ver}")
        
        # Import after pygame to ensure proper initialization order
        from source import main
        
        logger.info("Starting main game loop...")
        main.main()
        
    except Exception as e:
        logger.error(f"Fatal error: {type(e).__name__}: {e}")
        logger.error(traceback.format_exc())
        
        # Keep window open to see error
        input("\nPress Enter to exit...")
        
    finally:
        logger.info("Game shutting down")
        try:
            pygame.quit()
        except:
            pass
        sys.exit()

if __name__ == '__main__':
    main()