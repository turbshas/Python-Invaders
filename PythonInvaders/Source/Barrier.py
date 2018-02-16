import os
import pygame
from Source import Colours
from Source import Entity

BARRIER_SPRITES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage0.png'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage1.png'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage2.png'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Images', 'barrier_stage3.png')
]

BARRIER_WIDTH = 16
BARRIER_HEIGHT = 16
BARRIER_GAP = 100 # Gap between barrier groups
# Place of the groups of barriers
width = 640
BARRIER_GROUP_X = [width/8 - BARRIER_WIDTH * 2,
                   width/2 - ((BARRIER_WIDTH * 4) + BARRIER_GAP / 2),
                   width/2 + BARRIER_GAP / 2,
                   width * (7/8) - BARRIER_WIDTH * 2]
# Variables determing how many barriers to place
NUM_ROWS_BARRIERS = 3
NUM_COLUMNS_BARRIERS = 4 # A space after every 4 barriers

class Barrier(Entity.Entity):
    # Class for the barrier
    def __init__(self, x, y):
        bitmap = pygame.image.load(BARRIER_SPRITES[0]).convert()
        super(Barrier,self).__init__(x, y, bitmap)
        
        # Stage of damager barrier is in (default is 0)
        self.stage = 0

    def Move(self):
        pass

    def Damage(self):
        self.stage += 1
        if self.stage < len(BARRIER_SPRITES):
            self._bitmap = pygame.image.load(BARRIER_SPRITES[self.stage]).convert()
            return False
        else:
            self._bitmap.fill(Colours.BLACK)
            return True