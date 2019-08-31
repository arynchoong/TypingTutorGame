#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug 21 2019

@author: arynchoong
"""

import pygame
from pygame.locals import *

# Resource folder. Words list
RESFOLDER = '../../res/'

#               R    G    B
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
SHADOWGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 128)


class TypingTutor:
    def __init__(self):
        """
        Initialise game variables
        """
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400

    def on_init(self):
        """
        Initialise pygame
        """
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
        self.font = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 16)
        self.bigfont = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 32)
        pygame.display.set_caption('Typing Tutorial Game')
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        
    def on_loop(self):
        """
        Game play
        """
        pass
    
    def text_objs(self, text, font, color):
        """
        Create and return font's surface and rectangle
        """
        surf = font.render(text, True, color)
        return surf, surf.get_rect()
    
    def on_render(self):
        """
        Render main screen
        """
        # start screen / score screen
        self._display_surf.fill(BLACK)
        text = 'Typing Tutor Game'
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
        return
        
    def on_cleanup(self):
        """
        Quit pygame
        """
        pygame.quit()
 
    def on_execute(self):
        """
        Excecute game loop
        """
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    typing_tutor = TypingTutor()
    typing_tutor.on_execute()
