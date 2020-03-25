# city.py
import random
# Dimensions
MARGINX = 5
FONTWIDTH = 9 # based on Consolas Bold 16 pt font size

class CityLine:
    def __init__(self, screen_width):
        ''' Member objects
        self._len
        self.city_line
        # Initialise city blocks
        '''
        pass

    def __iter__(self):
        return CityIterator(self.city_line)
    
    def __len__(self):
        return self._len
    
    def del_blocks(self, start_x, str_len):
        '''Delete associalted block that is hit by untyped words.'''
        pass

    
    def check_gameover(self):
        '''Returns true if all blocks are destroyed'''
        pass
    

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
        ''' Member objects
        self.flag
        self.height
        '''
        pass
    
    def del_block(self):
        '''Remove city block'''
        pass
    
    def get_flag(self):
        '''Getter'''
        pass
    
    def get_height(self):
        '''Getter'''
        pass

