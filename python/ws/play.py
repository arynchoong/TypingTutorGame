# play.py
import pygame
from objects import GameObjects

# Colours        R    G    B
BLUE        = (  0,   0, 128)
WHITE       = (255, 255, 255)
GREEN       = (  0, 200,   0)
BLACK       = (  0,   0,   0)
YELLOW      = (255, 255,   0)
LIGHTBLUE   = (135, 206, 235)
# Dimensions
MARGINX = 5
# Resources
RESFOLDER = '../../res/'
# Sound types
SOUND_KEYHIT = 1
SOUND_ERROR = 2
SOUND_SUCCESS = 3
SOUND_CRASH = 4

class GamePlay():
    def __init__(self, screen, sound=False):
        '''
        # TODO: Initialise pygame libraries
        # Member objects:-
        self.screen
        self.disp_surf
        self.width
        self.height
        self.font
        self.playing
        self.game_objects
        self.last_add
        self.add_timeout
        self.fps
        self.fps_clock
        self.y_delta
        self.typing_flag
        self.score
        self.key_hit
        self.level
        self.typed_count
        # TODO: initialise sound effect
        '''
        pass
        
    def execute(self):
        '''Start a game'''
        pass
    
    def check_events(self):
        '''Check events for game play'''
        pass
    
    def loop(self):
        '''Game loop'''
        pass
        
    def render(self):
        '''Render surface'''
        pass

    def draw_word(self, text, colour, coord):
        '''Display some text'''
        pass
        
    def add_word(self):
        '''Add new word to drop from top'''
        pass
    
    def check_key_hit(self):
        '''Check user's typed key'''
        pass
    
    def add_score(self, score):
        '''Adds score when user successfully complete typing word.'''
        pass

    def draw_score(self):
        '''Draw status bar'''
        pass
    
    def init_sound(self):
        '''Ready sound files'''
        pass
    
    def play_sound(self, type):
        '''Play indicated sound'''
        pass
            
        