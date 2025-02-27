# game.py
import pygame
from play import GamePlay
import sys

# Dimensions
WIDTH = 640
HEIGHT = 480
# States
START = 1
PLAYING = 2
GAMEOVER = 3
# Colours    R    G    B
BLACK   = (  0,   0,   0)
GREEN   = (  0, 255,   0)
# Resources
RESFOLDER = '../../res/'

class TypingTutor():
    def __init__(self, sound=False):
        '''
        # TODO: initialise Pygame libraries
        # Member objects
        self.screen
        self.disp_surf
        self.size 
        self.running 
        self.state 
        self.font 
        self.game
        self.sound
        '''
        pass
    
    def init_display(self):
        '''Helper function to initialise and return display surface'''
        pass

    def execute(self):
        '''Executes main event loop'''
        pass
        
    def check_events(self):
        '''Process events'''
        pass
    
    def render(self):
        '''Render surface'''
        pass
    
    def draw_text(self, text, colour, center):
        '''Draws text onto diplay surface'''
        pass

if __name__ == '__main__':
    '''Main entry point'''
    pass