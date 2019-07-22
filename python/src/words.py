#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 22:29:17 2019

@author: arynchoong
Game objects
"""
import random

STARTY = 20
MARGINX = 6
BOUNDY = 600

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
    def move(self, delta):
        self.y += delta
        return self.y
    def typed(self):
        if (self.typedidx >= self.len):
            return False
        else:
            self.typedidx += 1
            return True
    def set_display(self, surf, rect):
        self.surf = surf
        self.rect = rect
        return
    def get_surf(self):
        return self.surf
    def get_rect(self):
        return self.rect

class Words:
    def __init__(self, wordlist=None, max_x=1000, font_size=16):
        if wordlist == None:
            self.wordlist = ['a','b','c','d','e','f','g','h','i','j','k','l',
                             'm','n','o','p','q','r','s','t','u','v','x','y',
                             'z']
            random.shuffle(self.wordlist)
        else:
            self.wordlist = wordlist
        self.max_x = max_x
        self.font_size = font_size
        self.game_words = []
    
    def add_word(self):
        if not self.wordlist:
            return False
        else:
            word = Word(self.wordlist.pop(0))
            # randomize start x of word
            bound_x = self.max_x - (self.font_size * word.len)
            word.set_x(random.randint(MARGINX,bound_x))
            self.game_words.append(word)
            return True
    
    def move(self):
        if not self.game_words:
            return
        for word in self.game_words:
            word.move(1)
        return
    
    def isEmpty(self):
        if self.wordlist:
            return False
        if self.game_words:
            return False
        return True
