import pygame
import math
from . import constants as c
from .sprites import Zako, Goei, BossGalaga
from .patterns import PatternEngine


class Formation:
    """Manages the enemy formation grid in Galaga"""
    
    # Formation layout: 10 columns x 5 rows
    COLS = 10
    ROWS = 5
    
    # Spacing between enemies in formation
    COL_SPACING = 18
    ROW_SPACING = 20
    
    # Formation position offsets
    BASE_X = c.GAME_SIZE.width // 2
    BASE_Y = 60
    
    def __init__(self):
        # 2D grid to track enemy positions [row][col]
        self.grid = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        
        # Formation movement parameters
        self.x_offset = 0
        self.y_offset = 0
        self.spread = c.FORMATION_MIN_SPREAD
        self.cycle_time = 0
        
        # Group to hold all enemies
        self.enemies = pygame.sprite.Group()
        
        # Pattern engine for entrance/attack patterns
        self.pattern_engine = PatternEngine()
        
        # Track entrance progress
        self.entrance_delay_timer = 0
        self.enemies_to_spawn = []
        
        # Attack timing
        self.attack_timer = 0
        self.attack_frequency = 3000  # Milliseconds between attack waves
        self.min_attack_frequency = 1000  # Minimum frequency at higher levels
        
    def create_stage_formation(self, stage_num):
        """Create enemy formation for a given stage with entrance patterns"""
        # Clear existing formation
        self.clear()
        
        # Determine entrance pattern for this stage
        pattern_type = self.pattern_engine.get_entrance_pattern(stage_num)
        
        # Create spawn list with delays
        spawn_list = []
        enemy_index = 0
        
        # Row 0 (top): Boss Galagas in center positions
        boss_positions = [3, 4, 5, 6]  # Center 4 columns
        for col in boss_positions:
            boss = BossGalaga(0, 0)  # Start off-screen
            boss.formation_pos = (0, col)
            
            # Create entrance path
            path = self.pattern_engine.create_entrance_path(pattern_type, enemy_index, (0, col))
            
            spawn_list.append({
                'enemy': boss,
                'path': path,
                'delay': enemy_index * 100,  # Stagger spawns
                'row': 0,
                'col': col
            })
            enemy_index += 1
        
        # Rows 1-2: Goei (butterflies)
        for row in range(1, 3):
            for col in range(self.COLS):
                # Alternate between red and white variants
                variant = 'red' if (row + col) % 2 == 0 else 'white'
                goei = Goei(0, 0, variant)
                goei.formation_pos = (row, col)
                
                # Create entrance path
                path = self.pattern_engine.create_entrance_path(pattern_type, enemy_index, (row, col))
                
                spawn_list.append({
                    'enemy': goei,
                    'path': path,
                    'delay': enemy_index * 50,  # Faster spawn for regular enemies
                    'row': row,
                    'col': col
                })
                enemy_index += 1
        
        # Rows 3-4: Zako (bees)
        for row in range(3, 5):
            for col in range(self.COLS):
                # Use yellow variant for higher stages
                variant = 'yellow' if stage_num > 5 else 'blue'
                zako = Zako(0, 0, variant)
                zako.formation_pos = (row, col)
                
                # Create entrance path
                path = self.pattern_engine.create_entrance_path(pattern_type, enemy_index, (row, col))
                
                spawn_list.append({
                    'enemy': zako,
                    'path': path,
                    'delay': enemy_index * 50,
                    'row': row,
                    'col': col
                })
                enemy_index += 1
        
        # Set up spawning
        self.enemies_to_spawn = spawn_list
        self.entrance_delay_timer = 0
    
    def get_position(self, row, col):
        """Get the screen position for a formation grid position"""
        # Calculate base position
        x = self.BASE_X + (col - self.COLS // 2) * self.COL_SPACING
        y = self.BASE_Y + row * self.ROW_SPACING
        
        # Apply formation movement offsets
        x += self.x_offset
        y += self.y_offset
        
        # Apply spread effect (breathing animation)
        center_col = self.COLS / 2.0
        spread_factor = abs(col - center_col) / center_col
        x += self.spread * spread_factor * (1 if col >= center_col else -1)
        
        return int(x), int(y)
    
    def update(self, delta_time, player_pos=None):
        """Update formation movement and enemy positions"""
        # Handle enemy spawning with delays
        if self.enemies_to_spawn:
            self.entrance_delay_timer += delta_time
            
            # Check if it's time to spawn the next enemy
            while self.enemies_to_spawn and self.entrance_delay_timer >= self.enemies_to_spawn[0]['delay']:
                spawn_data = self.enemies_to_spawn.pop(0)
                enemy = spawn_data['enemy']
                
                # Set entrance path and add to formation
                enemy.set_entrance_path(spawn_data['path'])
                self.grid[spawn_data['row']][spawn_data['col']] = enemy
                self.enemies.add(enemy)
        
        # Update attack timer and trigger attacks
        if not self.enemies_to_spawn:  # Only attack after all enemies have spawned
            self.attack_timer += delta_time
            if self.attack_timer >= self.attack_frequency:
                self.trigger_attack_wave(player_pos)
                self.attack_timer = 0
        
        # Update formation cycle for breathing effect
        self.cycle_time += delta_time
        cycle_progress = (self.cycle_time % c.FORMATION_CYCLE_TIME) / c.FORMATION_CYCLE_TIME
        
        # Calculate spread (breathing in and out)
        if cycle_progress < 0.5:
            # Breathing out
            self.spread = c.FORMATION_MIN_SPREAD + (c.FORMATION_MAX_SPREAD - c.FORMATION_MIN_SPREAD) * (cycle_progress * 2)
        else:
            # Breathing in
            self.spread = c.FORMATION_MAX_SPREAD - (c.FORMATION_MAX_SPREAD - c.FORMATION_MIN_SPREAD) * ((cycle_progress - 0.5) * 2)
        
        # Calculate horizontal movement
        self.x_offset = int(c.FORMATION_MAX_X * math.sin(cycle_progress * 2 * 3.14159))
        
        # Update enemy positions based on formation
        for row in range(self.ROWS):
            for col in range(self.COLS):
                enemy = self.grid[row][col]
                if enemy and not enemy.is_attacking and not enemy.is_entering:
                    x, y = self.get_position(row, col)
                    enemy.x = x
                    enemy.y = y
    
    def get_enemy_at(self, row, col):
        """Get enemy at specific grid position"""
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self.grid[row][col]
        return None
    
    def remove_enemy(self, enemy):
        """Remove enemy from formation"""
        if enemy.formation_pos:
            row, col = enemy.formation_pos
            self.grid[row][col] = None
        enemy.kill()
    
    def get_escort_candidates(self, boss_galaga):
        """Get potential Goei escorts for a Boss Galaga"""
        escorts = []
        if boss_galaga.formation_pos:
            boss_row, boss_col = boss_galaga.formation_pos
            
            # Check Goei in rows below the Boss Galaga
            for row in range(1, 3):  # Goei rows
                # Check adjacent columns
                for col_offset in [-1, 0, 1]:
                    col = boss_col + col_offset
                    goei = self.get_enemy_at(row, col)
                    if goei and goei.enemy_type == "goei" and not goei.is_attacking:
                        escorts.append(goei)
        
        return escorts[:2]  # Maximum 2 escorts
    
    def is_empty(self):
        """Check if formation is empty"""
        return len(self.enemies) == 0
    
    def clear(self):
        """Clear the formation"""
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col]:
                    self.grid[row][col].kill()
                    self.grid[row][col] = None
        self.enemies.empty()
    
    def trigger_attack_wave(self, player_pos=None):
        """Trigger a wave of enemy attacks"""
        # Get list of enemies available to attack
        available_enemies = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                enemy = self.grid[row][col]
                if enemy and not enemy.is_attacking and not enemy.is_entering:
                    available_enemies.append(enemy)
        
        if not available_enemies:
            return
        
        # Determine attack type based on enemy composition
        boss_galagas = [e for e in available_enemies if e.enemy_type == "boss_galaga"]
        
        # Sometimes send a Boss Galaga with escorts
        if boss_galagas and pygame.time.get_ticks() % 3 == 0:  # 1 in 3 chance
            boss = boss_galagas[0]
            escorts = self.get_escort_candidates(boss)
            
            # Create attack paths
            if not player_pos:
                player_pos = (c.GAME_SIZE.width // 2, c.STAGE_BOTTOM_Y - 16)  # Default position
            boss_path = self.pattern_engine.create_dive_pattern("boss_galaga", (boss.x, boss.y), player_pos)
            boss.start_attack(boss_path)
            
            # Send escorts with the boss
            boss.escort_count = len(escorts)
            for i, escort in enumerate(escorts):
                escort_path = self.pattern_engine.create_dive_pattern("goei", (escort.x, escort.y), player_pos)
                escort.start_attack(escort_path)
                escort.is_escort = True
        else:
            # Regular attack wave - select 1-3 random enemies
            import random
            num_attackers = min(random.randint(1, 3), len(available_enemies))
            attackers = random.sample(available_enemies, num_attackers)
            
            for enemy in attackers:
                if not player_pos:
                    player_pos = (c.GAME_SIZE.width // 2, c.STAGE_BOTTOM_Y - 16)
                attack_path = self.pattern_engine.create_dive_pattern(
                    enemy.enemy_type, 
                    (enemy.x, enemy.y), 
                    player_pos
                )
                enemy.start_attack(attack_path)
    
    def set_difficulty(self, stage_num):
        """Adjust attack frequency and enemy fire rates based on stage"""
        # Increase attack frequency as stages progress
        base_frequency = 3000
        reduction_per_stage = 100
        self.attack_frequency = max(
            self.min_attack_frequency,
            base_frequency - (stage_num * reduction_per_stage)
        )
        
        # Also adjust enemy fire rates
        fire_rate_reduction = min(50 * stage_num, 500)  # Cap at 500ms reduction
        for enemy in self.enemies:
            if enemy.can_fire:
                base_cooldown = 2000 if enemy.enemy_type == "zako" else 1500
                enemy.fire_cooldown = max(500, base_cooldown - fire_rate_reduction)