# City line 

import random

MARGINX = 6
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

class Block:
    def __init__(self, flag=True, height = 0):
        self.flag = flag
        self.height = height
        return
    def set_flag(self, flag):
        self.flag = flag
        return
    def get_flag(self):
        return self.flag
    def set_height(self, height):
        self.height = height
        return
    def get_height(self):
        return self.height
    
class Cityline:
    def __init__(self, screen_width):
        self.len = int(screen_width/10)
        self.cityline = []
        # with 10 px blocks, randomize building height
        for i in range(self.len):
            # each block is (flag,height) 
            self.cityline.append(Block(True, random.randint(1,20)))
        # n blocks require n+1 coordinates. last block redundant
        self.cityline[-1].set_flag(False) 
        return
    
    def __iter__(self):
        return CityIterator(self.cityline)
    
    def __len__(self):
        return self.len
    
    def check_gameover(self):
        if all(block.get_flag() == False for block in self.cityline):
            return True
        return False
    
    def del_blocks(self, startx, strlen):
        startidx = int((startx) / 10)
        endidx = (startidx + int((FONTWIDTH * strlen) / 10))
        if endidx >= self.len:
            endidx = self.len-1
        for i in range(startidx, endidx+1):
            self.cityline[i].set_flag(False)
        return
    
    def get_block(self, index):
        return self.cityline[index]
    
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