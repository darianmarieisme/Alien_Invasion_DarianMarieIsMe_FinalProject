'''
Final Project: Alien Invasion (Participation Activity)
Darian Marie Bruce
04/25/2026
This module deals with the level and scores of the game
'''

#volatile game stats
# from pathlib import Path
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    '''This module tracks game stats such as score, lives, and level
    it handles current score tracking, high score tracking,
    and resetting the game between sessions'''

    def __init__(self, game: 'AlienInvasion') -> None:
        '''This function initializes and sets all data for the game stats class
        '''
        self.game: AlienInvasion = game
        self.settings = game.settings
        self.max_score: int = 0
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self) -> None:
        '''loads the saved high score from a file or initializes it if
        it is not available
        '''
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat().st_size > 0:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score: int = 0
            self.save_scores()
            # save the file

    def save_scores(self) -> None:
        '''saves any current high score to a file'''
        scores: dict[str, int] = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)

        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f"File Not Found: {e}")

    def reset_stats(self) -> None:
        '''this resets dynamic game statistics for a new game session
        '''
        self.ships_left = self.settings.starting_ship_count
        self.score: int = 0
        self.level: int = 1

    def update(self, collisions: dict[object, list[object]]) -> None:
        '''This updates score related statistics based on collisions
        Arguments: collisions(dict): mapping of collided sprites returned by
        pygame.sprite.groupcollide()'''
        #update score
        self._update_score(collisions)
        
        #update score
        self._update_max_score()
        self._update_hi_score()

    def _update_max_score(self) -> None:
        '''This updates the maximum score in the current session'''
        if self.score > self.max_score:
            self.max_score = self.score
            self.save_scores()

      #  print(f'Max: {self.max_score}')

    def _update_hi_score(self) -> None:
        '''This updates the all time high score if the current
        score exceeds it'''
        if self.score > self.hi_score:
            self.hi_score = self.score

       # print(f'Hi: {self.max_score}')


    def _update_score(self, collisions: dict[object, list[object]]) -> None:
        '''increases the score based on each alien destroyed
        arguments: collsions (dict): mapping of collsions between bullets
        and aliens
        '''
        for alien in collisions.values():
            self.score += self.settings.alien_points
        # print(f'Basic: {self.score}')

    def update_level(self) -> None:
        '''increases the current game level'''
        self.level += 1
        # print(self.level)