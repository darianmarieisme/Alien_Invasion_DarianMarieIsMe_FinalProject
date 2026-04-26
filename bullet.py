'''
Final Project: Alien Invasion (Milestone 3)
Darian Marie Bruce
04/26/2026
this module defines the bullet class'''

import pygame
from settings import Settings
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    '''Represents a projectile fired by the ship that moves across the screen'''
    def __init__(self, game: 'AlienInvasion') -> None:
        '''Initializes the bullet, sets its starting position and loads its image, 
        positioning on left side of screen'''
        super().__init__()

        self.game = game

        self.screen: AlienInvasion = game.screen
        self.settings: Settings = game.settings

        self.image: pygame.Surface = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.bullet_h, self.settings.bullet_w)
            )
        

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.midleft = game.ship.rect.midright
        self.x: float = float(self.rect.x)

    def update(self):
        '''Updates the bullets position as it moves across the screen towards the right'''
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self) -> None:
        '''draws the bullet on the screen'''

        for i in range(1,4):
            trail = self.image.copy()
            trail.set_alpha(150-i *40)

            self.screen.blit(trail, (self.rect.x - i * 10, self.rect.y))
            
        self.screen.blit(self.image, (self.rect.x - 2, self.rect.y))
        self.screen.blit(self.image, (self.rect.x + 2, self.rect.y))


        self.screen.blit(self.image, self.rect)