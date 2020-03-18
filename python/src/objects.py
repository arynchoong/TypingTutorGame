# game objects.py
import string
import random
from word import Word
# Dimensions
MARGINX = 5
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size
# Resources
RESFOLDER = '../../res/'

class GameObjects:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.wordlist = self.init_words()
        self.game_words = []
        self.bound_y = screen_height - 40

    def init_words(self):
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
        word = random.choice(self.wordlist)
        firstchar = [word.text[0] for word in self.game_words]
        while word[0] in firstchar:
            word = random.choice(self.wordlist)
        
        # Calculate the max of x position of word
        max_x = (self.screen_width - MARGINX) - (FONTWIDTH * len(word))
        
        # Some randomised fun
        x = random.randint(MARGINX,max_x)
        
        self.game_words.append(Word(word, x))
        return True

    def move(self, delta):
        removed_typing = False
        for word in self.game_words:
            word.move(delta)
            if word.get_y() >= self.bound_y:
                if word.typedidx >= 0:
                    removed_typing = True
                word.set_remove()
        self.clean_up()
        return removed_typing
    
    def clean_up (self):
        if not self.game_words:
            return
        # Remove words from game_words with word.typedidx == -2
        self.game_words = [w for w in self.game_words if w.typedidx != -2]
        return