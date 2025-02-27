# game.py
import pygame

# Dimensions
WIDTH = 640
HEIGHT = 480

class TypingTutor():
    def __init__(self, sound=False):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.disp_surf = self.init_display()
        self.size = WIDTH, HEIGHT
        self.running = True if self.disp_surf else False
        return
    
    def execute(self):
        # Main event loop
        while self.running:
            self.check_events()
            return
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
        return

    def init_display(self):
        pygame.display.set_caption('Typing Tutor Game')
        # Create surface 
        disp_surf = pygame.Surface(self.screen.get_size())
        return disp_surf.convert()


if __name__ == '__main__':
    game = TypingTutor()
    game.execute()