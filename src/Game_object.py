class Game_object(object):    
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h    
    def wymiary(self):
        return [self.x, self.y, self.w, self.h]