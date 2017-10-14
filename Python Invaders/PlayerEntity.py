import Entity
import pygame

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 28
PLAYER_SPRITE = os.path.join('python invaders images','core_cannon.png')

class PlayerSprite(Entity.Entity):
    # Function to set the x,y, and sprite attributes more easily
    def __init__(self,x,y): 
        super(PlayerSprite,self).__init__(x, y)
		
        self.bitmap = pygame.image.load(PLAYER_SPRITE).convert()
        self.surface = pygame.Surface([PLAYER_WIDTH,PLAYER_HEIGHT])
        self.rect = self.surface.get_rect()