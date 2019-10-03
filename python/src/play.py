# game play

import pygame
from pygame.locals import *
from objects import Objects

#               R    G    B
BLUE        = (  0,   0, 128)
LIGHTBLUE   = (135, 206, 235)
WHITE       = (255, 255, 255)
GREEN       = (  0, 200,   0)
BLACK       = (  0,   0,   0)
YELLOW      = (255, 255,   0)
# Game States
PLAYING = 2
GAMEOVER = 3
SCORE = 4

MARGINX = 5 # for cityline
RESFOLDER = '../../res/'

class GamePlay():
    def __init__(self, display_surf):
        self._display_surf = display_surf
        self.width = self._display_surf.get_width()
        self.height = self._display_surf.get_height()
        self.game_objects = None
        self.last_add = 0
        self.add_timeout = 2000 # start with 2 seconds
        self.state = PLAYING
        self.font = pygame.font.Font(RESFOLDER+'Consolas Bold.ttf', 16)
        self.fps = 25
        self.fpsclock = pygame.time.Clock()
        self.ydelta = 1
        self.keyhit = None
        self.typingflag = False
        self.score = 0
        self.level = 1
        self.typed_count = 0
        
    def on_init(self):
        self.game_objects = Objects(self.width, self.height)
    
    def on_execute(self):
        self.on_init()
        while (self.state == PLAYING):
            self.on_loop()
            self.on_render()
            self.on_check_event()
            self.check_keyhit()
            self.fpsclock.tick(self.fps)
        pygame.event.clear()
        return self.score if self.state else -1
    
    def on_loop(self):
        if self.typed_count >= 4:
            self.level += 1
            self.typed_count = 0
            if self.fps < 70:
                self.fps += 5
            elif self.ydelta < 5:
                self.ydelta +=1
            elif self.add_timeout > 900:
                self.add_timeout -= 150
        if self.game_objects.cityline.check_gameover():
            self.state = GAMEOVER
            return
        if self.game_objects.move(self.ydelta):
            self.typingflag = False
        self.add_word()
    
    def add_word(self):
        if not self.game_objects.game_words or \
            ((pygame.time.get_ticks() - self.last_add) > self.add_timeout):
            if self.game_objects.add_word(self.level):
                self.last_add = pygame.time.get_ticks()
        return
    
    def on_check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.state = False
            elif event.type == TEXTINPUT:
                self.keyhit = event.text
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self.state = GAMEOVER
        return
    
    def on_render(self):
        self._display_surf.fill(BLUE)
        self.draw_status()
        base_y = self.height - 30
        # cityline
        for i in range(len(self.game_objects.cityline)):
            block = self.game_objects.cityline.get_block(i)
            if (block.get_flag()==False):
                continue
            startx = (i*10) + MARGINX
            starty = base_y + block.get_height()
            endx = ((i+1)*10) + MARGINX
            endy = base_y + self.game_objects.cityline.get_block(i+1).get_height()
            pygame.draw.lines(self._display_surf, LIGHTBLUE, False,
                             [(startx,starty), (startx,endy), (endx,endy)],
                             3)
        # words
        for word in self.game_objects.game_words:
            if(word.typedidx > -1):
                typed_text = word.text[:word.typedidx+1]
                self.draw_word(typed_text, GREEN, word.coord())
                untyped_text = ' '*(word.typedidx+1) + word.text[word.typedidx+1:]
                self.draw_word(untyped_text, WHITE, word.coord())
            else:
                self.draw_word(word.text, WHITE, word.coord())
        
        pygame.display.flip()
        return
    
    def draw_word(self, text, colour, coord):
        surf = self.font.render(text, True, colour)
        rect = surf.get_rect()
        rect.topleft = coord
        self._display_surf.blit(surf, rect)
        return
    
    def check_keyhit(self):
        if not self.keyhit:
            return
        if(self.typingflag):
            for word in self.game_objects.game_words:
                if word.typedidx != -1:
                    if word.text[word.typedidx+1] == self.keyhit:
                        if (word.typed() == False):
                            self.typingflag = False
                            self.score += len(word)
                            self.typed_count += 1
                    else:
                        word.typed_reset()
                        self.typingflag = False
        else:
            for word in self.game_objects.game_words:
                if word.text[0] == self.keyhit:
                    if(word.typed() != False):
                        self.typingflag = True
                    else:
                        self.score += 1
                    break
        self.game_objects.cleanup()
        self.keyhit = None
        return
    
    def draw_status(self):
        # draw status bar background
        pygame.draw.rect(self._display_surf, BLACK, (0,0,self.width,20), 0)
        # draw the score text
        text = 'Score: %s' % self.score
        self.draw_word(text, YELLOW, (self.width -150, 2))
        text = 'Level: %s' % self.level
        self.draw_word(text, YELLOW, (MARGINX, 2))
        return
        