'''
Trevor Urbshas
Kevin Reid
ICS 3U Space Invaders
January 2, 2014
[Date Completed]
This program is a remake of Space Invaders rewritten in Python for the culminating activity.
'''

# Import pygame and math
import pygame,math

#------Define Lists------
# Create empty lists for each row of aliens starting from the top
row1 = []
row2 = []
row3 = []
row4 = []
row5 = []
aliens_positions = [row1,row2,row3,row4,row5]
#------------------------

#----Define variables----
    # Maybe add the option to change resolution later??????
    #in original, enemies are in rows of 11 an of 5 height
resolution_list = [(640,360),(1024,576),(1280,720),(1366,768),(1600,900),(1920,1080)]
width = 640
height = int(width * (56/65))
window_size = (width,height)

# Set a value to the x coordinate of the aliens at the beginning
alien_x_pos_start = 0
# How fast the aliens will move, in pixels per second
alien_x_pos_change = 5
# Same for y coordinate
alien_y_start_pos = 0
alien_y_pos_change = 5

# Specifications of aliens
alien_width = 30
alien_height = 20
alien_spacing = 10
num_aliens = 11 # This is number of aliens per row

# Offset amount is used so aliens start in the middle of the screen
x_offset = (width - ((alien_width * num_aliens) + (alien_spacing * (num_aliens - 1)))) / 2
y_offset = (height - ((alien_height * len(aliens_positions)) + (alien_spacing * (len(aliens_positions) - 1)))) / 4

# Variable used to end the main program loop when the user clicks the exit button
done = False
y_position = 0
#------------------------

#-----Define colours-----
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#------------------------

# Initiate pygame
pygame.init()
# Open the window
screen = pygame.display.set_mode(window_size)
# Window title
pygame.display.set_caption('Python Invaders: A Simplified Version of the Classic Space Invaders Arcade Game')
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Start a counter to make the aliens move every second
alien_clock = 0

#--------Main loop--------
while not done:
    # All event processing below here
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
    # All event processing above here


    # All game logic below here

    # All game logic above here


    # All code to draw below here
    # Clear the screen before objects are drawn
    screen.fill(BLACK)
    # Draw Aliens
    # Run through each row
    for row_number in range(len(aliens_positions)):
        x_position = alien_x_pos_start
        # Run through each alien in the row
        for alien_number in range(num_aliens):
            # Set the x coordinate
            x = x_position + x_offset
            # Set the y coordinate
            y = y_position + y_offset
            # Append the list
            #pygame.draw.rect(screen,WHITE,[x,y,alien_width,alien_height])
            aliens_positions[row_number].append([x,y])
            # Move to the next alien
            x_position += alien_width + alien_spacing
            if alien_clock >= 59:
                x_pos_start += x_pos_change
                alien_clock = 0
            print(aliens_positions)
        y_position += alien_height + alien_spacing               
    pygame.display.flip()
    # All code to draw above here
    done = True
    alien_clock += 1
    # Limit to 60 frames per second
    clock.tick(1)
pygame.quit()

