import Alien
import Entity
import enum
import os
import pygame
import random

UFO_POINTS = [50,100,150,200,250,300]
UFO_SPRITE = os.path.join('python invaders images','ufo.png')
UFO_WIDTH = 48
UFO_HEIGHT = 21
UFO_SPEED = 1

class SpawnSide(enum.Enum):
	LEFT = 0
	RIGHT = 1

class UFO(Entity.Entity):	
	def __init__(self,x,y):
		bitmap = pygame.image.load(UFO_SPRITE).convert()
		surface = pygame.Surface([UFO_WIDTH,UFO_HEIGHT])
		super(UFO,self).__init__(x, y, bitmap, surface)
		
		self._score = UFO_POINTS[random.randrange(0,5)]
		self._spawned = False
		self._spawnSide = SpawnSide.LEFT
		
	def Move(self):
		self.rect.x += self._spawnSide.value * (-1) * UFO_SPEED
		
	def IsSpawned(self):
		return self._spawned
		
	def TrySpawn(self):
		if random.randint(1,180) == 180:
			self._spawned = True
			return True
		return False
		
	def Hide(self):
		self._spawned = False
		self._spawnSide = not self._spawnSide
		
	def Destroy(self, screen):
		self._spawned = False
		if self._spawnSide == SpawnSide.LEFT:
			self.rect.x = screen.get_rect().right - UFO_WIDTH
		else:
			self.rect.x = screen.get_rect().right
			