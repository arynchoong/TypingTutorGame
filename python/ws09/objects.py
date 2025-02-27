# game objects.py
import string
import random
from word import Word
from city import CityLine

# Dimensions
MARGINX = 5
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size
# Resources
RESFOLDER = '../../res/'

class GameObjects:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.word_list = self.init_words()
        self.game_words = []
        self.bound_y = screen_height - 40
        self.city_line = CityLine(screen_width)

    def init_words(self):
        '''Prepare list of words for the game'''
        words_list = None
        try:
            with open(RESFOLDER + "brown.txt", 'r', newline='') as file:
                words_list = [line.strip() for line in file.readlines()]
        except:
            # Error handling, provide default:
            words_list = list(string.ascii_letters)
            random.shuffle(words_list)
        return words_list
    
    def add_word(self):
        '''Add word to game play'''
        # Check that word doesn't duplicate first character in list
        word = random.choice(self.word_list)
        firstchar = [word.text[0] for word in self.game_words]
        while word[0] in firstchar:
            word = self.get_word()
        
        # Get the list of city blocks still standing
        avail_blocks = []
        for idx, block in enumerate(self.city_line):
            if block.get_flag() == True:
                avail_blocks.append(idx)
        x_avail = random.choice(avail_blocks) * 10 + MARGINX
        
        # Calculate the max of x position of word
        max_x = (self.screen_width - MARGINX) - (FONTWIDTH * len(word))

        # Some randomised fun
        x = random.randint(MARGINX,max_x)
        x = random.choice([x_avail, x])
        x = min(x, max_x)

        self.game_words.append(Word(word, x))
        return True
    
    def get_word(self):
          '''Randomly select word from word list for game play'''
          return random.choice(self.word_list)
    
    def move(self, delta):
        removed = False
        removed_typing = False
        for word in self.game_words:
            word.move(delta)
            if word.get_y() >= self.bound_y:
                removed = True
                if word.typed_idx >= 0:
                    removed_typing = True
                word.set_remove()
                self.city_line.del_blocks(word.get_x(), len(word))
        self.clean_up()
        return removed, removed_typing

    def clean_up (self):
        '''Check and remove any word in game that is flagged to be removed.'''
        if not self.game_words:
            return
        # Remove words from game_words with word.typed_idx == -2
        self.game_words = [w for w in self.game_words if w.typed_idx != -2]
        return
    
    def is_gameover(self):
        return self.city_line.check_gameover()