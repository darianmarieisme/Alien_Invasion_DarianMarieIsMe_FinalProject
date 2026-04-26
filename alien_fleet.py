'''
Final Project: Alien Invasion (Milestone 2)
Darian Marie Bruce
04/23/2026
this module defines the alien fleet class
'''

import pygame
import random
from settings import Settings
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    '''Represents the fleet flying towards the player ship'''
    def __init__(self, game: 'AlienInvasion') -> None:
        '''This clas initializes variables that will prepare the fleet
        '''
        self.game: AlienInvasion = game
        self.settings: Settings = game.settings
        self.fleet: pygame.sprite.Group = pygame.sprite.Group()
        

        self.create_fleet()

    def create_fleet(self):
        '''This method determines the fleet size based on the alien and screen size
        '''
        alien_w: int = self.settings.alien_w
        alien_h: int = self.settings.alien_h
        screen_w: int = self.settings.screen_w
        screen_h: int = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)

        x_offset: int = self.calculate_offsets(screen_w)


        self._create_rectangle_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset) -> None:
        '''This method takes the alien width, height, fleet width and height, then x offset
        to create an alien fleet
        '''
        max_cols: int = 8
        padding: int = 50
        spacing: int = alien_h * 2

        for row in range(fleet_h):
            for col in range(min(fleet_w, max_cols)):
                current_x: int = x_offset - alien_w * col
                current_y: int = padding + row * spacing

                if col % 2 == 0 or random.random() < 0.2:
                    continue

                self._create_alien(current_x, current_y)

    def calculate_offsets(self, screen_w) -> int:
        '''This method calculates offsets that will be used when designing the alien fleet.
        It takes screen_w and saves it into a new variable
        '''
        x_offset: int = screen_w
        return x_offset

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h) -> int:
        '''this method calculates the size of the fleet based on the screen and alien size,
        returning how wide and high the fleet will be in integer'''
        fleet_w = (screen_w//alien_w)
        fleet_h = ((screen_h /2)//alien_h)
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2

        if fleet_h  % 2 == 0:
            fleet_h -=1
        else:
            fleet_h -= 2

        return int(fleet_w), int(fleet_h)
    
    def _create_alien(self, current_x: int, current_y: int) -> None:
        '''This method creates a new alien from the parameters passed and adds it to
        the fleet'''
        new_alien: Alien = Alien(self, current_x, current_y)

        self.fleet.add(new_alien)

    def update_fleet(self) -> None:
        '''Updates the position and behavior of the aliens in the fleet
        '''
        self.fleet.update()

    def draw(self) -> None:
        '''Draws the aliens in the feel
        '''
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group) -> dict[pygame.sprite.Sprite, list[pygame.sprite.Sprite]]:
        '''Checks for collisions between the fleet and another sprite group,
        removing those collided sprites'''
        return pygame.sprite.groupcollide(other_group, self.fleet, True, True)
    
    def check_fleet_bottom(self) -> bool:
        '''Returns True if any alien in the fleet reaches the left edge of the screen
        '''
        alien: Alien
        if not self.fleet:
            return False

        leftmost = min(self.fleet, key=lambda alien: alien.rect.left)
        return leftmost.rect.left <= 0
        
    def check_destroyed_status(self) -> bool:
        '''Returns True if all aliens in the flet have been destroyed.'''
        return not self.fleet