# word.py
# Dimensions
STARTY = 20

class Word:
    def __init__(self, word, x):
        self.text = word
        self._len = len(self.text)
        self._x = x
        self._y = STARTY
        self.typed_idx = -1 # index of typed characters '-2' to remove
    
    def __len__(self):
        return self._len
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def coord(self):
        return self._x, self._y
    
    def move(self, delta):
        self._y += delta
        return
    
    def set_remove(self):
        '''Set flag to be removed'''
        self.typed_idx = -2
        return