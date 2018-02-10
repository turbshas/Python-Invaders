import Entity
import os
import pygame

# List of sprites for the alien missiles
MISSILE_SPRITES = [
	[
		os.path.join('python invaders images','alien_missile1A.png'),
		os.path.join('python invaders images','alien_missile1B.png')
	],
	[
		os.path.join('python invaders images','alien_missile2A.png'),
		os.path.join('python invaders images','alien_missile2B.png'),
	],
	[
		os.path.join('python invaders images','player_missile.png')
	]
]

PLAYER_MISSILE_WIDTH = 4
PLAYER_MISSILE_HEIGHT = 12
PLAYER_MISSILE_SPEED = 8

ALIEN_MISSILE_WIDTH = 12
ALIEN_MISSILE_HEIGHT = 25 # 25 is the height of the largest missile
SLOW_MISSILE_SPEED = 4 # The speed of the type 1 alien missiles
FAST_MISSILE_SPEED = 6 # The speed of the type 2 alien missiles

MISSILE_WIDTHS_BY_TYPE = [
	ALIEN_MISSILE_WIDTH,
	ALIEN_MISSILE_WIDTH,
	PLAYER_MISSILE_WIDTH
]

MISSILE_HEIGHTS_BY_TYPE = [
	ALIEN_MISSILE_HEIGHT,
	ALIEN_MISSILE_HEIGHT,
	PLAYER_MISSILE_HEIGHT
]

class MissileType:
	SLOW = 0
	FAST = 1
	PLAYER = 2
	
class MissileSpriteType:
	NORMAL = 0
	ALTERNATE = 1

class Missile(Entity.Entity):
	def __init__(self, x, y, missile_type, missile_sprite_type):
		sprite = MISSILE_SPRITES[missile_type][missile_sprite_type]
		width = MISSILE_WIDTHS_BY_TYPE[missile_type]
		height = MISSILE_HEIGHTS_BY_TYPE[missile_type]
		super(Missile, self).__init__(x, y, pygame.image.load(sprite).convert(), pygame.Surface([width,height]))
		
		self._missile_type = missile_type
		self._sprite_type = missile_sprite_type

	def Move(self):
		# Shift the missile upwards
		if self._missile_type == MissileType.PLAYER:
			self.rect.y -= PLAYER_MISSILE_SPEED
		else:
			if self._missile_type == MissileType.SLOW:
				self.rect.y += SLOW_MISSILE_SPEED
			else:
				self.rect.y += FAST_MISSILE_SPEED
	
	def UpdateSprite(self, missile_sprite_type):
		self._sprite_type = missile_sprite_type
		sprite = MISSILE_SPRITES[self._missile_type][self._sprite_type]
		self._bitmap = pygame.image.load(sprite).convert()
		