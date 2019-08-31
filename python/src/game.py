#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:29:17 2019

@author: arynchoong
"""

import pygame, sys
from pygame.locals import *
import math
import random
from objects import *

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 255,   0)
SHADOWGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 128)

RESFOLDER = '../../res/'

# Game States
START = 1
PLAYING = 2
SCORE = 3
GAMEOVER = 4

FONTSIZE = 16
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

class TypingTutor:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 1024, 640
        self.fps = 25
        self.fpsclock = pygame.time.Clock()
        self.add_timeout = 2000 # start with 2 seconds
        self.ydelta = 1
        self.game_object = None
        self.wordlist = self.init_words()
        self.levelwordcount = 1000
        self.levelwords = None
        self.font = None
        self.bigfont = None
        self.keyhit = None
        self.typingflag = False
        self.state = START
        self.level = 1
        self.score = 0
        self.high_score = 0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.font = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 16)
        self.bigfont = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 32)
        pygame.display.set_caption('Typing Tutorial Game')
        self._running = True
 
    def check_events(self):
        # returns last event key
        ret = None
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._running = False
                    self.state = GAMEOVER
                else:
                    self.state = PLAYING
                ret = event.key
        return ret
    
    def on_loop(self):
        if (self.state == PLAYING):
            # start game
            self.run_game()
        return
    
    def render_screen(self, score=0):
        # start screen / score screen
        self._display_surf.fill(BLACK)
        if self.state == START:
            text = 'Typing Tutorial Game'
        elif self.state == GAMEOVER:
            text = 'Game Over'
        elif self.state == SCORE:
            self.draw_status()
            text = 'Score: ' + str(self.score)
        else:
            text = 'Playing'
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
        
        if self.state == GAMEOVER:
            text = 'Score: ' + str(self.score)
            # Draw score
            titleSurf, titleRect = self.text_objs(text, self.bigfont, GREEN)
            titleRect.center = (int(self.width / 2), int(self.height / 2) - 100)
            self._display_surf.blit(titleSurf, titleRect)
    
        # Draw the additional "Press a key to play." text.
        pressKeySurf, pressKeyRect = self.text_objs('Press a key to play.', self.font, WHITE)
        pressKeyRect.center = (int(self.width / 2), int(self.height / 2) + 100)
        self._display_surf.blit(pressKeySurf, pressKeyRect)
        
        while self.check_events() == None:
            pygame.display.flip()
            self.fpsclock.tick()
        return
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            self.on_loop()
            self.render_screen()
        self.on_cleanup()
    
    def init_words(self):
        with open(RESFOLDER + "brown.txt", "r", newline='') as file:
            words_list = [line.strip() for line in file.readlines()]
        size = len(words_list)
        #blocksize = math.ceil(size/self.levels)
        #multiplier = 10**(len(str(blocksize)) -1)
        #levelwordcount = math.floor(blocksize/multiplier)*multiplier
        return words_list
    
    def set_level_words(self, level):
        if(20+(5*level) >= len(self.wordlist)):
            self.levelwords = self.wordlist.copy()
        else:
            if len(self.wordlist) > (100+(self.levelwordcount * (level-1))):
                words = self.wordlist[:(100+(self.levelwordcount * (level-1)))]
            else:
                words = self.wordlist
            # Randomly select, makesure there is no duplicate first char
            self.levelwords = []
            firstchar = []
            i = 0
            num_words = (20+(5*level))
            while (i < num_words):
                word = random.choice(words)
                if not (word[0] in firstchar):
                    firstchar.append(word[0])
                    self.levelwords.append(word)
                    i+=1
                if len(firstchar)>20:
                    firstchar = firstchar[-15:]
        return
    
    def text_objs(self, text, font, color):
        surf = font.render(text, True, color)
        return surf, surf.get_rect()
        
    def run_game(self):
        self.level = 1
        self.score = 0
        self.fps = 25
        self.ydelta = 1
        self.add_timeout = 2000
        while(self.state != GAMEOVER):
            self.set_level_words(self.level)
            self.game_object = Objects(self.levelwords)
            self.keyhit = None
            while (self.state == PLAYING):
                for event in pygame.event.get():
                    self.game_event(event)
                    self.check_keyhit()
                self.game_loop()
                self.game_render()
                self.fpsclock.tick(self.fps)
            # add delay and clear event queue from game
            pygame.time.wait(500)
            pygame.event.clear()
            while (self.state == SCORE):
                self.render_screen()
        return
    
    def game_loop(self):
        # cityline
        if self.game_object.is_gameover():
            self.state = GAMEOVER
            return
        # words
        self.game_object.move(self.ydelta)
        
        if self.game_object.isEmpty():
            # level up
            self.level += 1
            self.state = SCORE
            if self.fps < 60:
                self.fps += 25
            elif self.ydelta < 3:
                self.ydelta +=1
            if self.add_timeout > 900:
                self.add_timeout -= 150
        else:
            self.game_add_word()
            if self.typingflag:
                if all(w.typedidx < 0 for w in self.game_object.game_words):
                    self.typingflag = False
        return
    
    def game_add_word(self):
        if not self.game_object.game_words or \
           ((pygame.time.get_ticks() - self.last_add) > self.add_timeout):
            if self.game_object.add_word():
                self.last_add = pygame.time.get_ticks()
        return
    
    def game_render(self):
        self._display_surf.fill(BLUE)
        self.draw_status()
        
        # RENDER WORDS
        del_list = []
        for word in self.game_object.game_words:
            if(word.typedidx > -1):
                # typed
                wordSurf, wordRect = self.text_objs(
                                        word.text[:word.typedidx+1],
                                        self.font, RED)
                wordRect.topleft = (word.x, word.y)
                self._display_surf.blit(wordSurf, wordRect)
                # untyped
                text = ' '*(word.typedidx+1) + word.text[word.typedidx+1:]
                wordSurf, wordRect = self.text_objs(text, self.font, 
                                                    GREEN)
                wordRect.topleft = (word.x, word.y)
                self._display_surf.blit(wordSurf, wordRect)
            else:
                wordSurf, wordRect = self.text_objs(word.text, self.font, 
                                                    GREEN)
                wordRect.topleft = (word.x, word.y)
                self._display_surf.blit(wordSurf, wordRect)
        
        # RENDER CITYLINE
        for i in range(1, len(self.game_object.cityline)):
            if (self.game_object.cityline.get_block(i).get_flag()==False):
                continue
            startx = ((i-1)*10) + MARGINX*2
            starty = 612 + self.game_object.cityline.get_block(i-1).get_height()
            endx = (i*10) + MARGINX*2
            endy = 612 + self.game_object.cityline.get_block(i).get_height()
            pygame.draw.lines(self._display_surf, GREEN, False,
                             [(startx,starty), (startx,endy), (endx,endy)],
                             2)
        
        # Update display
        pygame.display.flip()
        return
    
    def draw_status(self):
        # draw the score text
        scoreSurf = self.font.render('Score: %s' % self.score, True,
                                     WHITE, BLACK)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.width -150, 2)
        self._display_surf.blit(scoreSurf, scoreRect)
    
        # draw the level text
        levelSurf = self.font.render('Level: %s' % self.level, True, 
                                     WHITE, BLACK)
        levelRect = levelSurf.get_rect()
        levelRect.topleft = (MARGINX, 2)
        self._display_surf.blit(levelSurf, levelRect)
        return
    
    def game_event(self, event):
        if event.type == QUIT:
            self._running = False
            self.state = GAMEOVER
        elif event.type == TEXTINPUT:
            self.keyhit = event.text
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.state = GAMEOVER

    def check_keyhit(self):
        if not self.keyhit:
            return
        if(self.typingflag):
            for word in self.game_object.game_words:
                if word.typedidx != -1:
                    if word.text[word.typedidx+1] == self.keyhit:
                        if (word.typed() == False):
                            self.typingflag = False
                            self.score += len(word)
                    else:
                        word.typed_reset()
                        self.typingflag = False
        else:
            for word in self.game_object.game_words:
                if word.text[0] == self.keyhit:
                    if(word.typed() != False):
                        self.typingflag = True
                    else:
                        self.score += 1
                    break
        self.game_object.cleanup()
        self.keyhit = None
        return


if __name__ == "__main__":
    typing_tutor = TypingTutor()
    typing_tutor.on_execute()
