# word.py
# Dimensions
STARTY = 20

class Word:
    def __init__(self, word, x):
        self.text = word
        self._len = len(self.text)
        self._x = x
        self._y = STARTY
    
    def __len__(self):
        return self._len
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def coord(self):
        return self._x, self._y
    