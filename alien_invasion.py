'''
Final Project: Alien Invasion (Milestone 2)
Darian Marie Bruce
04/23/2026
The purpose of this milestone is to modify the base
game to change the ship's orientation and movement'''

import sys
import pygame
from settings import Settings
from ship import Ship
from arsenal import Arsenal
from game_stats import GameStats
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:
    """Main class that manages game initialization, game loop, and overall behavior
    """
    def __init__ (self) -> None: 
        '''Initializes the game, creates the scene, loads assets,
        and sets up game objects'''
        pygame.init()
        self.settings: Settings = Settings()
        self.settings.initialize_dynamic_settings()


        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h))
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        pygame.display.set_caption(self.settings.name)

        self.bg: pygame.Surface  = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
            )

        self.running: bool  = True
        self.clock: pygame.time.Clock  = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound: pygame.mixer.Sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound: pygame.mixer.Sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.ship: Ship = Ship(self, Arsenal(self))
        self.alien_fleet: AlienFleet = AlienFleet(self)
        self.alien_fleet.create_fleet()

        self.play_button = Button(self, 'Play')
        self.game_active: bool = False

    def run_game(self) -> None:
        '''This method contains the main loop that runs the game logic'''

        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self) -> None:
       # check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()

            # subtract one life if possible
       # check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()

        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)

        #check collisions of projectiles and aliens
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            self.game_stats.update_level()
            self.HUD.update_level()

    def _check_game_status(self):
        if self.game_stats.ships_left  > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active: bool = False

    def _reset_level(self) -> None:
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
 

    def _update_screen(self) -> None:
        '''This method will redraw all game elements on the screen
        and update the display'''
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def restart_game(self) -> None:
       self.settings.initialize_dynamic_settings()
       self.game_stats.reset_stats()
       self.HUD.update_scores()
       self._reset_level()
       self.ship._center_ship()
       self.game_active = True
       pygame.mouse.set_visible(False)


    def _check_events(self) -> None:
        '''This method handles all user input events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos) and not self.game_active:
            self.restart_game()

    def _check_keyup_events(self, event) -> None:
        '''this method responds to key release events and stops ship
        movement'''
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _check_keydown_events(self, event) -> None:
        '''this method responds to key press events and updates ship
        movements and actions'''
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
           if self.ship.fire():
               self.laser_sound.play()
               self.laser_sound.fadeout(250)

        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    '''this is the main method that runs the logic from the game loop
    (run_game)'''
    ai = AlienInvasion()
    ai.run_game()
