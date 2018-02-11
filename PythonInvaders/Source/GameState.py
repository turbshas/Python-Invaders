import pygame

RESOLUTION_LIST = [(640,360),(1024,576),(1280,720),(1366,768),(1600,900),(1920,1080)]
FPS = 60
HALF_SECOND = FPS/2
CAPTION = 'Python Invaders: A Simplified Version of the Classic Space Invaders Arcade Game'
GAME_OVER_TEXT = 'GAME OVER'

class GameState:
    def __init__(self, screen_width, screen_height):
        self._window_size = (screen_width, screen_height)
        self._screen = None
        self._alien_clock = 0
        self._clock = pygame.time.Clock()
        
        # General State
        self.move_aliens = False
        self.shift_aliens_down = False
        self.sort_shooting_aliens = True
        self.reset_screen = True
        self.done = False
        
        # UFO Specifications
        self.ufo_start_x = None
        
        # Alien Specifications
        self.current_alien_prites = None
        self.alien_x_speed = None
        self.alien_y_speed = None
        
        # Player Specifications
        self.player_x_speed = None
        self.player_lives = None
        self.score = None
        
        # Missile Specification
        self.current_alien_missile_sprites = None
        self.shoot_player_missile = False
        
    def GetAlienClock(self):
        return self._alien_clock
        
    def AlienClockIsEven(self):
        return self._alien_clock & 0x1 == 0
    
    def TickAlienClock(self):
        self._alien_clock += 1
        if self._alien_clock >= FPS/2:
            self._alien_clock = 0
        
    def GetClock(self):
        return self._clock
        
    def TickClock(self):
        self._clock.tick(FPS)
        
    def GetScreen(self):
        return self._screen
    
    def StartGame(self):
        self._screen = pygame.display.set_mode(self._window_size)
        pygame.display.set_caption(CAPTION)
        
    def GameOver(self):
        self._screen.blit(GAME_OVER_TEXT, \
                        [self._window_size[0]/2 - len(GAME_OVER_TEXT), self._window_size[1]/2])
    
    def ResetState(self):
        self._alien_clock = 0
    
    def ProcessEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player_x_speed -= 5
                if event.key == pygame.K_RIGHT:
                    self.player_x_speed += 5
                if event.key == pygame.K_SPACE:
                    self.shoot_player_missile = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player_x_speed += 5
                if event.key == pygame.K_RIGHT:
                    self.player_x_speed -= 5
                    
    def RunAlienEvents(self):
        return self._alien_clock >= FPS/2 -1