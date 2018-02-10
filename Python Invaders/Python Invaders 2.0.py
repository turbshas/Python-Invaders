'''
Trevor Urbshas
Kevin Reid
ICS 3U Space Invaders
January 2, 2014
January 26, 2014
This program is a remake of Space Invaders rewritten in Python for the culminating activity.
'''

# Import libraries
import Alien
import Colours
import Entity
import GameState
import Missile
import os
import PlayerEntity
import pygame
import random
import time
import UFO

# Display the controls and rules in the python shell at startup
print("""Welcome to Python Invaders, a recreation of the Space Invaders video game in Python!

To move the player left, press the ← key
To move the player right, press the → key
To fire a missile, press SPACE

Kill the aliens to gain points! Kill all the aliens on the screen and gain 1 extra life!
Small Alien = 40 Points
Medium Alien = 20 Points
Large Alien = 10 Points
UFO = ??? Points

The game will end when you have run out of lives, or when you quit the game! Enjoy!""")
# Initialize pygame
pygame.init()

#------Define Lists------
# Columns of aliens used to determine which aliens can shoot
column1 = []
column2 = []
column3 = []
column4 = []
column5 = []
column6 = []
column7 = []
column8 = []
column9 = []
column10 = []
column11 = []
columns = [column1,column2,column3,column4,column5,column6,column7,column8,column9,column10,column11]

# List that will be used to contain aliens that have been hit by a missile
alien_hit = []
#------------------------

#----Define variables----
width = 640
height = 480
GAME_STATE = GameState.GameState(width, height)

# General State
GAME_STATE.move_aliens = False
GAME_STATE.shift_aliens_down = False
GAME_STATE.sort_shooting_aliens = True
GAME_STATE.reset_screen = True
GAME_STATE.done = False

# UFO Specifications
GAME_STATE.ufo_start_x = 0 - UFO.UFO_WIDTH # This will place the ufo offscreen at the beginning and will start the ufo on the side it left

# Alien Specifications
GAME_STATE.current_alien_sprites = Alien.AlienSpriteType.NORMAL # Determines which sprite is currently being used for the aliens
GAME_STATE.alien_x_speed = 10
GAME_STATE.alien_y_speed = Alien.ALIEN_HEIGHT

# Player Specifications
GAME_STATE.player_x_speed = 0
GAME_STATE.player_lives = 3
GAME_STATE.score = 0

# Missile Specification
GAME_STATE.current_alien_missile_sprites = Missile.MissileSpriteType.NORMAL
# Empty list to be able to add and delete the player_missile object
player_missile_list = [] #TODO
GAME_STATE.shoot_player_missile = False

# Offset amount is used so aliens start in the middle of the screen
X_OFFSET = (width - ((Alien.ALIEN_MAX_WIDTH * Alien.NUM_ALIENS) + (Alien.ALIEN_SPACING * (Alien.NUM_ALIENS - 1)))) / 2
Y_OFFSET = (height - ((Alien.ALIEN_HEIGHT * Alien.NUM_ROWS) + (Alien.ALIEN_SPACING * (Alien.NUM_ROWS - 1)))) / 4



# Font sizes
font = pygame.font.Font(None,25)
large_font = pygame.font.Font(None,45)

# y coordinate of green header line and header text
HEADER_TEXT_Y = 4
HEADER_LINE_Y = Y_OFFSET - 55
#------------------------
#------Define Groups-----
aliens = pygame.sprite.Group()
can_shoot_list = pygame.sprite.Group()
alien_missiles = pygame.sprite.Group()
ufos = pygame.sprite.GroupSingle()
player = pygame.sprite.GroupSingle()
barriers = pygame.sprite.Group()
#------------------------
#----Define functions----
def Reset(game_state):
	game_state.alien_x_speed = 10
	game_state.alien_y_speed = Alien.ALIEN_HEIGHT
	game_state.reset_screen = True
	game_state.ResetState()
	
def RedrawScreen(game_state, aliens, columns, player):
	alien_y_shift = 0
	
	for row_number in range(Alien.NUM_ROWS):
		alien_x_pos = X_OFFSET
		alien_y_pos = Y_OFFSET + alien_y_shift
		
		for column_number in range(Alien.NUM_ALIENS):
			alien = Alien.Alien(alien_x_pos, \
								alien_y_pos, \
								row_number, \
								column_number, \
								game_state.current_alien_sprites)
			alien.add(aliens)
			columns[column_number].append(alien)
			alien_x_pos += Alien.ALIEN_MAX_WIDTH + Alien.ALIEN_SPACING
			
		alien_y_shift += Alien.ALIEN_HEIGHT + Alien.ALIEN_SPACING
		
	player_sprite = PlayerEntity.PlayerSprite(width/2 - PlayerEntity.PLAYER_WIDTH/2, \
											  height - PlayerEntity.PLAYER_HEIGHT)
	player_sprite.add(player)
	
def FlashPlayerSprite(screen, player_sprite):
	for i in range(4):
		pygame.draw.rect(screen, Colours.BLACK, player_sprite.GetRect())
		pygame.display.flip()
		time.sleep(0.5)
		player_sprite.Render(screen)
		pygame.display.flip()
		time.sleep(0.5)
#-----------------------
GAME_STATE.StartGame()

Reset(GAME_STATE)
#------------------------

# The barriers were disbled because of lag issues
"""
# Place the barriers, this will only run at the beginning of the program
for barrier_group in BARRIER_GROUP_X:
	current_barrier_row = 0
	for row_number in range(NUM_ROWS_BARRIERS):
		barrier_x = barrier_group
		barrier_y = height * (3/4) + (BARRIER_HEIGHT * current_barrier_row)
		for column_number in range(NUM_COLUMNS_BARRIERS):
			Barrier(barrier_x,barrier_y).add(barrier_list)
			barrier_x += BARRIER_WIDTH
		current_barrier_row += 1
"""
# Temp area for refactoring
ufo = UFO.UFO(-UFO.UFO_WIDTH, Y_OFFSET - 40)
# Temp area for refactoring

#-------|Main loop|-------
while not GAME_STATE.done:
	# Process events
	GAME_STATE.ProcessEvents(pygame.event.get())

	#------------------------|All game logic below here|------------------------
	#########################--|Alien Code below here|--########################
	GAME_STATE.TickAlienClock()

	if GAME_STATE.reset_screen:
		GAME_STATE.reset_screen = False
		RedrawScreen(GAME_STATE, aliens, columns, player)

	# Sort the aliens at the bottom of the alien_list group and determine which ones can shoot
	if GAME_STATE.sort_shooting_aliens:
		GAME_STATE.sort_shooting_aliens = False
		for column in columns:
			if len(column) > 0:
				column[len(column) - 1].add(can_shoot_list)
		
	# Reverse the aliens' direction of travel and shift them downwards if the reach either end of the screen
	if GAME_STATE.RunAlienEvents():
		for alien in aliens:
			if alien.AtBounds(GAME_STATE.GetScreen()):
				if GAME_STATE.move_aliens:
					GAME_STATE.shift_aliens_down = True
					
					for alien in can_shoot_list:
						if alien.GetRect().y >= ((height - PlayerEntity.PLAYER_HEIGHT) + 20):
							GAME_STATE.GameOver()
							GAME_STATE.done = True
				else:
					GAME_STATE.alien_x_speed = GAME_STATE.alien_x_speed * -1
					GAME_STATE.move_aliens = True
				break
		# Switch sprites
		if GAME_STATE.current_alien_sprites == Alien.AlienSpriteType.NORMAL:
			GAME_STATE.current_alien_sprites = Alien.AlienSpriteType.ALTERNATE
		else:
			GAME_STATE.current_alien_sprites = Alien.AlienSpriteType.NORMAL

	# Random chance for the aliens in can_shoot_list to shoot
	for alien in can_shoot_list:
		alien_shoot_number = random.randint(1, Alien.ALIEN_SHOOT_CHANCE)
		if alien_shoot_number == Alien.ALIEN_SHOOT_CHANCE:
			rand_num = random.randint(0,1)
			missile_type = Missile.MissileType.SLOW if rand_num == 0 else Missile.MissileType.FAST
			missile = Missile.Missile(alien.GetRect().x + (Alien.ALIEN_WIDTH[alien.row]/2), \
									  alien.GetRect().y + Alien.ALIEN_HEIGHT, \
									  missile_type, \
									  GAME_STATE.current_alien_missile_sprites)
			missile.add(alien_missiles)

	# Determine if the alien missile has hit the player
	player_hit = pygame.sprite.spritecollide(player.sprite, alien_missiles, False)
	if len(player_hit) > 0:
		for missile in player_hit:
			missile.kill()
			del missile
		GAME_STATE.player_lives -= 1
		FlashPlayerSprite(GAME_STATE.GetScreen(), player.sprite)
	
	if GAME_STATE.AlienClockIsEven():
		if GAME_STATE.current_alien_missile_sprites == Missile.MissileSpriteType.NORMAL:
			GAME_STATE.current_alien_missile_sprites = Missile.MissileSpriteType.ALTERNATE
		else:
			GAME_STATE.current_alien_missile_sprites = Missile.MissileSpriteType.NORMAL
	#########################--|Alien Code above here|--########################


	##########################--|UFO Code below here|--#########################
	if ufo.IsSpawned():
		ufo.Move()
	else:
		ufo.TrySpawn()
	##########################--|UFO Code above here|--#########################
			

	#########################--|Player Code below here|--#######################
	if not player.sprite.AtLeftBound(GAME_STATE.GetScreen()) \
			and not player.sprite.AtRightBound(GAME_STATE.GetScreen()) \
		or (player.sprite.AtLeftBound(GAME_STATE.GetScreen()) and GAME_STATE.player_x_speed > 0) \
		or (player.sprite.AtRightBound(GAME_STATE.GetScreen()) and GAME_STATE.player_x_speed < 0):
		player.sprite.speed = GAME_STATE.player_x_speed
		player.sprite.Move()

	if GAME_STATE.shoot_player_missile and len(player_missile_list) < 1:
			player_missile_object = Missile.Missile(player.sprite.GetRect().center[0] - (Missile.PLAYER_MISSILE_WIDTH/2), \
													player.sprite.GetRect().top - Missile.PLAYER_MISSILE_HEIGHT, \
													Missile.MissileType.PLAYER, \
													Missile.MissileSpriteType.NORMAL)
			player_missile_list.append(player_missile_object)
	
	collision = False
	if len(player_missile_list) >= 1:
		aliens_hit = pygame.sprite.spritecollide(player_missile_list[0], aliens, False)
		ufos_hit = pygame.sprite.spritecollide(player_missile_list[0], ufos, False)
		
		for alien in aliens_hit:
			collision = True
			GAME_STATE.score += alien.score
			alien.kill()
			del columns[alien.column][alien.row]
			
			for row_number in range(len(columns[alien.column])):
				columns[alien.column][row_number].row = row_number
				
			GAME_STATE.sort_shooting_aliens = True
			GAME_STATE.shoot_player_missile = False
			if len(aliens) < 1:
				Reset(GAME_STATE)
				GAME_STATE.player_lives += 1
				
		for ufo in ufos_hit:
			GAME_STATE.score += ufo.score
			GAME_STATE.shoot_player_missile = False
			GAME_STATE.sort_shooting_aliens = True
			ufo.Destroy()
			
	if collision:
		del player_missile_list[0]
	#######################--|Player Code above here|--#########################
	#------------------------|All game logic above here|------------------------


	#-----------------------|All code to draw below here|-----------------------
	# Clear the screen before objects are drawn
	GAME_STATE.GetScreen().fill(Colours.BLACK)
	if GAME_STATE.player_lives == 0:
		GAME_STATE.GameOver()
		GAME_STATE.done = True
	if ufo.IsSpawned():
		ufo.Render(GAME_STATE.GetScreen())
	##############--|Score and life counter header below here|--################
	# Header separating line
	pygame.draw.line(GAME_STATE.GetScreen(), Colours.GREEN, [0, HEADER_LINE_Y], [width, HEADER_LINE_Y], 3)
	# Variable holding the score text
	score_text = large_font.render('SCORE   ' + str(GAME_STATE.score), False, Colours.WHITE)
	GAME_STATE.GetScreen().blit(score_text, [10, HEADER_TEXT_Y])
	lives_text = large_font.render('LIVES   ' + str(GAME_STATE.player_lives), False, Colours.WHITE)
	GAME_STATE.GetScreen().blit(lives_text, [width - ((PlayerEntity.PLAYER_WIDTH * 4) + (Alien.ALIEN_SPACING * 3) + 30), HEADER_TEXT_Y])
	
	if GAME_STATE.shoot_player_missile:
		if player_missile_object.IsOffScreen(GAME_STATE.GetScreen()):
			del player_missile_list[0]
			GAME_STATE.shoot_player_missile = False
		else:
			player_missile_list[0].Render(GAME_STATE.GetScreen())
			player_missile_list[0].Move()

	# Render the player on the screen
	player.sprite.Render(GAME_STATE.GetScreen())

	# Barriers disabled for lag reasons
	"""
	# Render the barriers on screen
	for barrier in barrier_list:
		barrier.render()
	"""
	# Render and animate the aliens
	for alien in aliens:
		alien.Render(GAME_STATE.GetScreen())
		if GAME_STATE.RunAlienEvents():
			if GAME_STATE.shift_aliens_down:
				alien.GetRect().y += GAME_STATE.alien_y_speed
				GAME_STATE.move_aliens = False
			else:
				alien.GetRect().x += GAME_STATE.alien_x_speed
			alien.UpdateSprite(GAME_STATE.current_alien_sprites)

	# Draw the missiles in the alien_missiles
	for missile in alien_missiles:
		if missile.IsOffScreen(GAME_STATE.GetScreen()):
			missile.kill()
			del missile
		else:
			missile.Move()
			missile.UpdateSprite(GAME_STATE.current_alien_missile_sprites)
			missile.Render(GAME_STATE.GetScreen())

	pygame.display.flip()
	#-----------------------|All code to draw above here|-----------------------
	if GAME_STATE.shift_aliens_down:
		GAME_STATE.shift_aliens_down = False
	GAME_STATE.TickClock()

# Print a game over message in the Python shell
print("""You have run out of lives, the game will now end.
You scored""", GAME_STATE.score, """points!
Restart the game to play again!""")

pygame.quit()
