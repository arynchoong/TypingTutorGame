# play.py
import pygame
from objects import GameObjects

# Colours        R    G    B
BLUE        = (  0,   0, 128)
WHITE       = (255, 255, 255)
GREEN       = (  0, 200,   0)
BLACK       = (  0,   0,   0)
YELLOW      = (255, 255,   0)
LIGHTBLUE   = (135, 206, 235)
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
        self.game_objects = GameObjects(self.width, self.height)
        self.last_add = 0 # time of adding word
        self.add_timeout = 2000 # 2 seconds
        self.fps = 25
        self.fpsclock = pygame.time.Clock()
        self.ydelta = 1
        self.typing_flag = False
        self.score = 0
        self.keyhit = None
        self.level = 1
        self.typed_count = 0
        self.error_count = 0
        
    def execute(self):
        while self.playing:
            self.check_events()
            self.loop()
            self.render()
            self.fpsclock.tick(self.fps)
        return
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.TEXTINPUT:
                self.keyhit = event.text
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
        return
    
    def loop(self):
        self.check_keyhit()
        if self.game_objects.is_gameover():
            self.playing = False
            return

        if self.game_objects.move(self.ydelta): # If moved beyond boundary Y
            self.typing_flag = False
        self.add_word()
        return
        
    def render(self):
        '''Render surface'''
        self.disp_surf.fill(BLUE) # Fill background
        self.draw_score()
        
        # set the words for display
        for word in self.game_objects.game_words:
            if word.typedidx > -1:
                typed_text = word.text[:word.typedidx+1]
                untyped_text = ' '*(word.typedidx+1) + word.text[word.typedidx+1:]
                self.draw_word(untyped_text, WHITE, word.coord())
                self.draw_word(typed_text, GREEN, word.coord())
            else:
                self.draw_word(word.text, WHITE, word.coord())
        
        # cityline
        base_y = self.height - 30
        start_x = MARGINX
        start_y = base_y
        for block in self.game_objects.cityline:
            end_x = start_x + 10
            end_y = base_y + block.get_height()
            if block.get_flag():
                pygame.draw.lines(self.disp_surf, LIGHTBLUE, False,
                    [(start_x,start_y), (start_x,end_y), (end_x,end_y)], 3)
            start_y = end_y
            start_x = end_x
        
        # Blit everything to screen
        self.screen.blit(self.disp_surf, (0,0))
        pygame.display.flip()
        return

    def draw_word(self, text, colour, coord):
        # Display some text
        textsurf = self.font.render(text, True, colour)
        textrect = textsurf.get_rect()
        textrect.topleft = coord
        self.disp_surf.blit(textsurf, textrect)
        return
        
    def add_word(self):
        if self.game_objects.is_gameover():
            return
        # Check if valid to add
        if not self.game_objects.game_words or (
            (pygame.time.get_ticks() - self.last_add) > self.add_timeout):
            if self.game_objects.add_word(self.level):
                self.last_add = pygame.time.get_ticks()
        return
    
    def check_keyhit(self):
        if not self.keyhit:
            return
        if self.typing_flag:
            for word in self.game_objects.game_words:
                if word.typedidx != -1:
                    if word.text[word.typedidx+1] == self.keyhit:
                        if word.typed():
                            self.typing_flag = False
                            self.add_score(len(word))
                    else:
                        word.typed_reset()
                        self.typing_flag = False
                        self.error_count += 1
        else:
            for word in self.game_objects.game_words:
                if word.text[0] == self.keyhit:
                    if word.typed():
                        self.add_score(1)
                    else:
                        self.typing_flag = True
                    break
        self.game_objects.clean_up()
        self.keyhit = None
        return
    
    def add_score(self, score):
        self.score += score
        self.typed_count += 1
        
        # Level up
        if self.typed_count >= 4:
            self.level += 1
            self.typed_count = 0
            # Increase difficulty when leveling up
            if self.fps < 70:
                self.fps += 3
            elif self.ydelta < 5:
                self.ydelta +=1
            elif self.add_timeout > 900:
                self.add_timeout -= 150
        return

    def draw_score(self):
        # draw status bar background
        pygame.draw.rect(self.disp_surf, BLACK, (0,0,self.width,20), 0)
        # draw score text
        text = 'Score: %s' % self.score
        self.draw_word(text, YELLOW, (self.width - 150, 2))
        # draw level text
        text = 'Level: %s' % self.level
        self.draw_word(text, YELLOW, (MARGINX, 2))
        return
        