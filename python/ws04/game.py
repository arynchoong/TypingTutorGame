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
GREEN   = (  0, 255,   0)
# Resources
RESFOLDER = '../../res/'

class TypingTutor():
    def __init__(self, sound=False):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.disp_surf = self.init_display()
        self.size = WIDTH, HEIGHT
        self.running = True if self.disp_surf else False
        self.state = START
        self.font = pygame.font.Font(RESFOLDER + 'Consolas Bold.ttf', 36)
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

        # set the text for display
        if self.state == START:
            text = 'Typing Tutorial Game'
            message = 'Press space to play.'
        else:
            text = 'Game Over'
            message = 'State: %s' % self.state

        # draw the messages
        self.draw_text(text, GREEN, (int(WIDTH / 2), int(HEIGHT / 2) - 50))
        self.draw_text(message, GREEN, (int(WIDTH / 2), int(HEIGHT / 2) + 50))

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

    def draw_text(self, text, colour, center):
        '''Draws text onto diplay surface'''
        text_surf = self.font.render(text, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = center
        self.disp_surf.blit(text_surf, text_rect)

if __name__ == '__main__':
    game = TypingTutor()
    game.execute()