# Typing tutorial word objects

STARTY = 20

class Word:
    def __init__(self, word, x):
        self.text = word
        self.len = len(self.text)
        self._x = x
        self._y = STARTY
        self.typedidx = -1 # index of typed characters '-2' to remove
    
    def __len__(self):
        return self.len
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def coord(self):
        return self._x, self._y
    
    def move(self, delta):
        self._y += 1
    
    def set_remove(self):
        self.typedidx = -2
        
    def typed(self):
        self.typedidx += 1
        if (self.typedidx >= (self.len-1)):
            # completed typing word
            self.set_remove()
            return False
        return True # finished typing word
    
    def typed_reset(self):
        self.typedidx = -1
        return
