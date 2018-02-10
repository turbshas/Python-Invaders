import Entity
import os
import pygame

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 28
PLAYER_SPRITE = os.path.join('python invaders images','core_cannon.png')

class PlayerSprite(Entity.Entity):
	# Function to set the x,y, and sprite attributes more easily
	def __init__(self,x,y):
		bitmap = pygame.image.load(PLAYER_SPRITE).convert()
		surface = pygame.Surface([PLAYER_WIDTH,PLAYER_HEIGHT])
		super(PlayerSprite,self).__init__(x, y, bitmap, surface)
		self.speed = 0
		
	def Move(self):
		self.rect.x += self.speed
		
	def AtLeftBound(self, screen):
		return screen.get_rect().left <= self.rect.left <= 5
		
	def AtRightBound(self, screen):
		return screen.get_rect().right - 5 <= self.rect.right <= screen.get_rect().right