class Cell:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        # self.value = -1
        self.element = []
        self.is_visited = False
        self.is_breeze = False
        self.is_stench = False
        self.is_whiff = False
        self.is_glow = False
        self.is_scream = False
        self.is_safe = False
