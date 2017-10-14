import Alien
import Entity
import enum
import random
import pygame

class SpawnSide(enum.Enum):
	LEFT = 0
	RIGHT = 1

class UFO(Entity.Entity):
    UFO_POINTS = [50,100,150,200,250,300]
	UFO_SPRITE = os.path.join('python invaders images','ufo.png')
	UFO_WIDTH = 48
	UFO_HEIGHT = 21
	UFO_SPEED = 1
	
    def __init__(self,x,y):
        super(UFO,self).__init__(x, y)
		
        self.bitmap = pygame.image.load(UFO_SPRITE).convert()
        self.surface = pygame.Surface([UFO_WIDTH,UFO_HEIGHT])
        self.rect = self.surface.get_rect()
        
        self.score = UFO_POINTS[random.randrange(0,5)]
		self.spawned = False
		self.spawnSide = SpawnSide.LEFT
		
	def MoveForward(self, screen):
		self.rect.x += self.spawnSide.value * (-1) * UFO_SPEED
		if not (-UFO_WIDTH < self.rect.x and <= screen.get_surface().get_rect().width):
			self.spawned = False
			self.spawnSide = not self.spawnSide
		
	def IsSpawned(self):
		return self.spawned
		
	def TrySpawn(self):
		if random.randint(1,180) == 180:
			self.spawned = True
			return True
		return False
		
	def Destroy(self, screen):
		self.spawned = False
		if self.spawnSide == SpawnSide.LEFT:
			self.rect.x = 0 - UFO_WIDTH
		else:
			selft.rect.x = screen.get_surface().get_rect().width
			