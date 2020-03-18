# play.py
import pygame

# Colours        R    G    B
BLUE        = (  0,   0, 128)
WHITE       = (255, 255, 255)
# Dimensions
MARGINX = 5
# Resources
RESFOLDER = '../../res/'

class GamePlay():
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.disp_surf = pygame.Surface(self.screen.get_size()).convert()
        self.width, self.height = screen.get_size()
        self.font =  pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 16)
        self.playing = True
        
    def execute(self):
        while self.playing:
            self.check_events()
            self.loop()
            self.render()
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
        pass
        
    def render(self):
        '''Render surface'''
        self.disp_surf.fill(BLUE) # Fill background

        self.draw_text('Playing...', WHITE, (320, 240))
        
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
        