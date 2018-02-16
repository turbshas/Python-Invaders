'''
Trevor Urbshas
Kevin Reid
ICS 3U Space Invaders
January 2, 2014
January 26, 2014
This program is a remake of Space Invaders rewritten in Python for the culminating activity.
'''

# Import libraries
import os
import pygame
import random
import time
from Source import Alien
from Source import Barrier
from Source import Colours
from Source import Entity
from Source import GameState
from Source import Header
from Source import Missile
from Source import PlayerEntity
from Source import UFO

#----Define functions------------------------
def Reset(game_state: GameState.GameState):
    game_state.alien_x_speed = 10
    game_state.alien_y_speed = Alien.ALIEN_HEIGHT
    game_state.reset_screen = True
    game_state.ResetState()
    
def RedrawScreen(game_state: GameState.GameState, aliens: pygame.sprite.Group, columns: pygame.sprite.Group, player: pygame.sprite.GroupSingle):
    alien_y_shift = 0

    if len(player) > 0:
        pygame.display.update(player.sprite.Clear(game_state.GetScreen()))
    
    for row_number in range(Alien.NUM_ROWS):
        alien_x_pos = Alien.X_OFFSET
        alien_y_pos = Alien.Y_OFFSET + alien_y_shift
        
        for column_number in range(Alien.NUM_ALIENS):
            alien = Alien.Alien(alien_x_pos, \
                                alien_y_pos, \
                                row_number, \
                                column_number)
            alien.add(aliens)
            columns[column_number].append(alien)
            alien_x_pos += Alien.ALIEN_MAX_WIDTH + Alien.ALIEN_SPACING
            
        alien_y_shift += Alien.ALIEN_HEIGHT + Alien.ALIEN_SPACING

    player_sprite = PlayerEntity.PlayerSprite(game_state.GetScreenWidth()/2 - PlayerEntity.PLAYER_WIDTH/2, \
                                                game_state.GetScreenHeight() - PlayerEntity.PLAYER_HEIGHT)
    player_sprite.add(player)
    
def FlashPlayerSprite(screen, player_sprite):
    for i in range(3):
        rect = pygame.draw.rect(screen, Colours.BLACK, player_sprite.GetRect())
        pygame.display.update([rect])
        time.sleep(0.5)
        pygame.display.update(player_sprite.Render(screen))
        time.sleep(0.5)

def GetLeftmostColumn(columns):
    for i in range(0, len(columns), 1):
        if len(columns[i]) > 0:
            return columns[i]

def GetRightmostColumn(columns):
    for i in range(len(columns) - 1, -1, -1):
        if len(columns[i]) > 0:
            return columns[i]
#--------------------------------------------

def main():
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
    #------Define Groups-----
    aliens = pygame.sprite.Group()
    bottom_row = pygame.sprite.Group()
    alien_missiles = pygame.sprite.Group()
    ufo = pygame.sprite.GroupSingle()
    player = pygame.sprite.GroupSingle()
    player_missile = pygame.sprite.GroupSingle()
    barriers = pygame.sprite.Group()
    destroyed_objects = pygame.sprite.Group()

    dirty_rects = []
    #------------------------
    """
    
    """

    #-------|Main loop|-------
    GAME_STATE = GameState.GameState()

    # General State
    GAME_STATE.move_aliens = False
    GAME_STATE.shift_aliens_down = False
    GAME_STATE.sort_shooting_aliens = True
    GAME_STATE.reset_screen = True
    GAME_STATE.done = False

    # UFO Specifications
    GAME_STATE.ufo_start_x = 0 - UFO.UFO_WIDTH # This will place the ufo offscreen at the beginning and will start the ufo on the side it left

    # Alien Specifications
    GAME_STATE.alien_x_speed = 10
    GAME_STATE.alien_y_speed = Alien.ALIEN_HEIGHT

    # Player Specifications
    GAME_STATE.player_x_speed = 0
    GAME_STATE.player_lives = 3
    GAME_STATE.score = 0

    # Missile Specification
    GAME_STATE.current_alien_missile_sprites = Missile.MissileSpriteType.NORMAL
    # Empty list to be able to add and delete the player_missile object
    GAME_STATE.shoot_player_missile = False

    GAME_STATE.StartGame()
    Reset(GAME_STATE)

    HEADER = Header.Header(0, 0, GAME_STATE.GetScreenWidth(), Header.HEADER_HEIGHT)
    UFO.UFO(-UFO.UFO_WIDTH, Alien.Y_OFFSET - 40).add(ufo)

    # Place the barriers, this will only run at the beginning of the program
    for barrier_group in Barrier.BARRIER_GROUP_X:
        current_barrier_row = 0
        for row_number in range(Barrier.NUM_ROWS_BARRIERS):
            barrier_x = barrier_group
            barrier_y = GAME_STATE.GetScreenHeight() * (3/4) + (Barrier.BARRIER_HEIGHT * current_barrier_row)
            for column_number in range(Barrier.NUM_COLUMNS_BARRIERS):
                new_barrier = Barrier.Barrier(barrier_x, barrier_y)
                new_barrier.add(barriers)
                dirty_rects.extend(new_barrier.Render(GAME_STATE.GetScreen()))
                barrier_x += Barrier.BARRIER_WIDTH
            current_barrier_row += 1

    pygame.display.update(dirty_rects)
    dirty_rects.clear()

    while not GAME_STATE.done:
        # Process events
        GAME_STATE.ProcessEvents(pygame.event.get())

        #------------------------|All game logic below here|------------------------
        #########################--|Alien Code below here|--########################
        if GAME_STATE.reset_screen:
            GAME_STATE.reset_screen = False
            RedrawScreen(GAME_STATE, aliens, columns, player)

        # Sort the aliens at the bottom of the alien_list group and determine which ones can shoot
        if GAME_STATE.sort_shooting_aliens:
            GAME_STATE.sort_shooting_aliens = False
            for column in columns:
                if len(column) > 0:
                    column[len(column) - 1].add(bottom_row)
    
        # Reverse the aliens' direction of travel and shift them downwards if they reach either end of the screen
        if GAME_STATE.RunAlienEvents():
            if GetLeftmostColumn(columns)[0].AtBounds(GAME_STATE.GetScreen()) \
                or GetRightmostColumn(columns)[0].AtBounds(GAME_STATE.GetScreen()):
                 if GAME_STATE.move_aliens:
                    GAME_STATE.shift_aliens_down = True
                 else:
                    GAME_STATE.alien_x_speed = GAME_STATE.alien_x_speed * -1
                    GAME_STATE.move_aliens = True
                    GAME_STATE.IncreaseAlienSpeed()
                    
        # Random chance for the aliens in can_shoot_list to shoot
        for alien in bottom_row:
            if alien.GetRect().bottom >= player.sprite.GetRect().top:
                GAME_STATE.GameOver()
                GAME_STATE.done = True
            if alien.TryShoot():
                rand_num = random.randint(0,1)
                missile_type = Missile.MissileType.SLOW if rand_num == 0 else Missile.MissileType.FAST
                missile = Missile.Missile(alien.GetRect().centerx - Missile.ALIEN_MISSILE_WIDTH / 2, \
                                          alien.GetRect().bottom, \
                                          missile_type)
                missile.add(alien_missiles)
        #########################--|Alien Code above here|--########################


        ##########################--|UFO Code below here|--#########################
        if ufo.sprite.IsSpawned():
            ufo.sprite.Move()
        else:
            ufo.sprite.TrySpawn()
        ##########################--|UFO Code above here|--#########################
            

        #########################--|Player Code below here|--#######################
        if not player.sprite.AtLeftBound(GAME_STATE.GetScreen()) \
                and not player.sprite.AtRightBound(GAME_STATE.GetScreen()) \
            or (player.sprite.AtLeftBound(GAME_STATE.GetScreen()) and GAME_STATE.player_x_speed > 0) \
            or (player.sprite.AtRightBound(GAME_STATE.GetScreen()) and GAME_STATE.player_x_speed < 0):
            player.sprite.speed = GAME_STATE.player_x_speed
            player.sprite.Move()
            dirty_rects.extend(player.sprite.Render(GAME_STATE.GetScreen()))

        if GAME_STATE.shoot_player_missile and len(player_missile) < 1:
                GAME_STATE.shoot_player_missile = False
                player_missile_object = Missile.Missile(player.sprite.GetRect().centerx - (Missile.PLAYER_MISSILE_WIDTH/2), \
                                                        player.sprite.GetRect().top - Missile.PLAYER_MISSILE_HEIGHT, \
                                                        Missile.MissileType.PLAYER)
                player_missile_object.add(player_missile)
        #######################--|Player Code above here|--#########################


        #######################--|Collision Code below here|--#########################
        # Determine if the alien missile has hit the player
        player_hit = pygame.sprite.spritecollide(player.sprite, alien_missiles, False)
        if len(player_hit) > 0:
            for missile in player_hit:
                missile.kill()
                dirty_rects.extend(missile.Render(GAME_STATE.GetScreen()))
                del missile
            GAME_STATE.player_lives -= 1
            FlashPlayerSprite(GAME_STATE.GetScreen(), player.sprite)

        # Check if player missile hit anything
        collision = False
        if len(player_missile) > 0:
            aliens_hit = pygame.sprite.spritecollide(player_missile.sprite, aliens, False)
            ufos_hit = pygame.sprite.spritecollide(player_missile.sprite, ufo, False)
            barriers_hit = pygame.sprite.spritecollide(player_missile.sprite, barriers, False)
            alien_missiles_hit = pygame.sprite.spritecollide(player_missile.sprite, alien_missiles, False)
        
            for alien in aliens_hit:
                collision = True
                GAME_STATE.score += alien.score
                alien.kill()
                dirty_rects.extend(alien.Clear(GAME_STATE.GetScreen()))
                del columns[alien.column][alien.row]
            
                for row_number in range(len(columns[alien.column])):
                    columns[alien.column][row_number].row = row_number
                
                GAME_STATE.sort_shooting_aliens = True
                if len(aliens) < 1:
                    Reset(GAME_STATE)
                    GAME_STATE.player_lives += 1
                
            for ufo_hit in ufos_hit:
                collision = True
                GAME_STATE.score += ufo_hit.score
                GAME_STATE.shoot_player_missile = False
                GAME_STATE.sort_shooting_aliens = True
                ufo_hit.Destroy(GAME_STATE.GetScreen())
                dirty_rects.extend(ufo_hit.Render(GAME_STATE.GetScreen()))

            if len(barriers_hit) > 0:
                collision = True
                if barriers_hit[0].Damage():
                    barriers_hit[0].kill()
                    dirty_rects.extend(barriers_hit[0].Clear(GAME_STATE.GetScreen()))
                else:
                    dirty_rects.extend(barriers_hit[0].Render(GAME_STATE.GetScreen()))

            for alien_missile in alien_missiles_hit:
                collision = True
                alien_missile.kill()
                dirty_rects.extend(alien_missile.Render(GAME_STATE.GetScreen()))
            
        if collision:
            sprite = player_missile.sprite
            sprite.kill()
            dirty_rects.extend(sprite.Clear(GAME_STATE.GetScreen()))
            del sprite

        collision_dict = pygame.sprite.groupcollide(alien_missiles, barriers, False, False)
        for missile, barriers_hit in collision_dict.items():
            # do stuff?
            for barrier in barriers_hit:
                if barrier.Damage():
                    barrier.kill()
                    dirty_rects.extend(barrier.Clear(GAME_STATE.GetScreen()))
                else:
                    dirty_rects.extend(barrier.Render(GAME_STATE.GetScreen()))

            missile.kill()
            dirty_rects.extend(missile.Clear(GAME_STATE.GetScreen()))

        collision_dict = pygame.sprite.groupcollide(aliens, barriers, False, False)
        for alien, barriers_hit in collision_dict.items():
            for barrier in barriers_hit:
                barrier.kill()
                dirty_rects.extend(barrier.Clear(GAME_STATE.GetScreen()))
        #######################--|Collision Code above here|--#########################
        #------------------------|All game logic above here|------------------------


        #-----------------------|All code to draw below here|-----------------------
        # Clear the screen before objects are drawn
        GAME_STATE.GetScreen().fill(Colours.BLACK)

        # End game if player has zero lives
        if GAME_STATE.player_lives == 0:
            GAME_STATE.GameOver()
            GAME_STATE.done = True

        # Draw ufo if it has spawned
        if ufo.sprite.IsSpawned():
            dirty_rects.extend(ufo.sprite.Render(GAME_STATE.GetScreen()))
        
        # Draw header and update score
        HEADER.UpdateValues(GAME_STATE.score, GAME_STATE.player_lives)
        dirty_rects.extend(HEADER.Render(GAME_STATE.GetScreen()))
        
        # Render player missile
        if len(player_missile) > 0:
            if player_missile.sprite.IsOffScreen(GAME_STATE.GetScreen()):
                sprite = player_missile.sprite
                sprite.kill()
                del sprite
                GAME_STATE.shoot_player_missile = False
            else:
                player_missile.sprite.Move()
                dirty_rects.extend(player_missile.sprite.Render(GAME_STATE.GetScreen()))

        # Render the player on the screen
        dirty_rects.extend(player.sprite.Render(GAME_STATE.GetScreen()))

        # Render the barriers on screen
        for barrier in barriers:
            barrier.Render(GAME_STATE.GetScreen())

        # Render and animate the aliens
        if GAME_STATE.RunAlienEvents():
            for alien in aliens:
                if GAME_STATE.shift_aliens_down:
                    alien.speed_x = 0
                    alien.speed_y = GAME_STATE.alien_y_speed
                    GAME_STATE.move_aliens = False
                else:
                    alien.speed_x = GAME_STATE.alien_x_speed
                    alien.speed_y = 0
                alien.Move()
                alien.ToggleSprite()
                dirty_rects.extend(alien.Render(GAME_STATE.GetScreen()))

        # Draw the missiles
        for missile in alien_missiles:
            if missile.IsOffScreen(GAME_STATE.GetScreen()):
                missile.kill()
                del missile
            else:
                missile.Move()
                if GAME_STATE.IsSpriteToggleTick():
                    missile.ToggleSprite()
                dirty_rects.extend(missile.Render(GAME_STATE.GetScreen()))

        pygame.display.update(dirty_rects)
        dirty_rects.clear()
        #-----------------------|All code to draw above here|-----------------------
        if GAME_STATE.shift_aliens_down:
            GAME_STATE.shift_aliens_down = False

        GAME_STATE.TickClock()
        GAME_STATE.TickAlienClock()

    # Print a game over message in the Python shell
    print("""You have run out of lives, the game will now end.
    You scored""", GAME_STATE.score, """points!
    Restart the game to play again!""")

        
# Initialize pygame
pygame.init()
if __name__ == "__main__": main()
pygame.quit()

