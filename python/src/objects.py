#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:29:17 2019

@author: arynchoong
Game objects
"""
import random

SCREENWIDTH = 1024
STARTY = 20
MARGINX = 6
BOUNDY = 600
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

class Word:
    def __init__(self, word):
        self.text = word
        self.len = len(self.text)
        self.x = 0
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
    
    def check_gameover(self):
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


class Objects:
    def __init__(self, wordlist=None, font_size=16):
        if wordlist == None:
            self.wordlist = ['a','b','c','d','e','f','g','h','i','j','k',
                             'l','m','n','o','p','q','r','s','t','u','v',
                             'x','y','z']
            random.shuffle(self.wordlist)
        else:
            self.wordlist = wordlist
        self.max_x = SCREENWIDTH - MARGINX
        self.font_size = font_size
        self.game_words = []
        self.cityline = Cityline()
    
    def add_word(self):
        if not self.wordlist:
            return False
        
        # calculate list of city blocks available
        avail_block = []
        for idx, block in enumerate(self.cityline):
            if block.get_flag() == True:
                avail_block.append(idx)
        # remove blocks with words already above
        if self.game_words:
            new_avail = avail_block.copy()
            for word in self.game_words:
                startidx = int((word.get_x()-(MARGINX))/10)
                endidx = startidx + int(len(word)/10)
                for idx in range(startidx,endidx+1):
                    if idx in new_avail:
                        new_avail.remove(idx)
            if new_avail:
                avail_block = new_avail
        
        word = Word(self.wordlist.pop(0))
        # calculate max x of word
        bound_x = self.max_x - (FONTWIDTH * len(word))
        if not avail_block:
            word.set_x(random.randint(MARGINX*2,bound_x))
        else:
            # randomly select block
            idx = random.choice(avail_block)
            # calculate start x of word
            if ((idx*10)+MARGINX) > bound_x:
                word.set_x(bound_x)
            else:
                word.set_x((idx*10)+MARGINX)
        self.game_words.append(word)
        return True
    
    def move(self, delta):
        # move all game words downwards
        if not self.game_words:
            return
        for word in self.game_words:
            word.move(delta)
            if word.get_y() >= BOUNDY:
                word.set_remove()
                self.cityline.del_blocks(word.get_x(),len(word))
        self.cleanup()
        return
    
    def isEmpty(self):
        if self.wordlist:
            return False
        if self.game_words:
            return False
        return True
    
    def cleanup(self):
        if not self.game_words:
            return
        # remove words from game_words with word.typedidx == -2
        self.game_words = [w for w in self.game_words if w.typedidx != -2]
        
    def is_gameover(self):
        return self.cityline.check_gameover()
    
