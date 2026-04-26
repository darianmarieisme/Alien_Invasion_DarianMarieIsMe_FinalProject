'''
Final Project: Alien Invasion (Milestone 2)
Darian Marie Bruce
04/23/2026
this module defines the alien class'''

import pygame
import random
from settings import Settings
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    '''Represents the alien that fills out a fleet flying towards the left of the screen'''
    def __init__(self, fleet: 'AlienFleet', x: float, y: float) -> None:
        '''Initializes the variables to be used by the alien sprite'''
        super().__init__()
        self.fleet: AlienFleet = fleet
        self.screen: pygame.Surface = fleet.game.screen
        self.boundaries: pygame.Rect = fleet.game.screen.get_rect()
        self.settings: Settings = fleet.game.settings

        self.image: pygame.Surface = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.alien_w, self.settings.alien_h)
            )
        self.image = pygame.transform.rotate(self.image, -90)

        tint = random.choice([
            (255, 100, 100),
            (100, 255, 100),
            (100, 100, 255),
            (255, 150, 255),
        ])

        tint_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        tint_surface.fill((*tint, 255))

        self.image.blit(tint_surface, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

        
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.drift_direction: int = random.choice([-1, 1])

        self.y: float = float(self.rect.y)
        self.x: float = float(self.rect.x)

        self.speed: float = self.settings.fleet_speed * random.uniform(0.8, 1.3)

    def update(self) -> None:
        '''Updates the alien's position as it moves across the screen'''
        self.y += 0.2 * self.drift_direction
        self.rect.y = self.y
        if self.rect.top <= 0:
            self.drift_direction = 1
        elif self.rect.bottom >= self.boundaries.bottom:
            self.drift_direction = -1

        self.x -= self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def is_off_screen(self) -> bool:
        '''This method determines if an alien has reached the left border, if so, will return true'''
        return self.rect.left <= 0

    def draw_alien(self) -> None:
        '''draws the alien on the screen'''
        self.screen.blit(self.image, self.rect)