import abc
import Colours
import pygame

class Entity(abc.ABC, pygame.sprite.Sprite):
	def __init__(self, x, y, bitmap, surface):
		super(Entity,self).__init__()
		
		self._bitmap = bitmap
		self._surface = surface
		self.rect = self._surface.get_rect()
		
		# Coords on screen
		self.rect.x = x
		self.rect.y = y
	
	@abc.abstractmethod
	def Move(self):
		pass
		
	def GetRect(self):
		return self.rect

	def Render(self, screen):
		# Make the background of the sprite image file transparent
		self._bitmap.set_colorkey(Colours.BLACK)
		screen.blit(self._bitmap, self.rect)
		
	def IsOffScreen(self, screen):
		return self.rect.right <= 0 \
				or self.rect.bottom <= 0 \
				or self.rect.left >= screen.get_rect().width \
				or self.rect.top >= screen.get_rect().height