import pygame
from Source import Colours
from Source import Entity
from typing import List

HEADER_TEXT_Y_SPACING = 4
HEADER_LINE_THICKNESS = 3
HEADER_HEIGHT = 39

class Header(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super(Header, self).__init__()
        self._score = 0
        self._lives = 0
        self._rect = pygame.Rect(x, y, width, height)
        self._font = pygame.font.Font(None, 45)
        
    def UpdateValues(self, score, lives):
        self._score = score
        self._lives = lives

    def Render(self, screen) -> List[pygame.Rect]:
        score_text = self._font.render('SCORE   ' + str(self._score), False, Colours.WHITE)
        lives_text = self._font.render('LIVES   ' + str(self._lives), False, Colours.WHITE)

        scores_rect = screen.blit(score_text, [self._rect.left + 10, self._rect.top + HEADER_TEXT_Y_SPACING])
        lives_rect = screen.blit(lives_text, [self._rect.centerx, self._rect.top + HEADER_TEXT_Y_SPACING])

        line_rect = pygame.draw.line(screen, Colours.GREEN, [self._rect.left, scores_rect.bottom + HEADER_TEXT_Y_SPACING], [self._rect.right, scores_rect.bottom + HEADER_TEXT_Y_SPACING], HEADER_LINE_THICKNESS)

        return [self._rect, line_rect]

