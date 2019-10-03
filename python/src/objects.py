# Typing tutorial game objects

import random
from word import Word
from city import Cityline

MARGINX = 6
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

RESFOLDER = '../../res/'

class Objects:
    def __init__(self, screen_width, screen_height):
        self.wordlist = self.init_words()
        self.game_words = []
        self.width = screen_width
        self.bound_y = screen_height - 40
        self.cityline = Cityline(screen_width)
        
    def init_words(self):
        words_list = None
        try:
            with open(RESFOLDER+"brown.txt", "r", newline='') as file:
                words_list = [line.strip() for line in file.readlines()]
        except:
            # Error handling, provide default:
            words_list = ['a','b','c','d','e','f','g','h','i','j','k',
                             'l','m','n','o','p','q','r','s','t','u','v',
                             'x','y','z']
            random.shuffle(words_list)
        self.wordlist_len = len(words_list)
        return words_list
    
    def add_word(self, level):
        # check that word doesn't duplicate first character in list
        word = random.choice(self.wordlist[:min(self.wordlist_len,1000*level)])
        firstchar = [word.text[0] for word in self.game_words]
        while (word[0] in firstchar):
            word = random.choice(self.wordlist)

        # calculate list of city blocks still standing
        avail_block = []
        for idx, block in enumerate(self.cityline):
            if block.get_flag() == True:
                avail_block.append(idx)
        x_avail = random.choice(avail_block)*10 + MARGINX
        # calculate max x of word
        max_x = (self.width - MARGINX) - (FONTWIDTH * len(word))
        x = random.randint(MARGINX,max_x)
        # randomize fun
        x = random.choice([x_avail,x])
        x = min(x,max_x)
        
        self.game_words.append(Word(word, x))
        return self.game_words[-1]
    
    def move(self, delta):
        removed_typing = False
        if not self.game_words:
            return
        for word in self.game_words:
            word.move(delta)
            # check y boundary
            if word.get_y() >= self.bound_y:
                if word.typedidx >= 0:
                    removed_typing = True
                word.set_remove()
                self.cityline.del_blocks(word.get_x(), len(word))
        self.cleanup()
        return removed_typing
    
    def cleanup(self):
        if not self.game_words:
            return
        # remove words from game_words with word.typedidx == -2
        self.game_words = [w for w in self.game_words if w.typedidx != -2]