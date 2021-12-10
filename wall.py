class Wall:
    def __init__(self, x):
        self.x = x
    
    def nearest_from(self, x, y):
        return self.x - x, 0
