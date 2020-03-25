# game objects.py
import string
import random
from word import Word
from city import CityLine

# Dimensions
MARGINX = 5
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size
# Resources
RESFOLDER = '../../res/'

class GameObjects:
    def __init__(self, screen_width, screen_height):
        ''' Member objects
        self.screen_width
        self.screen_height
        self.word_list
        self.game_words
        self.bound_y
        self.city_line
        '''
        pass

    def init_words(self):
        '''Prepare list of words for the game'''
        pass
    
    def add_word(self, level):
        '''Add word to game play'''
        pass
    
    def get_word(self, level):
        '''Randomly select word from word list for game play'''
        pass

    def move(self, delta):
        '''Returns Flags if word is removed and if it is in the middle of typing,
        when it has moved beyond boundary Y
        '''
        pass
    
    def clean_up (self):
        '''Check and remove any word in game that is flagged to be removed.'''
        pass
    
    def is_gameover(self):
        '''Check with game object if game over'''
        pass