'''
Final Project: Alien Invasion (Milestone 3)
Darian Marie Bruce
04/26/2026
This module deals with the HUD of the game
'''

import pygame.font
from pygame import Surface, Rect
import pygame
#from typing import TYPE_CHECKING

#if TYPE_CHECKING:
   # from alien_invasion import AlienInvasion

class HUD:
    '''This class creates and manages the HUD elements that
    display player lives, score, high score, max score, and current level
    '''
    def __init__(self, game) -> None:
        '''This initalizes HUD elements and prepares visual components
        Arguments: game (AlienInvasion): the main game instance providing access to screen,
        settings, and game statistics'''
        self.game = game
        self.settings = game.settings
        self.screen: Surface = game.screen
        self.boundaries: Rect = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font: pygame.font.Font = pygame.font.Font(self.settings.font_file, 
            self.settings.hud_font_size)
        self.padding: int = 20
        self._setup_life_image()
        self.update_scores()
        self.update_level()

    def _setup_life_image(self) -> None:
        '''This module loads and scales the image used to represent remaining lives
        '''
        self.life_image: Surface = pygame.image.load(self.settings.heart_file)
        self.life_image = pygame.transform.scale(self.life_image, (
                self.settings.heart_w, self.settings.heart_h
                ))
        self.life_rect: Rect = self.life_image.get_rect()

    def update_scores(self) -> None:
        '''This method updates the score related HUD elements'''
        self._update_max_score()
        self._update_score()
        self._update_hi_score()

        

    def _update_score(self) -> None:
        '''This method renders and positions the current score display
        '''
        self.score_str: str = f'Score: {self.game_stats.score:,.0f}'
        self.score_image: Surface = self.font.render(self.score_str, True,
                self.settings.text_color, None)
        self.score_rect: Rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + (self.padding * 1.5)

    def _update_max_score(self) -> None:
        '''This method renders and postions the max score display'''
        self.max_score_str: str = f'Max-Score: {self.game_stats.max_score:,.0f}'
        self.max_score_image: Surface = self.font.render(self.max_score_str, True,
                self.settings.text_color, None)
        self.max_score_rect: Rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_hi_score(self) -> None:
        '''This method renders and positions the high score display
        '''
        self.hi_score_str: str = f'Hi-Score: {self.game_stats.hi_score:,.0f}'
        self.hi_score_image: Surface = self.font.render(self.hi_score_str, True,
                self.settings.text_color, None)
        self.hi_score_rect: Rect = self.hi_score_image.get_rect()
        self.hi_score_rect.right = self.boundaries.right - self.padding
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self) -> None:
        '''This method renders and positions the update level display
        '''
        self.level_str: str = f'Level: {self.game_stats.level:,.0f}'
        self.level_image: Surface = self.font.render(self.level_str, True,
                self.settings.text_color, None)
        self.level_rect: Rect = self.level_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.top = self.life_rect.bottom + (self.padding * 1.5)

    def _draw_lives(self) -> None:
        '''This method draws remaining lives as hearts on the screen
        '''
        current_x: int = self.padding
        current_y: int = self.padding
        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def _draw_panel(self, rect: Rect, padding: int = 10) -> None:
        '''This method draws a background panel
        Arguments: 
        rect (rect): the rectangle of the UI element
        padding (int): space added around the panel
        '''
        panel_rect = pygame.Rect(
            rect.left - padding,
            rect.top - padding,
            rect.width + padding * 2,
            rect.height + padding * 2
        )
        pygame.draw.rect(self.screen, (0, 0, 0), panel_rect)

    def _draw_outlined_text(self, text: str, rect: Rect) -> None:
        '''This method draws text with a black outline
        Arguments:
        text(str): the text string to render
        rect(rect): the position where the text should be drawn
        '''
        outline = self.font.render(text, True, (0, 0, 0))
        main = self.font.render(text, True, self.settings.text_color)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            self.screen.blit(outline, (rect.x + dx, rect.y + dy))
        self.screen.blit(main, rect)

    def draw(self) -> None:
        '''Draws the HUD elements onto the screen'''
        self._draw_panel(self.hi_score_rect)
        self.screen.blit(self.hi_score_image, self.hi_score_rect)

        self._draw_outlined_text(self.score_str, self.score_rect)
        self._draw_outlined_text(self.max_score_str, self.max_score_rect)

        self._draw_outlined_text(self.level_str, self.level_rect)

        self._draw_lives()