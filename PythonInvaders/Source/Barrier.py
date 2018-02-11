import os
from Source import Entity

BARRIER_SPRITES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage0.png'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage1.png'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage2.png'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage3.png')
]

BARRIER_WIDTH = 12
BARRIER_HEIGHT = 12
# Place of the groups of barriers
BARRIER_GROUP_X = [width/8 - ((BARRIER_WIDTH * 4)/2),width/2 - ((BARRIER_WIDTH * 4) + 50),width/2 + 50,width * (7/8) - ((BARRIER_WIDTH * 4)/2)]
# Variables determing how many barriers to place
NUM_ROWS_BARRIERS = 3
NUM_COLUMNS_BARRIERS = 4 # A space after every 4 barriers

class Barrier(Entity.Entity):
    # Class for the barrier
    def __init__(self,x,y):
        super(Barrier,self).__init__(x, y)
        
        self.surface = pygame.Surface([BARRIER_WIDTH,BARRIER_HEIGHT])
        self.rect = self.surface.get_rect()
        
        # Stage of damager barrier is in (default is 0)
        self.stage = 0

    def render(self, screen):
        # Reset the bitmap image, if the barrier's stage has changed
        self.bitmap = pygame.image.load(BARRIER_SPRITES[self.stage]).convert()
        self.bitmap.set_colorkey(BLACK)
        # Draw the barrier
        screen.blit(self.bitmap,self.rect)