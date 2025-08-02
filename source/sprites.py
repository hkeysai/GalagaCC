from .tools import time_millis
import pygame
from . import constants as c, tools
from .constants import Rectangle
from .tools import grab_sheet


class GalagaSprite(pygame.sprite.Sprite):
    """
    Base class for a general sprite in Galaga.
    Useful for sprites that can flip their images, show/hide, and have their images offset from
    their centers, as well as having centered sprites.
    """

    def __init__(self, x, y, width, height, *groups: pygame.sprite.Group):
        super(GalagaSprite, self).__init__(groups)

        # Rectangle and position
        self.rect = pygame.Rect(0, 0, width, height)
        self.x = x
        self.y = y

        # Display and image variables
        self.image = None
        self.image_offset_x: int = 0
        self.image_offset_y: int = 0
        self.is_visible: bool = True
        self.flip_horizontal: bool = False
        self.flip_vertical: bool = False

    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value: int):
        self.rect.centerx = value

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value: int):
        self.rect.centery = value

    def update(self, delta_time: int, flash_flag: bool):
        pass

    def display(self, surface: pygame.Surface):
        if self.image is not None and self.is_visible:
            image = pygame.transform.flip(self.image, self.flip_horizontal, self.flip_vertical)
            img_width, img_height = image.get_size()
            # Center the image
            x = self.x - img_width // 2 + self.image_offset_x
            y = self.y - img_height // 2 + self.image_offset_y
            surface.blit(image, (x, y))


class Player(GalagaSprite):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, 14, 12)
        self.image = grab_sheet(6 * 16, 0 * 16, 16, 16)
        self.image_offset_x = 1

    def update(self, delta_time, keys):
        s = round(c.PLAYER_SPEED * delta_time)
        if keys[pygame.K_RIGHT]:
            self.x += s
        elif keys[pygame.K_LEFT]:
            self.x -= s


class Enemy(GalagaSprite):
    """Base class for all enemy types in Galaga"""
    
    def __init__(self, x, y, width, height):
        super(Enemy, self).__init__(x, y, width, height)
        self.enemy_type = "base"
        self.points_in_formation = 0
        self.points_while_attacking = 0
        self.is_attacking = False
        self.formation_pos = None  # (row, col) in formation
        self.current_frame = 0
        self.animation_timer = 0
        
        # Pattern following
        self.is_entering = False
        self.entrance_path = []
        self.path_index = 0
        self.attack_path = []
        self.path_speed = 2.0  # Pixels per frame
        
        # Firing mechanics
        self.can_fire = True
        self.last_fire_time = 0
        self.fire_cooldown = 1500  # Milliseconds between shots
        
    def get_points(self):
        """Return points based on current state"""
        return self.points_while_attacking if self.is_attacking else self.points_in_formation
        
    def update(self, delta_time: int, animation_flag: bool):
        """Update enemy state and animation"""
        # Handle pattern following
        if self.is_entering and self.entrance_path:
            self._follow_entrance_path()
        elif self.is_attacking and self.attack_path:
            self._follow_attack_path()
            
        # Update animation
        if animation_flag:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self._update_image()
    
    def _follow_entrance_path(self):
        """Follow the entrance path"""
        if self.path_index < len(self.entrance_path):
            target_x, target_y = self.entrance_path[self.path_index]
            
            # Move toward target position
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.path_speed:
                # Reached this point, move to next
                self.x = target_x
                self.y = target_y
                self.path_index += 1
            else:
                # Move toward target
                self.x += int(dx / distance * self.path_speed)
                self.y += int(dy / distance * self.path_speed)
        else:
            # Finished entrance, join formation
            self.is_entering = False
            self.path_index = 0
    
    def _follow_attack_path(self):
        """Follow the attack path"""
        if self.path_index < len(self.attack_path):
            target_x, target_y = self.attack_path[self.path_index]
            
            # Move toward target position
            dx = target_x - self.x
            dy = target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.path_speed:
                # Reached this point, move to next
                self.x = target_x
                self.y = target_y
                self.path_index += 1
            else:
                # Move toward target
                self.x += int(dx / distance * self.path_speed)
                self.y += int(dy / distance * self.path_speed)
        else:
            # Finished attack, return to formation
            self.is_attacking = False
            self.path_index = 0
    
    def set_entrance_path(self, path):
        """Set the entrance path for this enemy"""
        self.entrance_path = path
        self.is_entering = True
        self.path_index = 0
        if path:
            # Start at first position
            self.x, self.y = path[0]
    
    def start_attack(self, path):
        """Start an attack with the given path"""
        self.attack_path = path
        self.is_attacking = True
        self.path_index = 0
    
    def should_fire(self, current_time, player_pos):
        """Check if enemy should fire at player"""
        if not self.can_fire or not self.is_attacking:
            return False
            
        # Check cooldown
        if current_time - self.last_fire_time < self.fire_cooldown:
            return False
            
        # Only fire when diving toward player
        if self.y < player_pos[1] - 50:  # Enemy is above player
            return True
            
        return False
    
    def fire(self, current_time):
        """Fire a missile (to be implemented by Play state)"""
        self.last_fire_time = current_time
    
    def _update_image(self):
        """Update the sprite image based on current frame"""
        if hasattr(self, 'frames') and self.frames:
            x, y, w, h = self.frames[self.current_frame]
            self.image = grab_sheet(x, y, w, h)


class Zako(Enemy):
    """Bee-like enemy - most common type"""
    
    # Sprite sheet coordinates for Zako frames
    BLUE_FRAMES = [
        (80, 80, 16, 16),   # Frame 1
        (96, 80, 16, 16)    # Frame 2
    ]
    
    YELLOW_FRAMES = [
        (112, 80, 16, 16),  # Frame 1
        (128, 80, 16, 16)   # Frame 2
    ]
    
    def __init__(self, x, y, variant='blue'):
        super(Zako, self).__init__(x, y, 16, 16)
        self.enemy_type = "zako"
        self.variant = variant
        self.points_in_formation = 50
        self.points_while_attacking = 100
        self.fire_cooldown = 2000  # Zakos fire less frequently
        
        # Set frames based on variant
        self.frames = self.BLUE_FRAMES if variant == 'blue' else self.YELLOW_FRAMES
        self._update_image()


class Goei(Enemy):
    """Butterfly-like enemy - escorts for Boss Galaga"""
    
    # Sprite sheet coordinates for Goei frames
    RED_FRAMES = [
        (80, 96, 16, 16),   # Frame 1
        (96, 96, 16, 16)    # Frame 2
    ]
    
    WHITE_FRAMES = [
        (144, 80, 16, 16),  # Frame 1
        (160, 80, 16, 16)   # Frame 2
    ]
    
    def __init__(self, x, y, variant='red'):
        super(Goei, self).__init__(x, y, 16, 16)
        self.enemy_type = "goei"
        self.variant = variant
        self.points_in_formation = 80
        self.points_while_attacking = 160
        self.is_escort = False  # True when escorting Boss Galaga
        self.fire_cooldown = 1500  # Goei fire more frequently than Zako
        
        # Set frames based on variant
        self.frames = self.RED_FRAMES if variant == 'red' else self.WHITE_FRAMES
        self._update_image()


class BossGalaga(Enemy):
    """Large enemy that can capture player's ship"""
    
    # Sprite sheet coordinates for Boss Galaga frames
    GREEN_FRAMES = [
        (112, 96, 16, 16),  # Frame 1
        (128, 96, 16, 16)   # Frame 2
    ]
    
    PURPLE_FRAMES = [
        (144, 96, 16, 16),  # Frame 1 (after being hit once)
        (160, 96, 16, 16)   # Frame 2
    ]
    
    def __init__(self, x, y):
        super(BossGalaga, self).__init__(x, y, 16, 16)
        self.enemy_type = "boss_galaga"
        self.points_in_formation = 150
        self.points_while_attacking = 400  # Base points, modified by escorts
        self.hits_remaining = 2
        self.has_captured_fighter = False
        self.captured_fighter = None
        self.escort_count = 0
        self.can_fire = False  # Boss Galagas don't fire missiles, they use tractor beam
        
        # Start with green frames
        self.frames = self.GREEN_FRAMES
        self._update_image()
    
    def hit(self):
        """Handle being hit by player missile"""
        self.hits_remaining -= 1
        if self.hits_remaining == 1:
            # Change to purple after first hit
            self.frames = self.PURPLE_FRAMES
            self._update_image()
        return self.hits_remaining <= 0
    
    def get_points(self):
        """Calculate points based on escort count"""
        if not self.is_attacking:
            return self.points_in_formation
        
        # Points increase with escort count
        base_points = 400
        if self.escort_count == 1:
            return 800
        elif self.escort_count == 2:
            return 1600
        return base_points


class Missile(GalagaSprite):
    ENEMY_MISSILE = 246, 51, 3, 8
    PLAYER_MISSILE = 246, 67, 3, 8

    def __init__(self, x, y, vel, is_enemy):
        super(Missile, self).__init__(x, y, 2, 10)
        self.vel = vel
        self.is_enemy = is_enemy

        if self.is_enemy:
            img_slice = self.ENEMY_MISSILE
        else:
            img_slice = self.PLAYER_MISSILE
        ix, iy, w, h = img_slice
        self.image = grab_sheet(ix, iy, w, h)

    def update(self, delta_time: int, flash_flag: bool):
        vel = self.vel * delta_time
        self.x += round(vel.x)
        self.y += round(vel.y)


class Explosion(GalagaSprite):
    PLAYER_FRAME_DURATION = 140
    OTHER_FRAME_DURATION = 120

    PLAYER_FRAMES = [Rectangle(64, 112, 32, 32), Rectangle(96, 112, 32, 32), Rectangle(128, 112, 32, 32),
                     Rectangle(160, 112, 32, 32)]

    OTHER_FRAMES = [Rectangle(224, 80, 16, 16), Rectangle(240, 80, 16, 16), Rectangle(224, 96, 16, 16),
                    Rectangle(0, 112, 32, 32), Rectangle(32, 112, 32, 32)]

    def __init__(self, x: int, y: int, is_player_type=False):
        super(Explosion, self).__init__(x, y, 16, 16)
        self.is_player_type = is_player_type

        self.frame_timer = 0

        if self.is_player_type:
            self.image = grab_sheet(64, 112, 32, 32)
            self.frames = iter(self.PLAYER_FRAMES)
            self.frame_duration = self.PLAYER_FRAME_DURATION
        else:
            self.image = grab_sheet
            self.frames = iter(self.OTHER_FRAMES)
            self.frame_duration = self.OTHER_FRAME_DURATION

        self.frame = None
        self.next_frame()

    def next_frame(self):
        self.frame = next(self.frames)
        x, y, w, h = self.frame
        self.image = grab_sheet(x, y, w, h)
        self.frame_timer = 0

    def update(self, delta_time: int, flash_flag: bool):
        self.frame_timer += delta_time
        if self.frame_timer >= self.frame_duration:
            try:
                self.next_frame()
            except StopIteration:
                self.kill()
                return

    def display(self, surface: pygame.Surface):
        super(Explosion, self).display(surface)


def create_score_surface(number):
    sheet_y = 240
    char_width = 5
    char_height = 8
    sheet_char_width = 4

    number = int(number)
    str_num = str(number)
    length = len(str_num)

    # Create the surface to add to
    # noinspection PyArgumentList
    surface = pygame.Surface((char_width * length, char_height)).convert_alpha()

    # choose color based on the number
    color = None
    if number in (800, 1000):
        color = c.BLUE
    else:
        color = c.YELLOW

    # blit each individual char
    for i, character in enumerate(str_num):
        value = int(character)
        sheet_x = value * sheet_char_width
        number_sprite = grab_sheet(sheet_x, sheet_y, 4, 8)
        surface.blit(number_sprite, (i * char_width, 0))

    # replace white with color
    pixels = pygame.PixelArray(surface)
    pixels.replace((255, 255, 255), color)
    pixels.close()

    return surface


class ScoreText(GalagaSprite):
    # The class keeps track of the text sprites
    text_sprites = pygame.sprite.Group()

    def __init__(self, x, y, number, lifetime=950):
        super(ScoreText, self).__init__(x, y, 1, 1, self.text_sprites)  # BB size doesn't matter here
        self.number = number
        self.image = create_score_surface(self.number)
        self.lifetime = lifetime

    def update(self, delta_time: int, flash_flag: bool):
        # Wait to die
        if self.lifetime < 0:
            self.kill()
            return
        self.lifetime -= delta_time
