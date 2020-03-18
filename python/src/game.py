import pygame
from play import GamePlay

# Dimensions
WIDTH = 640
HEIGHT = 480
# States
START = 1
PLAYING = 2
GAMEOVER = 3
# Colours    R    G    B
BLACK   = (  0,   0,   0)
GREEN   = (  0, 255,   0)
# Resources
RESFOLDER = '../../res/'

class TypingTutor():
    def __init__(self):
        pygame.init() # initialises Pygame libraries
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.disp_surf = self.init_display()
        self.size = WIDTH, HEIGHT
        self.running = True if self.disp_surf else False
        self.state = START
        self.bigfont = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 36)
        self.game = None
        return
    
    def init_display(self):
        pygame.display.set_caption('Typing Tutor Game')
        # Create surface
        disp_surf = pygame.Surface(self.screen.get_size())
        return disp_surf.convert()

    def execute(self):
        # Event loop
        while self.running:
            self.check_event()
            if self.state == PLAYING:
                self.game = GamePlay(self.screen)
                self.game.execute()
                self.state += 1
            else:
                self.render()
        return
        
    def check_event(self):
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
    
    def render(self):
        '''Render surface'''
        self.disp_surf.fill(BLACK)
        
        # set the text for display
        if self.state == START:
            text = 'Typing Tutorial Game'
            message = 'Press space to play.'
        else:
            text = 'Game Over'
            message = 'Score: %s' % self.game.score

        # draw the messages
        self.draw_text(text, GREEN, (WIDTH / 2, HEIGHT / 2 - 50))
        self.draw_text(message, GREEN, (WIDTH / 2, HEIGHT / 2 + 50))
        
        # Blit everything to screen
        self.screen.blit(self.disp_surf, (0,0))
        pygame.display.flip()
        return
    
    def draw_text(self, text, colour, center):
        # Display some text
        textsurf = self.bigfont.render(text, True, colour)
        textrect = textsurf.get_rect()
        textrect.center = center
        self.disp_surf.blit(textsurf, textrect)
        return

if __name__ == '__main__': 
    game = TypingTutor()
    game.execute()