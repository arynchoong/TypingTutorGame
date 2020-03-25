# word.py
# Dimensions
STARTY = 20

class Word:
    def __init__(self, word, x):
        ''' Member objects
        self.text
        self._len
        self._x
        self._y
        self.typed_idx
        '''
        pass
    
    def __len__(self):
        '''Getter'''
        pass
    
    def get_x(self):
        '''Getter'''
        pass

    def get_y(self):
        '''Getter'''
        pass
    
    def coord(self):
        '''Getter'''
        pass
    
    def move(self, delta):
        '''Move word downwards to animate'''
        pass
    
    def set_remove(self):
        '''Set flag to be removed'''
        pass
        
    def typed(self):
        '''Returns True if completed typing word, False otherwise.'''
        pass
    
    def typed_reset(self):
        '''User typed incorrectly, reset flag'''
        pass