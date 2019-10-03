# Workshop testing

import pygame
from pygame.locals import *
from play import GamePlay

WIDTH = 640
HEIGHT = 480
# Game States
START = 1
PLAYING = 2
GAMEOVER = 3
#            R    G    B
BLACK   = (  0,   0,   0)
GREEN   = (  0, 255,   0)

RESFOLDER = '../../res/'

class TypingTutor():
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = WIDTH, HEIGHT
        self.state = START
        self.score = 0
        
    def on_init(self):
        pygame.init()
        pygame.display.set_caption('Typing Tutor Game')
        self._display_surf = pygame.display.set_mode(self.size)
        self.bigfont = pygame.font.Font(RESFOLDER+'Consolas Bold.ttf', 32)
        return True if self._display_surf else False
        
    def on_cleanup(self):
        pygame.quit()
        return
    
    def on_execute(self):
        if not self.on_init():
            self._running = False
        # main game loop
        while (self._running):
            self.on_render()
            self.on_check_event()
            self.on_loop()
        self.on_cleanup()
        return
    
    def on_loop(self):
        if (self.state == PLAYING):
            # start game
            self.score = GamePlay(self._display_surf).on_execute()
            if (self.score == -1):
                self._running = False
            self.state = GAMEOVER
        return

    def on_render(self):
        self._display_surf.fill(BLACK)
        message = ''
        if self.state == START:
            text = 'Typing Tutorial Game'
            message = 'Press any key to play.'
        elif self.state == GAMEOVER:
            text = 'Game Over'
            message = 'Score: %s' % self.score
        else:
            text = 'Playing'
        
        self.on_draw_text(text, GREEN, (int(self.width/2), int(self.height/2)-50))
        
        if len(message):
            self.on_draw_text(message, GREEN, (int(self.width/2), int(self.height/2)+50))
        
        pygame.display.flip()
        return
        
    def on_draw_text(self, text, colour, center):
        surf = self.bigfont.render(text, True, colour)
        rect = surf.get_rect()
        rect.center = center
        self._display_surf.blit(surf, rect)
        return
    
    def on_check_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False
                self.state = GAMEOVER
            elif event.type == KEYUP:
                if (self.state == GAMEOVER):
                    self.state = 1
                else:
                    self.state += 1
        return


if __name__=="__main__":
    game = TypingTutor()
    game.on_execute()
    