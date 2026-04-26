'''
Final Project: Alien Invasion (Milestone 2)
Darian Marie Bruce
04/23/2026
This is the settings used across the project'''

from pathlib import Path

class Settings:
    '''Stores all configuration values for the game'''
    
    def __init__(self):
        '''initializes all game settings'''

        # general

        self.name: str = "Alien Invasion"
        self.screen_w: int = 1200
        self.screen_h: int = 800
        self.FPS: int = 60
        self.bg_file: Path = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'

        # Ship

        self.ship_file: Path = Path.cwd() / 'Assets' / 'images' / 'ship2.png'
        self.ship_w: int = 40
        self.ship_h: int = 60

        # Lives

        self.heart_file: Path = Path.cwd() / 'Assets' / 'images' / 'heart.png'
        self.heart_w: int = 40
        self.heart_h: int = 60

        # Bullet

        self.bullet_file: Path = Path.cwd() / 'Assets' / 'images' / 'laserBlastedit.png'
        self.laser_sound: Path = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3'
        self.impact_sound: Path = Path.cwd() / 'Assets' / 'sound' / 'ImpactSound.mp3'


        # Alien

        self.alien_file: Path = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w: int = 40
        self.alien_h: int = 40
        self.fleet_direction: int = 1

        # Button

        self.button_w: int = 200
        self.button_h: int = 50
        self.button_color: tuple[int, int, int] = (255, 51, 122)

        # Text

        self.text_color: tuple[int, int, int] = (255, 255, 255)
        self.button_font_size: int = 48
        self.hud_font_size: int = 20
        self.font_file: Path = Path.cwd() / 'Assets' / 'fonts' / 'Silkscreen' / 'Silkscreen-Bold.ttf'

    def initialize_dynamic_settings(self) -> None:
        '''This method initializes settings that will change through gameplay
        '''
        self.ship_speed: int = 5
        self.starting_ship_count: int = 3

        self.bullet_w: int = 25
        self.bullet_h: int = 80
        self.bullet_speed: int = 9
        self.bullet_amount: int = 15
            
        self.fleet_speed: float = 0.7
        self.alien_points: int = 50

    def increase_difficulty(self) -> None:
        '''This method handles the difficulty that will change with each level increase'''
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale
