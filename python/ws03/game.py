# game.py
import pygame

# Dimensions
WIDTH = 640
HEIGHT = 480
# States
START = 1
PLAYING = 2
GAMEOVER = 3
# Colours    R    G    B
BLACK   = (  0,   0,   0)

class TypingTutor():
    def __init__(self, sound=False):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.disp_surf = self.init_display()
        self.size = WIDTH, HEIGHT
        self.running = True if self.disp_surf else False
        self.state = START
        return
    
    def execute(self):
        # Main event loop
        while self.running:
            self.check_events()
            self.render()
        return

    def render(self):
        '''Render surface'''
        self.disp_surf.fill(BLACK)

        # Blit everything to screen
        self.screen.blit(self.disp_surf, (0,0))
        pygame.display.flip()
        return
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.state = GAMEOVER
                return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.state == GAMEOVER:
                        self.state = START
                    else:
                        self.state +=1
        return

    def init_display(self):
        pygame.display.set_caption('Typing Tutor Game')
        # Create surface 
        disp_surf = pygame.Surface(self.screen.get_size())
        return disp_surf.convert()


if __name__ == '__main__':
    game = TypingTutor()
    game.execute()