import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Entity,self).__init__()
		
        self.bitmap
        self.surface
        self.rect = self.surface.get_rect()
		
		# Coords on screen
        self.rect.x = x
        self.rect.y = y

    def render(self, screen):
        # Make the background of the sprite image file transparent
        self.bitmap.set_colorkey(BLACK)
        # Render the entity on the screen
        screen.blit(self.bitmap,self.rect)