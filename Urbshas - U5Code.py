'''
Trevor Urbshas
Kevin Reid
ICS 3U Space Invaders
January 2, 2014
January 6, 2014
This program is a remake of Space Invaders rewritten in Python for the culminating activity.
'''

# Import libraries
import pygame,math

# Initialize pygame
pygame.init()

#------Define Lists------
# List of sprites, in order of row starting from the top
SPRITES = ['small_invader1.png','medium_invader1.png','medium_invader1.png','large_invader1.png','large_invader1.png']
ALTERNATE_SPRITES = ['small_invader2.png','medium_invader2.png','medium_invader2.png','large_invader2.png','large_invader2.png']
# Store the enemies in lists
row1 = []
row2 = []
row3 = []
row4 = []
row5 = []
aliens = [row1,row2,row3,row4,row5]
#------------------------

#----Define variables----
    # Maybe add the option to change resolution later??????
    #in original, enemies are in rows of 11 an of 5 height
RESOLUTION_LIST = [(640,360),(1024,576),(1280,720),(1366,768),(1600,900),(1920,1080)]
width = 640 # this is left lowercase because I may add the option to change the resolution of the screen
height = int(width * (56/65))
WINDOW_SIZE = (width,height)

# How far the aliens are moved from their starting positions
alien_x_shift = 0
# How fast the aliens will move, in pixels per second
alien_x_change = 10
# Same for y coordinate
alien_y_shift = 0
alien_y_change = 16 # 16 is the height of the aliens

# Specifications of aliens
ALIEN_WIDTH = 24 # This is the width of the largest alien. It is used to make sure all the aliens line up vertically
ALIEN_HEIGHT = 16 # All of the aliens are 16 pixels tall
ALIEN_SPACING = 10
NUM_ALIENS = 11 # This is number of aliens per row
NUM_ROWS = 5 # The number of rows of aliens
current_sprites = SPRITES # Determines which sprite is currently being used for the aliens

# Offset amount is used so aliens start in the middle of the screen
X_OFFSET = (width - ((ALIEN_WIDTH * NUM_ALIENS) + (ALIEN_SPACING * (NUM_ALIENS - 1)))) / 2
Y_OFFSET = (height - ((ALIEN_WIDTH * NUM_ROWS) + (ALIEN_SPACING * (NUM_ROWS - 1)))) / 4

# Player specifications
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 32
PLAYER_SPRITE = 'core_cannon.png'
player_x_change = 0 # How fast/which direction the player sprite moves. Default is 0, value changes when the user presses a key
player_lives = 3
# Variables used to determine how fast/ where a player character should be moving
player_x_change1 = 0
player_x_change2 = 0

# Variables to determine if the aliens have already been shifted or not
has_shifted = False
# Variable to determine whether to move the aliens downwards or not
shift_downwards = False
# Variable to determine when to reset the aliens
reboot = True
# Variable used to end the main program loop when the user clicks the exit button
done = False
# Start a counter to make the aliens move every second
alien_clock = 0
alien_clock_change = 1 # This variable is used to determine how fast the aliens are drawn and therefor how fast they move
# Start a counter to control when the UFO spawns
ufo_clock = 0
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

#----Reset the aliens----
def reset():
    # This function will reset the variables as well as the position of the aliens and place them in the middle of the screen
    # These variables must be declared global
    global alien_x_shift
    alien_x_shift = 0
    global alien_x_change
    alien_x_change = 10
    global alien_y_shift
    alien_y_shift = 0
    global alien_y_change
    alien_y_change = 16
    global alien_clock
    alien_clock = 0
    global ufo_clock
    ufo_clock = 0
    global reboot
    reboot = True
#-----------------------
# Open the window
SCREEN = pygame.display.set_mode(WINDOW_SIZE)
# Window title
pygame.display.set_caption('Python Invaders: A Simplified Version of the Classic Space Invaders Arcade Game')
#--------Classes--------
# Open a class for all sprites
class Sprite():
    # Function to set the x,y, and sprite attributes more easily
    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.bitmap = pygame.image.load(sprite).convert()
        self.bitmap.set_colorkey(BLACK)
    # Function to set the position of the object when needed
    def set_position(self,x,y):
        self.x = x
        self.y = y
    # Function to render the sprite before being placed on the screen
    def render(self):
        SCREEN.blit(self.bitmap,[self.x,self.y])

class Alien(Sprite):
    # Modified __init__ function to include the alien's row
    def __init__(self,x,y,row,sprite):
        self.x = x
        self.y = y
        self.row = row
        self.bitmap = pygame.image.load(sprite).convert()
        self.bitmap.set_colorkey(BLACK)

class UFO():
    x = -32 # This puts the ufo offscreen by 1 width of itself
    y = height - (7/8 * height)
    x_change = 2
    sprite = pygame.image.load('ufo.png').convert()
    
    def draw(self):
        x = self.x
        y = self.y
        sprite = self.sprite
        screen.blit(sprite,[x,y])
#------------------------

#--------Main loop--------
while not done:
    #----------------------All event processing below here----------------------
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        # If the user pressed a key down
        if event.type == pygame.KEYDOWN:
            # If the player pushed down the left arrow key
            if event.key == pygame.K_LEFT:
                player_x_change1 = -5
            # If the player pushed down the right arrow key
            if event.key == pygame.K_RIGHT:
                player_x_change2 = 5
        # If a user let a key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_x_change1 = 0
            if event.key == pygame.K_RIGHT:
                player_x_change2 = 0
    #----------------------All event processing above here----------------------
    # This variable is used to change the player character's x position
    player_x_change_total = player_x_change1 + player_x_change2

    #-------------------------All game logic below here-------------------------
    alien_clock += 1
    # Switch sprites every time the aliens move
    if alien_clock >= 29:
        if current_sprites == SPRITES:
            current_sprites = ALTERNATE_SPRITES
        else:
            current_sprites = SPRITES
    ufo_clock += 1
    #-------------------------All game logic above here-------------------------


    #------------------------All code to draw below here------------------------
    # Clear the screen before objects are drawn
    SCREEN.fill(BLACK)

    # Draw the aliens
    # Only execute this code if it is the first time the program boots up or if the player wins the round
    if reboot:
        # Give the aiens a position in a list
        for row_number in range(NUM_ROWS):
            alien_x_pos = X_OFFSET # x coordinate of alien on the far left
            alien_y_pos = Y_OFFSET + alien_y_shift # y coordinate of row
            for alien in range(NUM_ALIENS):
                # Add the alien to a list of aliens and load its respective sprite
                aliens[row_number].append(Alien(alien_x_pos,alien_y_pos,row_number,SPRITES[row_number]))
                alien_x_pos += ALIEN_WIDTH + ALIEN_SPACING
            alien_y_shift += ALIEN_HEIGHT + ALIEN_SPACING
        # Create the player sprite
        player_sprite = Sprite(width/2 - PLAYER_WIDTH/2,height - PLAYER_HEIGHT,PLAYER_SPRITE)
        reboot = False
    player_sprite.render()
    player_sprite.x += player_x_change_total
    # Reverse the aliens' direction of travel and shift them downwards if the reach either end of the screen
    if alien_clock >= 29:
        for i in range(NUM_ROWS):
            # If the last alien on the right reaches the right side of the screen
            # If the first alien on the left reaches the left side of the screen
            if aliens[i][len(aliens[i]) - 1].x >= (width - (ALIEN_WIDTH + 20)) or aliens[i][0].x <= 20:
                if not has_shifted: # Only execute this if the aliens have not been shifted downwards already
                    shift_downwards = True # Shift downwards
                else:
                    alien_x_change = alien_x_change * -1 # Reverse direction
                    has_shifted = False
                break # Break the loop so that the direction of travel is not reversed multiple times
            
    # Render and animate the aliens
    for row in aliens:
        for alien in row:
            alien.render()
            if alien_clock >= 29: # If it has been a half second since the last time they moved
                if shift_downwards: # Move the aliens downward if necessary(explained below)
                    alien.y += alien_y_change # Shift the aliens downwards
                    has_shifted = True
                else:
                    alien.x += alien_x_change # Shift the aliens
                # Switch the sprites
                alien.bitmap = pygame.image.load(current_sprites[alien.row]).convert()

    pygame.display.flip()
    #------------------------All code to draw above here------------------------

                
    # Reset the clocks and variables
    if alien_clock >= 29:
        alien_clock = 0 # The clock must be reset at the end of the frame so that it does not affect the drawing of the aliens
    if shift_downwards: # Tell the program not to shift the aliens down
        shift_downwards = False
    # Limit to 60 frames per second
    clock.tick(60)
pygame.quit()
