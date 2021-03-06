import enum
import os
import pygame
import random
from Source import Entity
from Source import GameState

# List of sprites, in order of row starting from the top
SPRITES = [
    [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'small_invader1.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'medium_invader1.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'medium_invader1.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'large_invader1.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'large_invader1.png')
    ],
    [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'small_invader2.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'medium_invader2.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'medium_invader2.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'large_invader2.png'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'large_invader2.png')
    ]
]

ALIEN_POINTS = [40,20,20,10,10]
ALIEN_WIDTH = [16,22,22,24,24] # This list holds the width of the aliens in each row, e.g. aliens in row 1 are width 16 pixels, aliens in row 2 are 22 pixels etc.
ALIEN_MAX_WIDTH = 24 # This is the width of the largest alien. It is used to make sure all the aliens line up vertically
ALIEN_HEIGHT = 16 # All of the aliens are 16 pixels tall
ALIEN_SPACING = 10
ALIEN_BOUNDS = 20
NUM_ALIENS = 11 # This is number of aliens per row
NUM_ROWS = 5 # The number of rows of aliens
ALIEN_SHOOT_CHANCE = 900 # 1/ALIEN_SHOOT_CHANCE the aliens will shoot at the player

# Offset amount is used so aliens start in the middle of the screen
X_OFFSET = (GameState.WIDTH - ((ALIEN_MAX_WIDTH * NUM_ALIENS) + (ALIEN_SPACING * (NUM_ALIENS - 1)))) / 2
Y_OFFSET = (GameState.HEIGHT - ((ALIEN_HEIGHT * NUM_ROWS) + (ALIEN_SPACING * (NUM_ROWS - 1)))) / 4

class AlienSpriteType(enum.Enum):
    NORMAL = 0
    ALTERNATE = 1

class Alien(Entity.Entity):
    def __init__(self, x, y, row, column):
        bitmap = pygame.image.load(SPRITES[AlienSpriteType.NORMAL.value][row]).convert()
        super(Alien, self).__init__(x, y, bitmap)
        
        self.row = row
        self.column = column

        self._sprite_type = AlienSpriteType.NORMAL
        self._sprite = SPRITES[AlienSpriteType.NORMAL.value][row]
        self._alternate_sprite = SPRITES[AlienSpriteType.ALTERNATE.value][row]
        
        self.score = ALIEN_POINTS[row]
        self.speed_x = 0
        self.speed_y = 0
        
    def Move(self):
        self.new_rect = self.rect.move(self.speed_x, self.speed_y)
    
    def ToggleSprite(self):
        if self._sprite_type == AlienSpriteType.NORMAL:
            self._sprite_type = AlienSpriteType.ALTERNATE
            self._bitmap = pygame.image.load(self._alternate_sprite).convert()
        else:
            self._sprite_type = AlienSpriteType.NORMAL
            self._bitmap = pygame.image.load(self._sprite).convert()

    def TryShoot(self) -> bool:
        return random.randint(1, ALIEN_SHOOT_CHANCE) == ALIEN_SHOOT_CHANCE
        
    def AtBounds(self, screen) -> bool:
        return self.rect.left >= screen.get_rect().right - (ALIEN_MAX_WIDTH + ALIEN_BOUNDS) \
            or self.rect.left <= ALIEN_BOUNDS