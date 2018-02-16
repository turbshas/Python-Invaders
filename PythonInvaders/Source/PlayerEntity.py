import os
import pygame
from Source import Entity

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 28
PLAYER_SPRITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'core_cannon.png')

class PlayerSprite(Entity.Entity):
    # Function to set the x,y, and sprite attributes more easily
    def __init__(self, x, y):
        bitmap = pygame.image.load(PLAYER_SPRITE).convert()
        super(PlayerSprite,self).__init__(x, y, bitmap)
        self.speed = 0
        
    def Move(self):
        self.new_rect = self.rect.move(self.speed, 0)
        
    def AtLeftBound(self, screen) -> bool:
        return screen.get_rect().left <= self.rect.left <= 5
        
    def AtRightBound(self, screen) -> bool:
        return screen.get_rect().right - 5 <= self.rect.right <= screen.get_rect().right