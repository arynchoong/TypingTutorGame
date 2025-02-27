# play.py
import pygame
from objects import GameObjects

# Colours        R    G    B
BLUE        = (  0,   0, 128)
WHITE       = (255, 255, 255)
# Resources
RESFOLDER = '../../res/'

class GamePlay():
    def __init__(self, screen, sound=False):
        pygame.init()
        self.screen = screen
        self.disp_surf = pygame.Surface(self.screen.get_size()).convert()
        self.width, self.height = screen.get_size()
        self.font =  pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 16)
        self.playing = True
        self.game_objects = GameObjects(self.width, self.height)
        self.last_add = 0 # time of adding word
        self.add_timeout = 2000 # 2 seconds
        self.fps = 25
        self.fps_clock = pygame.time.Clock()
        self.y_delta = 1        
        
    def execute(self):
        '''Start a game'''
        while self.playing:
            self.check_events()
            self.loop()
            self.render()
            self.fps_clock.tick(self.fps)
        return
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
        return
    
    def loop(self):
        '''Game loop'''
        self.game_objects.move(self.y_delta)
        self.add_word()
        
    def render(self):
        '''Render surface'''
        self.disp_surf.fill(BLUE) # Fill background
        
        # Draw word on screen
        for word in self.game_objects.game_words:
            self.draw_word(word.text, WHITE, word.coord())

        # Blit everything to screen
        self.screen.blit(self.disp_surf, (0,0))
        pygame.display.flip()
        return

    def draw_word(self, text, colour, coord):
        '''Display some text'''
        text_surf = self.font.render(text, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.topleft = coord
        self.disp_surf.blit(text_surf, text_rect)
        return

    def add_word(self):
        # Check if valid to add
        if not self.game_objects.game_words or (
            (pygame.time.get_ticks() - self.last_add) > self.add_timeout):
            if self.game_objects.add_word():
                self.last_add = pygame.time.get_ticks()
        return