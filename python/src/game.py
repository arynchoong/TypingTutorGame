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
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 255,   0)
SHADOWGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)

RESFOLDER = '../../res/'

# Game States
START = 1
PLAYING = 2
SCORE = 3
GAMEOVER = 4

class TypingTutor:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1024, 640
        self.fps = 25
        self.fpsclock = pygame.time.Clock()
        self.levels = 30 # number of levels in the game
        self.wordlist, self.levelwordcount = self.init_words()
        self.font = None
        self.bigfont = None
        self.keyhit = None
        self.state = START
        self.level = 1
        self.score = 0
        self.high_score = 0
        self.falling = None # active gameplay words 
        self.cityline = None # cityline sprite objects

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.font = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 16)
        self.bigfont = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 32)
        pygame.display.set_caption('Typing Tutorial Game')
        self._running = True
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            if event.key >= K_HASH and event.key <= K_z:
                self.keyhit = event.key
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                self._running = False
            else:
                self.state = PLAYING
    
    def on_loop(self):
        if self.keyhit == None:
            return
        # start game
        score = self.run_game()
        self.keyhit = None
        return score
    
    def on_render(self, score=0):
        # start screen / score screen
        self._display_surf.fill(BLACK)
        if self.state == START:
            text = 'Typing Tutorial Game'
        elif self.state == GAMEOVER:
            text = 'Game Over'
        else:
            text = 'Score'
        # This function displays large text in the
        # centerof the screen until a key is pressed.
        # Draw the text drop shadow
        titleSurf, titleRect = self.text_objs(text, self.bigfont, SHADOWGREEN)
        titleRect.center = (int(self.width / 2), int(self.height / 2))
        self._display_surf.blit(titleSurf, titleRect)
    
        # Draw the text
        titleSurf, titleRect = self.text_objs(text, self.bigfont, GREEN)
        titleRect.center = (int(self.width / 2)-1, int(self.height / 2)-1)
        self._display_surf.blit(titleSurf, titleRect)
    
        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = self.text_objs('Press a key to play.', self.font, WHITE)
        pressKeyRect.center = (int(self.width / 2), int(self.height / 2) + 100)
        self._display_surf.blit(pressKeySurf, pressKeyRect)
        
        pygame.display.flip()
        self.fpsclock.tick()
        return
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            score = self.on_loop()
            self.on_render(score)
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
    
    def text_objs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()
    
    def run_game(self):
        self.level = 1
        self.score = 0
        while(self.state != GAMEOVER):
            levelwords = self.get_level_words(level)
            words = random.sample(levelwords,k=20+(10*level))
            self.falling = None
            self.cityline = None # cityline sprite objects
            self.state = PLAYING
            while (self.state == PLAYING):
                self.game_loop()
                self.game_render()
            self.state = GAMEOVER
        return score
    
    def game_loop(self):
        pass
    
    def game_render(self):
        pass


if __name__ == "__main__":
    typing_tutor = TypingTutor()
    typing_tutor.on_execute()
