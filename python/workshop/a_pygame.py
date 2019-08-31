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


class TypingTutor:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
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


if __name__ == "__main__":
    typing_tutor = TypingTutor()
    typing_tutor.on_execute()
