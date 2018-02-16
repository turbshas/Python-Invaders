import abc
import pygame
from Source import Colours
from typing import List

class Entity(abc.ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, bitmap_surface):
        super(Entity, self).__init__()
        
        self._bitmap = bitmap_surface
        self.rect = self._bitmap.get_rect()
        
        # Coords on screen
        self.rect.x = x
        self.rect.y = y

        self.new_rect = self.rect
    
    @abc.abstractmethod
    def Move(self):
        pass
        
    def GetRect(self) -> pygame.Rect:
        return self.rect

    def Render(self, screen) -> List[pygame.Rect]:
        rect_list = [self.rect, self.new_rect]
        self.rect = self.new_rect

        # Make the background of the sprite image file transparent
        self._bitmap.set_colorkey(Colours.BLACK)
        screen.blit(self._bitmap, self.rect)

        return rect_list
    
    def Clear(self, screen) -> List[pygame.Rect]:
        self._bitmap.fill(Colours.BLACK)
        screen.blit(self._bitmap, self.rect)
        return [self.rect]
        
    def IsOffScreen(self, screen):
        return self.rect.right <= screen.get_rect().left \
                or self.rect.bottom <= screen.get_rect().top \
                or self.rect.left >= screen.get_rect().right \
                or self.rect.top >= screen.get_rect().bottom