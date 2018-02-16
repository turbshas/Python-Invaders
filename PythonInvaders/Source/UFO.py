import enum
import os
import pygame
import random
from Source import Alien
from Source import Entity

UFO_POINTS = [50,100,150,200,250,300]
UFO_SPRITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'ufo.png')
UFO_WIDTH = 48
UFO_HEIGHT = 21
UFO_SPEED = 1

class SpawnSide(enum.Enum):
    LEFT = 0
    RIGHT = 1

class UFO(Entity.Entity):    
    def __init__(self, x, y):
        bitmap = pygame.image.load(UFO_SPRITE).convert()
        super(UFO,self).__init__(x, y, bitmap)
        
        self._spawned = False
        self._spawnSide = SpawnSide.LEFT
        
    def Move(self):
        self.new_rect = self.rect.move(UFO_SPEED if self._spawnSide == SpawnSide.LEFT else -UFO_SPEED, 0)
        
    def IsSpawned(self) -> bool:
        return self._spawned
        
    def TrySpawn(self) -> bool:
        if random.randint(1, 600) == 600:
            self._spawned = True
            self.score = UFO_POINTS[random.randrange(0,5)]
            return True
        return False
        
    def Hide(self):
        self._spawned = False
        self._spawnSide = not self._spawnSide
        
    def Destroy(self, screen):
        self._spawned = False
        if self._spawnSide == SpawnSide.LEFT:
            self.new_rect.x = screen.get_rect().left - UFO_WIDTH
        else:
            self.new_rect.x = screen.get_rect().right
            