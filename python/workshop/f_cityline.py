#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug 21 2019

@author: arynchoong
"""

import pygame
from pygame.locals import *
import random

# Resource folder. Words list
RESFOLDER = '../../res/'

#               R    G    B
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
SHADOWGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 128)

# Game States
START = 1
PLAYING = 2
GAMEOVER = 3

FONTSIZE = 16
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

SCREENWIDTH = 640
STARTY = 20
MARGINX = 6
BOUNDY = 360
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

class Word:
    def __init__(self, word, x = MARGINX):
        self.text = word
        self.len = len(self.text)
        self.x = x
        self.y = 6
        self.typedidx = -1
        self.surf = None
        self.rect = None
    
    def get_x(self):
        return self.x
    def set_x(self, x):
        self.x = x
        return
    def get_y(self):
        return self.y
    def __len__(self):
        return self.len
    def move(self, delta):
        self.y += delta
        return self.y
    def typed(self):
        self.typedidx += 1
        if (self.typedidx >= (self.len-1)):
            # completed typing word
            self.typedidx = -2
            return False
        return True
    def typed_reset(self):
        self.typedidx = -1
        return
    def set_remove(self):
        self.typedidx = -2
        return
    def set_display(self, surf, rect):
        self.surf = surf
        self.rect = rect
        return
    def get_surf(self):
        return self.surf
    def get_rect(self):
        return self.rect


class Block:
    def __init__(self, flag=True, height = 0):
        self.flag = flag
        self.height = height
        return
    def set_flag(self, flag):
        self.flag = flag
        return
    def get_flag(self):
        return self.flag
    def set_height(self, height):
        self.height = height
        return
    def get_height(self):
        return self.height
    
class Cityline:
    def __init__(self):
        self.len = int((SCREENWIDTH-MARGINX*2)/10)
        # Create cityline
        self.cityline = []
        # with 10 px blocks, randomize building height
        for i in range(self.len):
            # each block is (flag,height) 
            self.cityline.append(Block(True, random.randint(1,20)))
        # n blocks require n+1 coordinates. last block redundant
        self.cityline[-1].set_flag(False) 
        return
    
    def __iter__(self):
        return CityIterator(self.cityline)
    
    def __len__(self):
        return self.len
    
    def reset(self):
        for block in self.cityline:
            block.set_flag(True)
        self.cityline[-1].set_flag(False) 
    
    def check_gameover(self):
        if not self.cityline:
            print(self.cityline)
            return False
        if all(block.get_flag() == False for block in self.cityline):
            return True
        return False
    
    def del_blocks(self, startx, strlen):
        startidx = int((startx-MARGINX) / 10)
        endidx = (startidx + int((FONTWIDTH * strlen) / 10))
        if endidx >= self.len:
            endidx = self.len-1
        for i in range(startidx, endidx+1):
            self.cityline[i].set_flag(False)
        return
    
    def get_block(self, index):
        return self.cityline[index]
    
class CityIterator:
    def __init__(self, city):
        self.city = city
        self.index = 0
    
    def __next__(self):
        try:
            block = self.city[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return block
    
    def __iter__(self):
        return self


class TypingTutor:
    def __init__(self):
        """
        Initialise game variables
        """
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.state = START
        self.fps = 25
        self.fpsclock = pygame.time.Clock()
        self.wordlist = self.init_words()
        self.gamewords = []
        self.keyhit = None
        self.typingflag = False
        self.cityline = Cityline()

    def init_words(self):
        with open(RESFOLDER + "brown.txt", "r", newline='') as file:
            words_list = [line.strip() for line in file.readlines()]
        size = len(words_list)
        return words_list
    
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
        
    def check_events(self):
        """
        Loops through and handle events
        returns last event key
        """
        ret = None
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
            if event.type == TEXTINPUT:
                self.keyhit = event.text
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if self.state == PLAYING:
                        self.state = GAMEOVER
                    else:
                        self._running = False
                elif self.state != PLAYING:
                    self.state = PLAYING
                ret = event.key
        return ret
        
    def game_event(self, event):
        if event.type == QUIT:
            self._running = False
            self.state = GAMEOVER
        elif event.type == TEXTINPUT:
            self.keyhit = event.text
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.state = GAMEOVER
                
    def on_loop(self):
        """
        Game play
        """
        if (self.state != PLAYING):
            return
        # start game
        self.score = 0
        self.fps = 25
        self.ydelta = 1
        self.add_timeout = 2000
        self.game_words = []
        self.last_add = 0
        self.cityline.reset()
        while(self.state == PLAYING):
            if (not self.game_words) or \
              ((pygame.time.get_ticks() - self.last_add) > self.add_timeout):
                if self.add_word():
                    self.last_add = pygame.time.get_ticks()
            # check and handle game event
            for event in pygame.event.get():
                self.game_event(event)
                self.check_keyhit()
            self.game_render()
            self.fpsclock.tick(self.fps)
            # check cityline
            if self.is_gameover():
                self.state = GAMEOVER
            self.move(self.ydelta)
        return
    
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
        if self.state == START:
            text = 'Typing Tutor Game'
        elif self.state == GAMEOVER:
            text = 'Game Over'
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
            self.check_events()
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    
    def add_word(self):
        """
        randomly select word
        check first letter not matching in game words
        """
        word = random.choice(self.wordlist)
        firstchar = [word.text[0] for word in self.game_words]
        while (word[0] in firstchar):
            word = random.choice(self.wordlist)
        # calculate max x of word
        max_x = (SCREENWIDTH - MARGINX) - (FONTWIDTH * len(word))
        x = random.randint(MARGINX,max_x)
        self.game_words.append(Word(word, x))
        return True
    
    def move(self, delta):
        # move all game words downwards
        if not self.game_words:
            return
        for word in self.game_words:
            word.move(delta)
            if word.get_y() >= BOUNDY:
                if word.typedidx > -1:
                    self.typingflag = False 
                word.set_remove()
                self.cityline.del_blocks(word.get_x(),len(word))
        self.cleanup()
        return
    
    def cleanup(self):
        """
        Remove words that have hit the bottom
        """
        if not self.game_words:
            return
        # remove words from game_words with word.typedidx == -2
        self.game_words = [w for w in self.game_words if w.typedidx != -2]
        # Check typing flag:
        if self.typingflag:
            if not self.game_words:
                self.typingflag = False
                return
            if all(w.typedidx < 0 for w in self.game_words):
                self.typingflag = False
        return
    
    def game_render(self):
        """
        Render display during game play
        """
        self._display_surf.fill(BLUE)
        # RENDER WORDS
        del_list = []
        for word in self.game_words:
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
        for i in range(1, len(self.cityline)):
            if (self.cityline.get_block(i).get_flag()==False):
                continue
            startx = ((i-1)*10) + MARGINX*2
            starty = BOUNDY + 12 + self.cityline.get_block(i-1).get_height()
            endx = (i*10) + MARGINX*2
            endy = BOUNDY + 12 + self.cityline.get_block(i).get_height()
            pygame.draw.lines(self._display_surf, GREEN, False,
                             [(startx,starty), (startx,endy), (endx,endy)],
                             2)
        # Update display
        pygame.display.flip()
        return
    
    def check_keyhit(self):
        if not self.keyhit:
            return
        if(self.typingflag):
            for word in self.game_words:
                if word.typedidx != -1:
                    if word.text[word.typedidx+1] == self.keyhit:
                        if (word.typed() == False):
                            self.typingflag = False
                            self.score += len(word)
                    else:
                        word.typed_reset()
                        self.typingflag = False
        else:
            for word in self.game_words:
                if word.text[0] == self.keyhit:
                    if(word.typed() != False):
                        self.typingflag = True
                    else:
                        self.score += 1
                    break
        self.cleanup()
        self.keyhit = None
        return
    
    def is_gameover(self):
        return self.cityline.check_gameover()


if __name__ == "__main__":
    typing_tutor = TypingTutor()
    typing_tutor.on_execute()
