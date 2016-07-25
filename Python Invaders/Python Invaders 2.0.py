'''
Trevor Urbshas
Kevin Reid
ICS 3U Space Invaders
January 2, 2014
January 26, 2014
This program is a remake of Space Invaders rewritten in Python for the culminating activity.
'''

# Import libraries
import pygame,os,random,time

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
# List of sprites, in order of row starting from the top
SPRITES = [os.path.join('python invaders images','small_invader1.png'),os.path.join('python invaders images','medium_invader1.png'),os.path.join('python invaders images','medium_invader1.png'),os.path.join('python invaders images','large_invader1.png'),os.path.join('python invaders images','large_invader1.png')]
ALTERNATE_SPRITES = [os.path.join('python invaders images','small_invader2.png'),os.path.join('python invaders images','medium_invader2.png'),os.path.join('python invaders images','medium_invader2.png'),os.path.join('python invaders images','large_invader2.png'),os.path.join('python invaders images','large_invader2.png')]
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
column_list = [column1,column2,column3,column4,column5,column6,column7,column8,column9,column10,column11]
# List of sprites for the alien missiles
ALIEN_MISSILE_SPRITES_A = [os.path.join('python invaders images','alien_missile1A.png'),os.path.join('python invaders images','alien_missile2A.png')]
ALIEN_MISSILE_SPRITES_B = [os.path.join('python invaders images','alien_missile1B.png'),os.path.join('python invaders images','alien_missile2B.png')]
# List of barrier sprites
BARRIER_SPRITES = [os.path.join('python invaders images','barrier_stage0.png'),os.path.join('python invaders images','barrier_stage1.png'),os.path.join('python invaders images','barrier_stage2.png'),os.path.join('python invaders images','barrier_stage3.png')]
# List of point values for each row
ALIEN_POINTS = [40,20,20,10,10]
UFO_POINTS = [50,100,150,200,250,300]
# List that will be used to contain aliens that have been hit by a missile
alien_hit = []
#------------------------

#----Define variables----
    # Maybe add the option to change resolution later?
    #in original, enemies are in rows of 11 and of 5 height
RESOLUTION_LIST = [(640,360),(1024,576),(1280,720),(1366,768),(1600,900),(1920,1080)]
width = 640 # this is left lowercase because I may add the option to change the resolution of the screen
height = 480
WINDOW_SIZE = (width,height)
FPS = 60 # How many times the game updates per second

# UFO Specifications
ufo_spawned = False # Variable to determine whether to spawn the UFO or not
UFO_SPRITE = os.path.join('python invaders images','ufo.png') # The ufo's bitmapped sprite
UFO_WIDTH = 48
UFO_HEIGHT = 21
ufo_start_x = 0 - UFO_WIDTH # This will place the ufo offscreen at the beginning and will start the ufo on the side it left
ufo_speed = 1 # The speed of the ufo, in pixels/tick

# Specifications of aliens
ALIEN_WIDTH = [16,22,22,24,24] # This list holds the width of the aliens in each row, e.g. aliens in row 1 are width 16 pixels, aliens in row 2 are 22 pixels etc.
ALIEN_FAKE_WIDTH = 24 # This is the width of the largest alien. It is used to make sure all the aliens line up vertically
ALIEN_HEIGHT = 16 # All of the aliens are 16 pixels tall
ALIEN_SPACING = 10
NUM_ALIENS = 11 # This is number of aliens per row
NUM_ROWS = 5 # The number of rows of aliens
ALIEN_SHOOT_CHANCE = 900 # 1/ALIEN_SHOOT_CHANCE the aliens will shoot at the player
current_sprites = SPRITES # Determines which sprite is currently being used for the aliens
# How fast the aliens will move, in pixels per second
alien_x_change = 10
# Same for y coordinate
alien_y_shift = 0
alien_y_change = 16 # 16 is the height of the aliens

# Offset amount is used so aliens start in the middle of the screen
X_OFFSET = (width - ((ALIEN_FAKE_WIDTH * NUM_ALIENS) + (ALIEN_SPACING * (NUM_ALIENS - 1)))) / 2
Y_OFFSET = (height - ((ALIEN_HEIGHT * NUM_ROWS) + (ALIEN_SPACING * (NUM_ROWS - 1)))) / 4

# Player specifications
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 28
PLAYER_SPRITE = os.path.join('python invaders images','core_cannon.png')
player_x_change = 0 # How fast/which direction the player sprite moves. Default is 0, value changes when the user presses a key
player_lives = 3
# Variables used to determine how fast/ where a player character should be moving
player_x_change1 = 0
player_x_change2 = 0
# Variable holding score
score = 0

# The barriers have been omitted from the program as they cause too much lag in the game, however you may enable it if need be
"""
# Barrier specifications
BARRIER_WIDTH = 12
BARRIER_HEIGHT = 12
# Place of the groups of barriers
BARRIER_GROUP_X = [width/8 - ((BARRIER_WIDTH * 4)/2),width/2 - ((BARRIER_WIDTH * 4) + 50),width/2 + 50,width * (7/8) - ((BARRIER_WIDTH * 4)/2)]
# Variables determing how many barriers to place
NUM_ROWS_BARRIERS = 3
NUM_COLUMNS_BARRIERS = 4 # A space after every 4 barriers
"""

# Specifications of missiles
PLAYER_MISSILE_SPRITE = os.path.join('python invaders images','player_missile.png')
PLAYER_MISSILE_WIDTH = 4
PLAYER_MISSILE_HEIGHT = 12
PLAYER_MISSILE_SPEED = 8
ALIEN_MISSILE_WIDTH = 12
ALIEN_MISSILE_HEIGHT = 25 # 25 is the height of the largest missile
SLOW_MISSILE_SPEED = 4 # The speed of the type 1 alien missiles
FAST_MISSILE_SPEED = 6 # The speed of the type 2 alien missiles
alien_current_missile_sprites = ALIEN_MISSILE_SPRITES_A # The default sprite list for the alien missiles
# Empty list to be able to add and delete the player_missile object
player_missile_list = []
shoot_missile = False # This determines when to shoot a missile from the player sprite

# Font sizes
font = pygame.font.Font(None,25)
large_font = pygame.font.Font(None,45)

# Text printed on the screen if the player loses
GAME_OVER_TEXT = 'GAME OVER'
# y coordinate of green header line and header text
HEADER_TEXT_Y = 4
HEADER_LINE_Y = Y_OFFSET - 55
# Variables to determine if the aliens have already been shifted or not
has_shifted = False
# Variable to determine whether to move the aliens downwards or not
shift_downwards = False
# Variable to determine when to sort the aliens to determine which ones can shoot
sort_shooting_aliens = True
# Variable to determine when to reset the aliens
reboot = True
# Variable used to end the main program loop when the user clicks the exit button
done = False
# Start a counter to make the aliens move every second
alien_clock = 0
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#------------------------

#-----Define colours-----
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#------------------------

#----Define functions----
# Reset the aliens
def reset():
    # This function will reset the variables as well as the position of the aliens and place them in the middle of the screen
    # These variables must be declared global
    global alien_x_change,alien_y_shift,alien_y_change,alien_clock,reboot
    alien_x_change = 10
    alien_y_shift = 0
    alien_y_change = 16
    alien_clock = 0
    reboot = True
#-----------------------
# Open the window
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
# Window title
pygame.display.set_caption('Python Invaders: A Simplified Version of the Classic Space Invaders Arcade Game')
#--------Classes--------
# Open a class for all sprites
class PlayerSprite(pygame.sprite.Sprite):
    # Function to set the x,y, and sprite attributes more easily
    def __init__(self,x,y): 
        super(PlayerSprite,self).__init__()
        self.bitmap = pygame.image.load(PLAYER_SPRITE).convert()
        self.bitmap.set_colorkey(BLACK)
        # Physical image of the player on screen
        self.image = pygame.Surface([PLAYER_WIDTH,PLAYER_HEIGHT])
        # A rectangle representing an approximation of the sprite's image
        self.rect = self.image.get_rect()
        # x coordinate of player
        self.rect.x = x
        # y coordinate of player
        self.rect.y = y
    # Function to render the sprite before being placed on the screen
    def render(self):
        SCREEN.blit(self.bitmap,[self.rect.x,self.rect.y])

class Alien(pygame.sprite.Sprite):
    def __init__(self,x,y,row,column):
        # global variables used in this function
        global ALIEN_POINTS,SPRITES,ALIEN_WIDTH,ALIEN_HEIGHT
        super(Alien,self).__init__() # It is necessary to call the parent class so that it may be added to a group
        # The row the alien is in
        self.row = row
        # The column the alien is in, this is used to determine if the alien should shoot or not
        self.column = column
        # The amount of points the player gets for destroying the alien
        self.score = ALIEN_POINTS[row]
        # The alien's sprite image
        self.bitmap = pygame.image.load(SPRITES[row]).convert()
        # The physical image of the alien that the sprite takes up on the screen
        self.image = pygame.Surface([ALIEN_WIDTH[self.row],ALIEN_HEIGHT])
        # A rectangle representing an approximation of the sprite's image
        self.rect = self.image.get_rect()
        # x coordinate of the rectangle
        self.rect.x = x
        # y coordinate of the rectangle
        self.rect.y = y

    def render(self):
        # Make the background of the sprite image file transparent
        self.bitmap.set_colorkey(BLACK)
        # Render the alien on the screen
        SCREEN.blit(self.bitmap,self.rect)

class Missile(pygame.sprite.Sprite):
    def __init__(self,x,y,sprite,width,height,*random_num): # random_num is used for the alien missiles to determine which sprite the missile will have
        super(Missile,self).__init__()
        if random_num:
            self.random_num = random_num[0]
        # The missile's sprite image
        self.sprite = sprite
        self.bitmap = pygame.image.load(self.sprite).convert()
        # The physical image of the missile that the sprite takes up on the screen
        self.image = pygame.Surface([width,height])
        # A rectangle representing an approximation of the sprite's image
        self.rect = self.image.get_rect()
        # x coordinate of the rectangle
        self.rect.x = x
        # y coordinate of the rectangle
        self.rect.y = y

    def update(self):
        # Shift the missile upwards
        global PLAYER_MISSILE_SPEED
        self.rect.y -= PLAYER_MISSILE_SPEED

    def render(self):
        # Make the background of the missile image transparent
        self.bitmap.set_colorkey(BLACK)
        # Render the missile on the screen
        SCREEN.blit(self.bitmap,self.rect)
        
class UFO(pygame.sprite.Sprite):
    # Class for the UFO
    def __init__(self,x,y,score):
        super(UFO,self).__init__() # It is necessary to call the parent class so that it may be added to a group
        # The physical image of the ufo that the sprite takes up on the screen
        self.image = pygame.Surface([UFO_WIDTH,UFO_HEIGHT])
        # A rectangle representing an approximation of the sprite's image
        self.rect = self.image.get_rect()
        # x coordinate of the ufo
        self.rect.x = x
        # y coordinate of ufo
        self.rect.y = y
        # Score the player is awarded for destroying the ufo
        self.score = score
        # Bitmap image of the ufo
        self.bitmap = pygame.image.load(UFO_SPRITE).convert()

    def render(self):
        # Render the ufo on the screen
        SCREEN.blit(self.bitmap,self.rect)

# As stated above, the barriers cause a lot of lag from all of them being rendered at the same time
"""
class Barrier(pygame.sprite.Sprite):
    # Class for the barrier
    def __init__(self,x,y):
        super(Barrier,self).__init__()
        # Image of sprite on screen
        self.image = pygame.Surface([BARRIER_WIDTH,BARRIER_HEIGHT])
        # Rectangle representing an approximation of the sprite's image
        self.rect = self.image.get_rect()
        # x coord of rect
        self.rect.x = x
        # y coord of rect
        self.rect.y = y
        # Stage of damager barrier is in (default is 0)
        self.stage = 0

    def render(self):
        # Reset the bitmap image, if the barrier's stage has changed
        self.bitmap = pygame.image.load(BARRIER_SPRITES[self.stage]).convert()
        # Draw the barrier
        SCREEN.blit(self.bitmap,self.rect)
"""
#------------------------

#------Define Groups-----
alien_list = pygame.sprite.Group() # This group holds all the aliens
can_shoot_list = pygame.sprite.Group() # This group holds all the aliens that can shoot at the player i.e. the aliens with the highest y coordinate
alien_missile_list = pygame.sprite.Group() # This group holds all the alien missiles
ufo_list = pygame.sprite.GroupSingle() # This group will hold the ufo when it is on the screen. It will be used to check collision between it and the missile
player_sprite_group = pygame.sprite.GroupSingle() # This group will be used to check for collisions
barrier_list = pygame.sprite.Group() # This group will hold a list of the barriers on the screen
#------------------------
reset()
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
#-------|Main loop|-------
while not done:
    #---------------------|All event processing below here|---------------------
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        # If the user pressed a key down
        if event.type == pygame.KEYDOWN:
            # If the player pushed down the left arrow key
            if event.key == pygame.K_LEFT:
                player_x_change1 = -5 # This variable will always be used for moving left and will always be negative
            # If the player pushed down the right arrow key
            if event.key == pygame.K_RIGHT:
                player_x_change2 = 5 # This variable will always be used for moving right and will always be positive
            # If the player pressed down the spacebar
            if event.key == pygame.K_SPACE:
                shoot_missile = True
        # If a user let a key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_change1 = 0
            if event.key == pygame.K_RIGHT:
                player_x_change2 = 0
    #---------------------|All event processing above here|---------------------


    #------------------------|All game logic below here|------------------------
    #########################--|Alien Code below here|--########################
    alien_clock += 1

    # Only execute this code if it is the first time the program boots up or if the player wins the round
    if reboot:
        # Give the aiens a position in a list
        for row_number in range(NUM_ROWS):
            alien_x_pos = X_OFFSET # x coordinate of alien on the far left
            alien_y_pos = Y_OFFSET + alien_y_shift # y coordinate of row
            for column_number in range(NUM_ALIENS):
                # Create an alien object
                current_alien = Alien(alien_x_pos,alien_y_pos,row_number,column_number)
                # Add the alien to a list of aliens
                current_alien.add(alien_list)
                # Add the alien to its column position in a list
                column_list[column_number].append(current_alien)
                alien_x_pos += ALIEN_FAKE_WIDTH + ALIEN_SPACING
            alien_y_shift += ALIEN_HEIGHT + ALIEN_SPACING
        # Create the player sprite
        player_sprite = PlayerSprite(width/2 - PLAYER_WIDTH/2,height - PLAYER_HEIGHT)
        #player_sprite.add(player_sprite_group)
        reboot = False

    # Sort the aliens at the bottom of the alien_list group and determine which ones can shoot
    if sort_shooting_aliens:
        for column in column_list:
            if len(column) > 0: # If there is an alien in the selected column
                column[len(column) - 1].add(can_shoot_list) # Add the alien in the very last position of the column to the can_shoot_list
        sort_shooting_aliens = False # Make sure the program does not sort the aliens every tick
        
    # Reverse the aliens' direction of travel and shift them downwards if the reach either end of the screen
    if alien_clock >= (FPS/2 - 1):
        for alien in alien_list:
            # If the last alien on the right reaches the right side of the screen
            # If the first alien on the left reaches the left side of the screen
            if alien.rect.x >= (width - (ALIEN_FAKE_WIDTH + 20)) or alien.rect.x <= 20:
                if not has_shifted: # Only execute this if the aliens have not been shifted downwards already
                    shift_downwards = True # Shift downwards
                    # Check if the aliens have reached the bottom of the screen
                    for alien in alien_list:
                        # If the aliens touch the bottom of the screen
                        if alien.rect.y >= ((height - PLAYER_HEIGHT) + 20):
                            SCREEN.blit(GAME_OVER_TEXT,[width/2 - len(GAME_OVER_TEXT)/2,height/2])
                else:
                    alien_x_change = alien_x_change * -1 # Reverse direction
                    has_shifted = False
                break # Break the loop so that the direction of travel is not reversed  and aliens are not shifted downwards multiple times 
        # Switch sprites every time the aliens move
        if current_sprites == SPRITES:
            current_sprites = ALTERNATE_SPRITES
        else:
            current_sprites = SPRITES

    # Random chance for the aliens in can_shoot_list to shoot
    for alien in can_shoot_list:
        alien_shoot_number = random.randint(1,ALIEN_SHOOT_CHANCE)
        if alien_shoot_number == ALIEN_SHOOT_CHANCE: # This means the aliens have a 1/ALIEN_SHOOT_CHANCE chance to shoot
            rand_num = random.randint(0,1) # Choose a random number between 0 and 1, this will be used to determine which sprite it will use
            temp_missile_variable = Missile(alien.rect.x + (ALIEN_WIDTH[alien.row]/2),alien.rect.y + ALIEN_HEIGHT,alien_current_missile_sprites[rand_num],ALIEN_MISSILE_WIDTH,ALIEN_MISSILE_HEIGHT,rand_num)
            temp_missile_variable.add(alien_missile_list)

    # Determine if the alien missile has hit the player
    player_hit = pygame.sprite.spritecollide(player_sprite,alien_missile_list,False)
    if len(player_hit) > 0:
        for missile in player_hit: # A player could be hit by 2 missile at the same time
            missile.kill() # Delete all the missiles in the list
            del missile
        player_lives -= 1 # Subtract a life from the player
        counter = 0 # Start a counter to determine how many times to flash the player sprite
        while counter < 3: # Do this 3 times
            pygame.draw.rect(SCREEN,BLACK,player_sprite.rect) # Cover the player sprite with a black rectangle
            pygame.display.flip() # Flip image to the display
            time.sleep(0.5) # Wait half a second
            player_sprite.render() # Draw the player sprite over the black rectangle
            pygame.display.flip() # Flip image to the display
            time.sleep(0.5) # Wait a half second
            counter +=1 # Add 1 to the counter
    
    if alien_clock % 2 == 0: # Change the alien missile sprite every 2 ticks
        if alien_current_missile_sprites == ALIEN_MISSILE_SPRITES_A:
            alien_current_missile_sprites = ALIEN_MISSILE_SPRITES_B
        else:
            alien_current_missile_sprites = ALIEN_MISSILE_SPRITES_A
    #########################--|Alien Code above here|--########################


    ##########################--|UFO Code below here|--#########################
    # If the isn't already a ufo on the screen
    if not ufo_spawned:
        # Random chance for the alien to spawn
        random_ufo_chance = random.randint(1,180)
        if random_ufo_chance == 180:
            # Choose a score for the player to be awarded for destroying the ufo
            ufo_score = random.randrange(0,5) # This will be used a list index and as lists start at 0, so does this
            # Define the ufo object
            ufo = UFO(ufo_start_x,Y_OFFSET - 40,UFO_POINTS[ufo_score])
            # Place the ufo in a group
            ufo.add(ufo_list)
            #ufo.render()
            ufo_spawned = True

    if ufo_spawned:
        ufo.rect.x += ufo_speed
        if ufo.rect.x <= (0 - UFO_WIDTH) or ufo.rect.x >= width:
            ufo_start_x = ufo.rect.x
            ufo_speed = ufo_speed * -1
            del ufo
            ufo_spawned = False
    ##########################--|UFO Code above here|--#########################
            

    #########################--|Player Code below here|--#######################
    # If the player is within 5 pixels of the left side of the screen
    if player_sprite.rect.x <= player_x_change1 * -1 and player_sprite.rect.x >= player_x_change1:
        # Stop the player from moving left
        player_x_change1 = 0
    # If the player is within 5 pixels of the right side of the screen
    elif player_sprite.rect.x <= (width - PLAYER_WIDTH) + player_x_change2 and player_sprite.rect.x >= (width - PLAYER_WIDTH) - player_x_change2:
        # Stop the player from moving right
        player_x_change2 = 0
    # Move the player by adding the two x change values to the player sprite's x value
    player_sprite.rect.x += player_x_change1 + player_x_change2
    
    # If the player pressed down the spacebar and if there is not already a missile on the screen
    if shoot_missile and len(player_missile_list) < 1:
            # Create the missile object and place it in the list
            player_missile_object = Missile(player_sprite.rect.x + ((PLAYER_WIDTH/2) - (PLAYER_MISSILE_WIDTH/2)),player_sprite.rect.y - PLAYER_MISSILE_HEIGHT,PLAYER_MISSILE_SPRITE,PLAYER_MISSILE_WIDTH,PLAYER_MISSILE_HEIGHT,0)
            player_missile_list.append(player_missile_object)

    # Check if the player's missile collided with an alien
    if len(player_missile_list) == 1:
        # The missile collides with anything
        alien_hit = pygame.sprite.spritecollide(player_missile_list[0],alien_list,False) # The False value indicates that if any sprites do collide, it will not remove them from their groups
        if len(alien_hit) > 0:
            # Increase the score value
            score += alien_hit[0].score
            # Remove the missile from the screen
            del player_missile_list[0]
            # Remove the alien from the screen
            alien_hit[0].kill()
            # Remove the alien from the list of columns, so it cannot shoot again
            del column_list[alien_hit[0].column][alien_hit[0].row]
            for row_number in range(len(column_list[alien_hit[0].column])): # Adjust the row attribute of the aliens in the column
                column_list[alien_hit[0].column][row_number].row = row_number
            sort_shooting_aliens = True # Recalculate which aliens can shoot
            shoot_missile = False # Tell the program that the missile is now gone
            # If there are no aliens left on the screen, redraw them
            if len(alien_list) < 1:
                reset()
                player_lives += 1
        # Check if the player's missile collided with the ufo
        elif pygame.sprite.spritecollide(player_missile_list[0],ufo_list,False):
            # Create a variable to access the attributes of the ufo and delete it
            ufo_hit = pygame.sprite.spritecollide(player_missile_list[0],ufo_list,False)
            score += ufo_hit[0].score # Increase the player's score
            del player_missile_list[0] # Delete the missile
            shoot_missile = False
            sort_shooting_aliens = True # Recalculate which aliens can shoot
            del ufo_hit # Delete the ufo
            ufo_spawned = False
    #######################--|Player Code above here|--#########################
    #------------------------|All game logic above here|------------------------


    #-----------------------|All code to draw below here|-----------------------
    # Clear the screen before objects are drawn
    SCREEN.fill(BLACK)
    if player_lives == 0:
        game_over_text = large_font.render('GAME OVER',False,WHITE)
        SCREEN.blit(game_over_text,[width/2 - 100,height/2])
        done = True
    if ufo_spawned:
        ufo.render()
    ##############--|Score and life counter header below here|--################
    # Header separating line
    pygame.draw.line(SCREEN,GREEN,[0,HEADER_LINE_Y],[width,HEADER_LINE_Y],3)
    # Variable holding the score text
    score_text = large_font.render('SCORE   ' + str(score),False,WHITE) # False means the text is not antialiased
    SCREEN.blit(score_text,[10,HEADER_TEXT_Y])
    lives_text = large_font.render('LIVES   ' + str(player_lives),False,WHITE)
    SCREEN.blit(lives_text,[width - ((PLAYER_WIDTH * 4) + (ALIEN_SPACING * 3) + 30),HEADER_TEXT_Y])
    
    # If the player pressed down the spacebar
    if shoot_missile:
        # Render the missile on screen and move it upwards
        player_missile_list[0].render()
        player_missile_list[0].update()
        # If the missile is at the top of the screen
        if player_missile_object.rect.y < HEADER_LINE_Y:
            # Delete the missile from the list, thus allowing another missile to be fired
            del player_missile_list[0]
            shoot_missile = False

    # Render the player on the screen
    player_sprite.render()

    # Barriers disabled for lag reasons
    """
    # Render the barriers on screen
    for barrier in barrier_list:
        barrier.render()
    """
    # Render and animate the aliens
    for alien in alien_list:
        alien.render()
        if alien_clock >= (FPS/2 -1): # If it has been a half second since the last time they moved
            if shift_downwards: # Move the aliens downward if necessary
                alien.rect.y += alien_y_change # Shift the aliens downwards
                has_shifted = True
            else:
                alien.rect.x += alien_x_change # Shift the aliens
            # Switch the sprites
            alien.bitmap = pygame.image.load(current_sprites[alien.row]).convert()

    # Draw the missiles in the alien_missile_list
    for missile in alien_missile_list:
        missile.render()
        # If the missile is of type 1, it travels slower
        if missile.sprite == ALIEN_MISSILE_SPRITES_A[0] or missile.sprite == ALIEN_MISSILE_SPRITES_B[0]:
            missile.rect.y += SLOW_MISSILE_SPEED
        # If the missile is not of type 1(therefore it is type 2 because there are only 2 types), it travels faster
        else:
            missile.rect.y += FAST_MISSILE_SPEED
        missile.bitmap = pygame.image.load(alien_current_missile_sprites[missile.random_num]).convert()
        if missile.rect.y == height:
            missile.kill()
            del missile

    pygame.display.flip()
    #-----------------------|All code to draw above here|-----------------------
    # Reset the clocks and variables
    if alien_clock >= (FPS/2 - 1):
        alien_clock = 0 # The clock must be reset at the end of the frame so that it does not affect the drawing of the aliens
    if shift_downwards: # Tell the program not to shift the aliens down
        shift_downwards = False
    # Limit to 60 frames per second
    clock.tick(FPS)

# Print a game over message in the Python shell
print("""You have run out of lives, the game will now end.
You scored""",score,"""points!
Restart the game to play again!""")

pygame.quit()
