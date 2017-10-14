import Entity
import pygame

# List of sprites for the alien missiles
ALIEN_MISSILE_SPRITES_A = [
	os.path.join('python invaders images','alien_missile1A.png'),
	os.path.join('python invaders images','alien_missile2A.png')
]

ALIEN_MISSILE_SPRITES_B = [
	os.path.join('python invaders images','alien_missile1B.png'),
	os.path.join('python invaders images','alien_missile2B.png')
]

class Missile(Entity.Entity):
    def __init__(self,x,y,sprite,width,height,*random_num): # random_num is used for the alien missiles to determine which sprite the missile will have
        super(Missile,self).__init__()
        if random_num:
            self.random_num = random_num[0]
        
        self.sprite = sprite
        self.bitmap = pygame.image.load(self.sprite).convert()
        self.surface = pygame.Surface([width,height])
        self.rect = self.image.get_rect()

    def update(self):
        # Shift the missile upwards
        global PLAYER_MISSILE_SPEED
        self.rect.y -= PLAYER_MISSILE_SPEED