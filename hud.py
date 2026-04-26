'''
Final Project: Alien Invasion (Milestone 3)
Darian Marie Bruce
04/26/2026
This module deals with the HUD of the game
'''

import pygame.font
#from typing import TYPE_CHECKING

#if TYPE_CHECKING:
   # from alien_invasion import AlienInvasion

class HUD:

    def __init__(self, game) -> None:
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_file, 
            self.settings.hud_font_size)
        self.padding = 20
        self._setup_life_image()
        self.update_scores()
        self.update_level()

    def _setup_life_image(self) -> None:
        self.life_image = pygame.image.load(self.settings.heart_file)
        self.life_image = pygame.transform.scale(self.life_image, (
                self.settings.heart_w, self.settings.heart_h
                ))
        self.life_rect = self.life_image.get_rect()

    def update_scores(self) -> None:
        self._update_max_score()
        self._update_score()
        self._update_hi_score()

        

    def _update_score(self) -> None:
        score_str = f'Score: {self.game_stats.score:,.0f}'
        self.score_image = self.font.render(score_str, True,
                self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + (self.padding * 1.5)

    def _update_max_score(self) -> None:
        max_score_str = f'Max-Score: {self.game_stats.max_score:,.0f}'
        self.max_score_image = self.font.render(max_score_str, True,
                self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_hi_score(self) -> None:
        hi_score_str = f'Hi-Score: {self.game_stats.hi_score:,.0f}'
        self.hi_score_image = self.font.render(hi_score_str, True,
                self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.right = self.boundaries.right - self.padding
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self) -> None:
        level_str = f'Level: {self.game_stats.level:,.0f}'
        self.level_image = self.font.render(level_str, True,
                self.settings.text_color, None)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.padding
        self.level_rect.top = self.life_rect.bottom + (self.padding * 1.5)

    def _draw_lives(self) -> None:
        current_x = self.padding
        current_y = self.padding
        for _ in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def _draw_panel(self, rect, padding=10) -> None:
        panel_rect = pygame.Rect(
            rect.left - padding,
            rect.top - padding,
            rect.width + padding * 2,
            rect.height + padding * 2
        )
        pygame.draw.rect(self.screen, (0, 0, 0), panel_rect)

    def draw(self) -> None:
        left_panel_rect = pygame.Rect(
            self.padding, 
            self.padding,
            self.life_rect.width * self.game_stats.ships_left +
            self.padding * (self.game_stats.ships_left -1),
            self.level_rect.bottom - self.padding
        )
        self._draw_panel(left_panel_rect)

        right_panel_rect = pygame.Rect(
            min(self.max_score_rect.left, self.score_rect.left),
            self.max_score_rect.top,
            max(self.max_score_rect.width, self.score_rect.width),
            self.score_rect.bottom - self.max_score_rect.top
        )
        self._draw_panel(right_panel_rect)

        self._draw_panel(self.hi_score_rect)


        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()