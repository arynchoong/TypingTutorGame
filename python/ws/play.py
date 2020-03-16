# play.py
import pygame

# Colours    R    G    B
BLACK   = (  0,   0,   0)
GREEN   = (  0, 255,   0)

class GamePlay():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('Consolas Bold.ttf', 24)
        
    def execute(self):
        self.render()
        return
        
    def render(self):
        '''Render surface'''
        # Create surface
        disp_surf = pygame.Surface(self.screen.get_size())
        self.disp_surf = disp_surf.convert()
        self.disp_surf.fill(BLACK) # Fill background
        # set the text for display
        self.draw_text("Playing ...", GREEN, self.disp_surf.get_rect().center)
        # Blit everything to screen
        self.screen.blit(self.disp_surf, (0,0))
        pygame.display.flip()
        return
    
    def draw_text(self, text, colour, center):
        # Display some text
        textsurf = self.font.render(text, True, colour)
        textrect = textsurf.get_rect()
        textrect.center = center
        self.disp_surf.blit(textsurf, textrect)
        return