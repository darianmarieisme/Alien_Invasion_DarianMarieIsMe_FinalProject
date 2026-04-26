'''
Final Project: Alien Invasion (Milestone 2)
Darian Marie Bruce
04/26/2026
This module manages bullets'''

import pygame
from settings import Settings
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Arsenal:
    '''Manages all bullets fired by the ship'''
    def __init__(self, game: "AlienInvasion"):
        '''initializes the arsenal, linking it to the game and creating a group to store
        bullets'''
        self.game: AlienInvasion = game
        self.settings: Settings = game.settings
        self.arsenal: pygame.sprite.Group = pygame.sprite.Group()

    def update_arsenal(self) -> None:
        '''updates all bullets' positions and removes any that have moved offscreen'''
        self.arsenal.update()
        self._remove_bullets_offscreen()
        
    def _remove_bullets_offscreen(self) -> None:
        '''removes bullets that have left the visible screen to free up space
        for new bullets, checking position of bullet to right barrier of screen'''
        for bullet in self.arsenal.copy():
            if bullet.rect.right >= self.game.settings.screen_w:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        '''Draws any active bullets onto the screen'''
        for bullet in self.arsenal:
            bullet.draw_bullet()

    def fire_bullet(self) -> bool:
        '''Creates and adds a new bullet if under the limit of on screen bullets
        returns: true or false based on condition of on screen bullets'''
        if len(self.arsenal) < self.settings.bullet_amount:
            center: Bullet = Bullet(self.game)
            top: Bullet = Bullet(self.game)
            bottom: Bullet = Bullet(self.game)

            top.rect.y -= 50
            bottom.rect.y += 50

            self.arsenal.add(center, top, bottom)
            return True
        
        return False