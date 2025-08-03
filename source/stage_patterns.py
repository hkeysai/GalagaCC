"""
Stage-specific entrance patterns based on STAGES.MD documentation
"""
import math
from . import constants as c


class StagePatterns:
    """Implements the specific entrance patterns for each stage as documented"""
    
    @staticmethod
    def get_stage_1_groups():
        """
        Stage 1 entrance groups:
        - Group 1: Boss & Escorts (Left) - 1 Boss, 2 Butterflies
        - Group 2: Boss & Escorts (Right) - 1 Boss, 2 Butterflies  
        - Group 3: Bee Squadron (Left) - 8 Bees
        - Group 4: Bee Squadron (Right) - 8 Bees
        - Group 5: Butterfly Squadron (Looping) - 8 Butterflies
        - Group 6: Final Bosses - 4 Boss Galagas
        """
        groups = []
        
        # Group 1: Boss & Escorts (Left)
        groups.append({
            'enemies': [
                {'type': 'boss_galaga', 'row': 0, 'col': 6},  # Top-right
                {'type': 'goei', 'row': 1, 'col': 6},
                {'type': 'goei', 'row': 1, 'col': 7}
            ],
            'pattern': 'boss_escort_left',
            'delay': 0
        })
        
        # Group 2: Boss & Escorts (Right)
        groups.append({
            'enemies': [
                {'type': 'boss_galaga', 'row': 0, 'col': 3},  # Top-left
                {'type': 'goei', 'row': 1, 'col': 2},
                {'type': 'goei', 'row': 1, 'col': 3}
            ],
            'pattern': 'boss_escort_right',
            'delay': 500
        })
        
        # Group 3: Bee Squadron (Left)
        bee_positions_left = []
        for row in range(3, 5):  # Bottom 2 rows
            for col in range(5, 10):  # Right half
                bee_positions_left.append({'type': 'zako', 'row': row, 'col': col})
        groups.append({
            'enemies': bee_positions_left[:8],
            'pattern': 'bee_squadron_left',
            'delay': 1000
        })
        
        # Group 4: Bee Squadron (Right)
        bee_positions_right = []
        for row in range(3, 5):  # Bottom 2 rows
            for col in range(0, 5):  # Left half
                bee_positions_right.append({'type': 'zako', 'row': row, 'col': col})
        groups.append({
            'enemies': bee_positions_right[:8],
            'pattern': 'bee_squadron_right',
            'delay': 1500
        })
        
        # Group 5: Butterfly Squadron (Looping)
        butterfly_positions = []
        for row in range(1, 3):  # Middle 2 rows
            for col in range(0, 5):  # Left half
                if (row, col) not in [(1, 2), (1, 3)]:  # Skip already placed
                    butterfly_positions.append({'type': 'goei', 'row': row, 'col': col})
        groups.append({
            'enemies': butterfly_positions[:8],
            'pattern': 'butterfly_loop',
            'delay': 2000
        })
        
        # Group 6: Final Bosses
        groups.append({
            'enemies': [
                {'type': 'boss_galaga', 'row': 0, 'col': 4},
                {'type': 'boss_galaga', 'row': 0, 'col': 5},
                {'type': 'boss_galaga', 'row': 0, 'col': 2},
                {'type': 'boss_galaga', 'row': 0, 'col': 7}
            ],
            'pattern': 'final_bosses',
            'delay': 2500
        })
        
        return groups
    
    @staticmethod
    def get_stage_2_groups():
        """
        Stage 2 entrance groups with unique patterns:
        - Group 1: Bee Squadron (Left) - enters from bottom-left
        - Group 2: Bee Squadron (Right) - enters from bottom-right
        - Group 3: Butterfly Squadron (Left) - enters from top-left
        - Group 4: Butterfly Squadron (Right) - enters from top-right
        - Group 5: The Bosses - enter from top-center in single file
        """
        groups = []
        
        # Group 1: Bee Squadron (Left) - bottom-left entry
        bee_left = []
        for row in range(3, 5):
            for col in range(0, 5):
                bee_left.append({'type': 'zako', 'row': row, 'col': col})
        groups.append({
            'enemies': bee_left[:8],
            'pattern': 'bee_bottom_left',
            'delay': 0
        })
        
        # Group 2: Bee Squadron (Right) - bottom-right entry
        bee_right = []
        for row in range(3, 5):
            for col in range(5, 10):
                bee_right.append({'type': 'zako', 'row': row, 'col': col})
        groups.append({
            'enemies': bee_right[:8],
            'pattern': 'bee_bottom_right',
            'delay': 500
        })
        
        # Group 3: Butterfly Squadron (Left)
        butterfly_left = []
        for row in range(1, 3):
            for col in range(0, 5):
                butterfly_left.append({'type': 'goei', 'row': row, 'col': col})
        groups.append({
            'enemies': butterfly_left[:8],
            'pattern': 'butterfly_top_left',
            'delay': 1000
        })
        
        # Group 4: Butterfly Squadron (Right)
        butterfly_right = []
        for row in range(1, 3):
            for col in range(5, 10):
                butterfly_right.append({'type': 'goei', 'row': row, 'col': col})
        groups.append({
            'enemies': butterfly_right[:8],
            'pattern': 'butterfly_top_right',
            'delay': 1500
        })
        
        # Group 5: The Bosses - single file from top
        groups.append({
            'enemies': [
                {'type': 'boss_galaga', 'row': 0, 'col': 3},
                {'type': 'boss_galaga', 'row': 0, 'col': 4},
                {'type': 'boss_galaga', 'row': 0, 'col': 5},
                {'type': 'boss_galaga', 'row': 0, 'col': 6}
            ],
            'pattern': 'bosses_single_file',
            'delay': 2000
        })
        
        return groups
    
    @staticmethod
    def create_entrance_path(pattern_name, enemy_index, formation_pos):
        """Create specific entrance paths based on pattern name"""
        if pattern_name == 'boss_escort_left':
            return StagePatterns._boss_escort_left_path(enemy_index, formation_pos)
        elif pattern_name == 'boss_escort_right':
            return StagePatterns._boss_escort_right_path(enemy_index, formation_pos)
        elif pattern_name == 'bee_squadron_left':
            return StagePatterns._bee_squadron_left_path(enemy_index, formation_pos)
        elif pattern_name == 'bee_squadron_right':
            return StagePatterns._bee_squadron_right_path(enemy_index, formation_pos)
        elif pattern_name == 'butterfly_loop':
            return StagePatterns._butterfly_loop_path(enemy_index, formation_pos)
        elif pattern_name == 'final_bosses':
            return StagePatterns._final_bosses_path(enemy_index, formation_pos)
        elif pattern_name == 'bee_bottom_left':
            return StagePatterns._bee_bottom_left_path(enemy_index, formation_pos)
        elif pattern_name == 'bee_bottom_right':
            return StagePatterns._bee_bottom_right_path(enemy_index, formation_pos)
        elif pattern_name == 'butterfly_top_left':
            return StagePatterns._butterfly_top_left_path(enemy_index, formation_pos)
        elif pattern_name == 'butterfly_top_right':
            return StagePatterns._butterfly_top_right_path(enemy_index, formation_pos)
        elif pattern_name == 'bosses_single_file':
            return StagePatterns._bosses_single_file_path(enemy_index, formation_pos)
        else:
            # Default path
            return StagePatterns._default_path(formation_pos)
    
    @staticmethod
    def _boss_escort_left_path(index, formation_pos):
        """Wide clockwise loop from top-left"""
        path = []
        steps = 90
        
        # Start from top-left
        start_x = -30
        start_y = 30
        
        for i in range(steps):
            t = i / (steps - 1)
            
            # Clockwise arc
            angle = -math.pi/2 + t * math.pi * 1.5
            radius = 80
            center_x = c.GAME_SIZE.width * 0.7
            center_y = 100
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _boss_escort_right_path(index, formation_pos):
        """Wide counter-clockwise loop from top-right"""
        path = []
        steps = 90
        
        # Start from top-right
        start_x = c.GAME_SIZE.width + 30
        start_y = 30
        
        for i in range(steps):
            t = i / (steps - 1)
            
            # Counter-clockwise arc
            angle = -math.pi/2 - t * math.pi * 1.5
            radius = 80
            center_x = c.GAME_SIZE.width * 0.3
            center_y = 100
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _bee_squadron_left_path(index, formation_pos):
        """Enter from top-left, fly down and bank right"""
        path = []
        steps = 80
        
        # Stagger start positions
        start_x = -20 - (index % 4) * 10
        start_y = -20 - (index // 4) * 15
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.6:
                # Fly down and toward center
                move_t = t / 0.6
                x = start_x + move_t * (c.GAME_SIZE.width * 0.4 - start_x)
                y = start_y + move_t * (c.GAME_SIZE.height * 0.6 - start_y)
            else:
                # Bank right to formation
                bank_t = (t - 0.6) / 0.4
                x = c.GAME_SIZE.width * 0.4 + bank_t * (c.GAME_SIZE.width * 0.8 - c.GAME_SIZE.width * 0.4)
                y = c.GAME_SIZE.height * 0.6 + bank_t * (c.GAME_SIZE.height * 0.2)
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _bee_squadron_right_path(index, formation_pos):
        """Mirror of left path - enter from top-right"""
        path = []
        steps = 80
        
        # Stagger start positions
        start_x = c.GAME_SIZE.width + 20 + (index % 4) * 10
        start_y = -20 - (index // 4) * 15
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.6:
                # Fly down and toward center
                move_t = t / 0.6
                x = start_x + move_t * (c.GAME_SIZE.width * 0.6 - start_x)
                y = start_y + move_t * (c.GAME_SIZE.height * 0.6 - start_y)
            else:
                # Bank left to formation
                bank_t = (t - 0.6) / 0.4
                x = c.GAME_SIZE.width * 0.6 - bank_t * (c.GAME_SIZE.width * 0.6 - c.GAME_SIZE.width * 0.2)
                y = c.GAME_SIZE.height * 0.6 + bank_t * (c.GAME_SIZE.height * 0.2)
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _butterfly_loop_path(index, formation_pos):
        """Single file line from left, loop up and right"""
        path = []
        steps = 100
        
        # Start below player position on left
        start_x = c.GAME_SIZE.width * 0.2
        start_y = c.GAME_SIZE.height - 50 - index * 20
        
        for i in range(steps):
            t = i / (steps - 1)
            
            # Create looping path
            if t < 0.3:
                # Fly up
                up_t = t / 0.3
                x = start_x
                y = start_y - up_t * (start_y - c.GAME_SIZE.height * 0.3)
            elif t < 0.7:
                # Loop right
                loop_t = (t - 0.3) / 0.4
                angle = -math.pi/2 + loop_t * math.pi
                radius = 60
                x = start_x + radius - math.cos(angle) * radius
                y = c.GAME_SIZE.height * 0.3 + math.sin(angle) * radius
            else:
                # Move to formation
                final_t = (t - 0.7) / 0.3
                x = start_x + radius * 2 - final_t * radius
                y = c.GAME_SIZE.height * 0.3 - final_t * 50
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _final_bosses_path(index, formation_pos):
        """Enter from top in pairs, fly straight down"""
        path = []
        steps = 60
        
        # Two pairs entering
        pair = index // 2
        offset = (index % 2) * 30 - 15
        
        start_x = c.GAME_SIZE.width // 2 + pair * 60 - 30 + offset
        start_y = -30
        
        for i in range(steps):
            t = i / (steps - 1)
            
            # Simple downward path
            x = start_x
            y = start_y + t * (c.GAME_SIZE.height * 0.4 - start_y)
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _bee_bottom_left_path(index, formation_pos):
        """Stage 2: Enter from bottom-left, fly up left edge"""
        path = []
        steps = 90
        
        # Start from bottom-left
        start_x = -20 - (index % 4) * 15
        start_y = c.GAME_SIZE.height + 20 + (index // 4) * 15
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.5:
                # Fly up left edge
                up_t = t / 0.5
                x = start_x + up_t * 30
                y = start_y - up_t * (start_y - 40)
            else:
                # Tight clockwise turn at top
                turn_t = (t - 0.5) / 0.5
                angle = math.pi + turn_t * math.pi
                radius = 40
                x = 30 + math.cos(angle) * radius
                y = 40 + math.sin(angle) * radius
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _bee_bottom_right_path(index, formation_pos):
        """Stage 2: Mirror - enter from bottom-right"""
        path = []
        steps = 90
        
        # Start from bottom-right
        start_x = c.GAME_SIZE.width + 20 + (index % 4) * 15
        start_y = c.GAME_SIZE.height + 20 + (index // 4) * 15
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.5:
                # Fly up right edge
                up_t = t / 0.5
                x = start_x - up_t * 30
                y = start_y - up_t * (start_y - 40)
            else:
                # Tight counter-clockwise turn at top
                turn_t = (t - 0.5) / 0.5
                angle = -turn_t * math.pi
                radius = 40
                x = c.GAME_SIZE.width - 30 + math.cos(angle) * radius
                y = 40 + math.sin(angle) * radius
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _butterfly_top_left_path(index, formation_pos):
        """Stage 2: Enter from top-left with sharp counter-clockwise loop"""
        path = []
        steps = 80
        
        start_x = -20 - (index % 4) * 10
        start_y = -20 - (index // 4) * 10
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.4:
                # Fly down toward center
                down_t = t / 0.4
                x = start_x + down_t * (c.GAME_SIZE.width * 0.5 - start_x)
                y = start_y + down_t * (c.GAME_SIZE.height * 0.5 - start_y)
            else:
                # Sharp counter-clockwise loop
                loop_t = (t - 0.4) / 0.6
                angle = loop_t * math.pi * 1.5
                radius = 50
                x = c.GAME_SIZE.width * 0.5 - math.cos(angle) * radius
                y = c.GAME_SIZE.height * 0.5 - math.sin(angle) * radius
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _butterfly_top_right_path(index, formation_pos):
        """Stage 2: Mirror - sharp clockwise loop"""
        path = []
        steps = 80
        
        start_x = c.GAME_SIZE.width + 20 + (index % 4) * 10
        start_y = -20 - (index // 4) * 10
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.4:
                # Fly down toward center
                down_t = t / 0.4
                x = start_x + down_t * (c.GAME_SIZE.width * 0.5 - start_x)
                y = start_y + down_t * (c.GAME_SIZE.height * 0.5 - start_y)
            else:
                # Sharp clockwise loop
                loop_t = (t - 0.4) / 0.6
                angle = -loop_t * math.pi * 1.5
                radius = 50
                x = c.GAME_SIZE.width * 0.5 + math.cos(angle) * radius
                y = c.GAME_SIZE.height * 0.5 - math.sin(angle) * radius
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _bosses_single_file_path(index, formation_pos):
        """Stage 2: Single file from top, split into pairs"""
        path = []
        steps = 90
        
        # All start from top center
        start_x = c.GAME_SIZE.width // 2
        start_y = -30 - index * 20
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.4:
                # Fly down together
                down_t = t / 0.4
                x = start_x
                y = start_y + down_t * (c.GAME_SIZE.height * 0.5 - start_y)
            else:
                # Split into pairs
                split_t = (t - 0.4) / 0.6
                pair = index // 2
                if pair == 0:  # Left pair
                    x = start_x - split_t * 60
                else:  # Right pair
                    x = start_x + split_t * 60
                y = c.GAME_SIZE.height * 0.5 - split_t * 80
                
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _default_path(formation_pos):
        """Default simple path for fallback"""
        path = []
        row, col = formation_pos
        
        # Simple entrance from top
        start_x = c.GAME_SIZE.width // 2 + (col - 5) * 20
        start_y = -30
        
        target_x = c.GAME_SIZE.width // 2 + (col - 5) * 18
        target_y = 60 + row * 20
        
        steps = 60
        for i in range(steps):
            t = i / (steps - 1)
            x = start_x + t * (target_x - start_x)
            y = start_y + t * (target_y - start_y)
            path.append((int(x), int(y)))
        
        return path