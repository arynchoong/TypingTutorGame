# city.py
import random
# Dimensions
MARGINX = 5
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

class Cityline:
    def __init__(self, screen_width):
        self._len = int(screen_width / 10)
        self.cityline = []
        for i in range(self._len):
            self.cityline.append(Block(height = random.randint(1,20)))
        self.cityline[-1].del_block()
        return
    
    def __iter__(self):
        return CityIterator(self.cityline)
    
    def __len__(self):
        return self._len
    
    def del_blocks(self, start_x, str_len):
        startidx = int((start_x - MARGINX) / 10)
        endidx = startidx + int((FONTWIDTH * str_len) / 10)
        if endidx >= self._len:
            endidx = self.len - 1
        for i in range(startidx, endidx+1):
            self.cityline[i].del_block()
        return
    
    def check_gameover(self):
        if all(block.get_flag() == False for block in self.cityline):
            return True
        return False
    

class CityIterator:
    def __init__(self, city):
        self.city = city
        self.index = 0
    
    def __next__(self):
        try:
            block = self.city[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return block
    
    def __iter__(self):
        return self
    
    
class Block:
    def __init__(self, flag = True, height = 0):
        self.flag = flag
        self.height = height
        return
    
    def del_block(self):
        self.flag = False
        return
    
    def get_flag(self):
        return self.flag
    
    def get_height(self):
        return self.height

