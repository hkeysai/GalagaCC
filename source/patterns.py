import pygame
import math
from . import constants as c


class PatternEngine:
    """Manages enemy entrance and attack patterns"""
    
    # Entrance pattern types
    PATTERN_LEFT_SWEEP = 0
    PATTERN_RIGHT_SWEEP = 1
    PATTERN_TOP_CASCADE = 2
    
    def __init__(self):
        self.active_patterns = []
        
    def get_entrance_pattern(self, stage_num):
        """Determine which entrance pattern to use based on stage number"""
        # Cycle through 3 patterns
        pattern_index = (stage_num - 1) % 3
        return pattern_index
    
    def create_entrance_path(self, pattern_type, enemy_index, formation_pos):
        """Create an entrance path for an enemy"""
        row, col = formation_pos
        
        if pattern_type == self.PATTERN_LEFT_SWEEP:
            return self._create_left_sweep_path(enemy_index, formation_pos)
        elif pattern_type == self.PATTERN_RIGHT_SWEEP:
            return self._create_right_sweep_path(enemy_index, formation_pos)
        else:  # PATTERN_TOP_CASCADE
            return self._create_top_cascade_path(enemy_index, formation_pos)
    
    def _create_left_sweep_path(self, index, formation_pos):
        """Enemies enter from left side in sweeping motion"""
        row, col = formation_pos
        path = []
        
        # Start position (off-screen left)
        start_x = -20
        start_y = 50 + row * 20
        
        # Create arc path to formation position
        steps = 60
        for i in range(steps):
            t = i / (steps - 1)
            
            # Bezier curve control points
            control_x = c.GAME_SIZE.width * 0.3
            control_y = c.GAME_SIZE.height * 0.7
            
            # Calculate position using quadratic Bezier
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * (c.GAME_SIZE.width // 2)
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * start_y
            
            path.append((int(x), int(y)))
        
        return path
    
    def _create_right_sweep_path(self, index, formation_pos):
        """Enemies enter from right side in sweeping motion"""
        row, col = formation_pos
        path = []
        
        # Start position (off-screen right)
        start_x = c.GAME_SIZE.width + 20
        start_y = 50 + row * 20
        
        # Create arc path to formation position
        steps = 60
        for i in range(steps):
            t = i / (steps - 1)
            
            # Bezier curve control points
            control_x = c.GAME_SIZE.width * 0.7
            control_y = c.GAME_SIZE.height * 0.7
            
            # Calculate position using quadratic Bezier
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * (c.GAME_SIZE.width // 2)
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * start_y
            
            path.append((int(x), int(y)))
        
        return path
    
    def _create_top_cascade_path(self, index, formation_pos):
        """Enemies enter from top in cascading motion"""
        row, col = formation_pos
        path = []
        
        # Start position (off-screen top)
        start_x = c.GAME_SIZE.width // 2 + (col - 5) * 20
        start_y = -20
        
        # Create swooping path to formation position
        steps = 80
        for i in range(steps):
            t = i / (steps - 1)
            
            # Add sine wave for swooping motion
            wave_amplitude = 30
            wave_frequency = 2
            
            x = start_x + math.sin(t * math.pi * wave_frequency) * wave_amplitude * (1 - t)
            y = start_y + t * (100 + row * 20)
            
            path.append((int(x), int(y)))
        
        return path
    
    def create_dive_pattern(self, enemy_type, start_pos, player_pos):
        """Create a diving attack pattern"""
        path = []
        start_x, start_y = start_pos
        player_x, player_y = player_pos
        
        if enemy_type == "zako":
            # Simple dive toward player then loop back
            path = self._create_zako_dive(start_x, start_y, player_x)
        elif enemy_type == "goei":
            # Figure-8 pattern with feints
            path = self._create_goei_dive(start_x, start_y)
        elif enemy_type == "boss_galaga":
            # Looping dive for capture or attack
            path = self._create_boss_dive(start_x, start_y, player_x)
        
        return path
    
    def _create_zako_dive(self, start_x, start_y, player_x):
        """Zako diving pattern - straight down then loop"""
        path = []
        steps = 120
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.4:
                # Dive down toward player
                dive_t = t / 0.4
                x = start_x + (player_x - start_x) * dive_t * 0.5
                y = start_y + dive_t * (c.GAME_SIZE.height - start_y - 50)
            else:
                # Loop back up
                loop_t = (t - 0.4) / 0.6
                angle = loop_t * math.pi
                radius = 40
                x = player_x + math.cos(angle) * radius
                y = c.GAME_SIZE.height - 50 - math.sin(angle) * radius * 2
            
            path.append((int(x), int(y)))
        
        return path
    
    def _create_goei_dive(self, start_x, start_y):
        """Goei diving pattern - figure-8 with feints"""
        path = []
        steps = 150
        
        for i in range(steps):
            t = i / (steps - 1)
            
            # Figure-8 pattern
            angle = t * math.pi * 4  # Two full loops
            radius_x = 50
            radius_y = 80
            
            x = start_x + math.sin(angle) * radius_x
            y = start_y + t * (c.GAME_SIZE.height - start_y) + math.sin(angle * 2) * 20
            
            path.append((int(x), int(y)))
        
        return path
    
    def _create_boss_dive(self, start_x, start_y, player_x):
        """Boss Galaga diving pattern - wide loop"""
        path = []
        steps = 100
        
        for i in range(steps):
            t = i / (steps - 1)
            
            # Wide circular dive
            angle = t * math.pi * 1.5
            radius = 60
            center_x = (start_x + player_x) / 2
            
            x = center_x + math.cos(angle + math.pi/2) * radius
            y = start_y + t * (c.GAME_SIZE.height * 0.7 - start_y)
            
            path.append((int(x), int(y)))
        
        return path