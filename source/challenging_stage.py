"""
Challenging Stage implementation based on STAGES.MD
Stage 3, 7, 11, 15, etc. are bonus rounds
"""
import pygame
import math
from . import constants as c
from .sprites import Zako, Goei, BossGalaga


class ChallengingStage:
    """Manages challenging stage patterns where enemies don't shoot"""
    
    @staticmethod
    def is_challenging_stage(stage_num):
        """Check if a stage is a challenging stage"""
        # Stage 3 is first challenging stage, then every 4 stages
        if stage_num == 3:
            return True
        return (stage_num - 3) % 4 == 0 and stage_num > 3
    
    @staticmethod
    def get_challenging_stage_waves(stage_num):
        """Get waves for challenging stage (5 waves of 8 enemies each)"""
        waves = []
        
        # Wave 1: Left-Side Weave (8 enemies)
        wave1 = []
        for i in range(8):
            enemy_type = 'zako' if i < 4 else 'goei'
            wave1.append({
                'type': enemy_type,
                'index': i,
                'pattern': 'left_weave'
            })
        waves.append({
            'enemies': wave1,
            'delay': 0
        })
        
        # Wave 2: Right-Side Weave (8 enemies)
        wave2 = []
        for i in range(8):
            enemy_type = 'goei' if i < 4 else 'zako'
            wave2.append({
                'type': enemy_type,
                'index': i,
                'pattern': 'right_weave'
            })
        waves.append({
            'enemies': wave2,
            'delay': 2000
        })
        
        # Wave 3: Center Loop Left (4 enemies)
        wave3 = []
        for i in range(4):
            wave3.append({
                'type': 'goei',
                'index': i,
                'pattern': 'center_loop_left'
            })
        waves.append({
            'enemies': wave3,
            'delay': 4000
        })
        
        # Wave 4: Center Loop Right (4 enemies)
        wave4 = []
        for i in range(4):
            wave4.append({
                'type': 'goei',
                'index': i,
                'pattern': 'center_loop_right'
            })
        waves.append({
            'enemies': wave4,
            'delay': 4500  # Slight delay after wave 3
        })
        
        # Wave 5: Boss Galaga Escort (8 enemies - 2 bosses, 6 butterflies)
        wave5 = []
        # Left column
        for i in range(4):
            if i < 3:
                wave5.append({
                    'type': 'goei',
                    'index': i,
                    'pattern': 'boss_escort_left',
                    'column': 0
                })
            else:
                wave5.append({
                    'type': 'boss_galaga',
                    'index': i,
                    'pattern': 'boss_escort_left',
                    'column': 0
                })
        # Right column
        for i in range(4):
            if i < 3:
                wave5.append({
                    'type': 'goei',
                    'index': i + 4,
                    'pattern': 'boss_escort_right',
                    'column': 1
                })
            else:
                wave5.append({
                    'type': 'boss_galaga',
                    'index': i + 4,
                    'pattern': 'boss_escort_right',
                    'column': 1
                })
        waves.append({
            'enemies': wave5,
            'delay': 6000
        })
        
        return waves
    
    @staticmethod
    def create_challenging_path(pattern_name, enemy_index):
        """Create path for challenging stage patterns"""
        if pattern_name == 'left_weave':
            return ChallengingStage._left_weave_path(enemy_index)
        elif pattern_name == 'right_weave':
            return ChallengingStage._right_weave_path(enemy_index)
        elif pattern_name == 'center_loop_left':
            return ChallengingStage._center_loop_left_path(enemy_index)
        elif pattern_name == 'center_loop_right':
            return ChallengingStage._center_loop_right_path(enemy_index)
        elif pattern_name == 'boss_escort_left':
            return ChallengingStage._boss_escort_column_path(enemy_index, 0)
        elif pattern_name == 'boss_escort_right':
            return ChallengingStage._boss_escort_column_path(enemy_index, 1)
        else:
            return []
    
    @staticmethod
    def _left_weave_path(index):
        """Enter from top-left, weave down left side, cross to right, exit top-right"""
        path = []
        steps = 180
        
        # Stagger entry
        start_delay = index * 10
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.3:
                # Enter from top-left, fly down left side
                down_t = t / 0.3
                x = -20 + down_t * 40
                y = -20 - start_delay + down_t * (c.GAME_SIZE.height + 40)
            elif t < 0.5:
                # Cross from left to right at bottom
                cross_t = (t - 0.3) / 0.2
                x = 20 + cross_t * (c.GAME_SIZE.width - 40)
                y = c.GAME_SIZE.height - 20
            elif t < 0.8:
                # Fly up right side
                up_t = (t - 0.5) / 0.3
                x = c.GAME_SIZE.width - 20
                y = c.GAME_SIZE.height - 20 - up_t * (c.GAME_SIZE.height + 40)
            else:
                # Exit top-right
                exit_t = (t - 0.8) / 0.2
                x = c.GAME_SIZE.width - 20 + exit_t * 40
                y = -20 - exit_t * 20
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _right_weave_path(index):
        """Mirror of left weave - enter top-right, exit top-left"""
        path = []
        steps = 180
        
        # Stagger entry
        start_delay = index * 10
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.3:
                # Enter from top-right, fly down right side
                down_t = t / 0.3
                x = c.GAME_SIZE.width + 20 - down_t * 40
                y = -20 - start_delay + down_t * (c.GAME_SIZE.height + 40)
            elif t < 0.5:
                # Cross from right to left at bottom
                cross_t = (t - 0.3) / 0.2
                x = c.GAME_SIZE.width - 20 - cross_t * (c.GAME_SIZE.width - 40)
                y = c.GAME_SIZE.height - 20
            elif t < 0.8:
                # Fly up left side
                up_t = (t - 0.5) / 0.3
                x = 20
                y = c.GAME_SIZE.height - 20 - up_t * (c.GAME_SIZE.height + 40)
            else:
                # Exit top-left
                exit_t = (t - 0.8) / 0.2
                x = 20 - exit_t * 40
                y = -20 - exit_t * 20
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _center_loop_left_path(index):
        """Enter from top-center, peel left, large counter-clockwise loop"""
        path = []
        steps = 150
        
        # Stagger within group
        start_offset = index * 15
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.1:
                # Enter from top center
                enter_t = t / 0.1
                x = c.GAME_SIZE.width // 2
                y = -20 - start_offset + enter_t * 40
            elif t < 0.7:
                # Large counter-clockwise loop in upper-left
                loop_t = (t - 0.1) / 0.6
                angle = -math.pi/2 + loop_t * math.pi * 2
                radius = 60
                center_x = c.GAME_SIZE.width * 0.3
                center_y = c.GAME_SIZE.height * 0.3
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
            else:
                # Exit off top
                exit_t = (t - 0.7) / 0.3
                x = c.GAME_SIZE.width * 0.3 + exit_t * 20
                y = c.GAME_SIZE.height * 0.3 - radius - exit_t * 100
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _center_loop_right_path(index):
        """Mirror - clockwise loop in upper-right"""
        path = []
        steps = 150
        
        # Stagger within group
        start_offset = index * 15
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.1:
                # Enter from top center
                enter_t = t / 0.1
                x = c.GAME_SIZE.width // 2
                y = -20 - start_offset + enter_t * 40
            elif t < 0.7:
                # Large clockwise loop in upper-right
                loop_t = (t - 0.1) / 0.6
                angle = -math.pi/2 - loop_t * math.pi * 2
                radius = 60
                center_x = c.GAME_SIZE.width * 0.7
                center_y = c.GAME_SIZE.height * 0.3
                x = center_x + math.cos(angle) * radius
                y = center_y + math.sin(angle) * radius
            else:
                # Exit off top
                exit_t = (t - 0.7) / 0.3
                x = c.GAME_SIZE.width * 0.7 - exit_t * 20
                y = c.GAME_SIZE.height * 0.3 - radius - exit_t * 100
            
            path.append((int(x), int(y)))
        
        return path
    
    @staticmethod
    def _boss_escort_column_path(index, column):
        """Two columns converging from top, bosses are last in each column"""
        path = []
        steps = 120
        
        # Position in column (0-3)
        pos_in_column = index % 4
        
        # Starting position
        if column == 0:  # Left column
            start_x = c.GAME_SIZE.width * 0.3
        else:  # Right column
            start_x = c.GAME_SIZE.width * 0.7
        
        start_y = -30 - pos_in_column * 25
        
        for i in range(steps):
            t = i / (steps - 1)
            
            if t < 0.6:
                # Fly downward, converging slightly
                down_t = t / 0.6
                if column == 0:
                    x = start_x + down_t * (c.GAME_SIZE.width * 0.1)
                else:
                    x = start_x - down_t * (c.GAME_SIZE.width * 0.1)
                y = start_y + down_t * (c.GAME_SIZE.height + 60)
            else:
                # Continue off bottom
                continue_t = (t - 0.6) / 0.4
                if column == 0:
                    x = start_x + c.GAME_SIZE.width * 0.1
                else:
                    x = start_x - c.GAME_SIZE.width * 0.1
                y = c.GAME_SIZE.height + 30 + continue_t * 50
            
            path.append((int(x), int(y)))
        
        return path