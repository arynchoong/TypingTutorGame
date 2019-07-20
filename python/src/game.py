#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:29:17 2019

@author: arynchoong
"""

import pygame, sys
from pygame.locals import *
import math

#               R    G    B
WHITE       = (255, 255, 255)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
BLUE        = (  0,   0, 155)

RESFOLDER = '../../res/'

class TypingTutor:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1024, 640
        self.fps = 25
        self.fpsclock = pygame.time.Clock()
        self.levels = 30 # number of levels in the game
        self.wordlist, self.levelwordcount = self.init_words()
        self.font = None
        self.bigfont = None
        self.keyhit = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.font = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 16)
        self.bigfont = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 32)
        pygame.display.set_caption('Typing Tutorial Game')
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type >= pygame.K_HASH and event.type <= pygame.K_z:
            self.keyhit = event.type
    
    def on_loop(self):
        self.run_game()
    
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    
    def init_words(self):
        with open(RESFOLDER + "brown.txt", "r", newline='') as file:
            words_list = [line.strip() for line in file.readlines()]
        size = len(words_list)
        blocksize = math.ceil(size/self.levels)
        multiplier = 10**(len(str(blocksize)) -1)
        levelwordcount = math.floor(blocksize/multiplier)*multiplier
        return words_list, levelwordcount
    
    def get_level_words(self, level):
        return self.wordlist[(self.levelwordcount * level):]
    
    def run_game(self):
        level = 1
        levelwords = self.get_level_words(level)
        return


if __name__ == "__main__":
    typing_tutor = TypingTutor()
    typing_tutor.on_execute()
