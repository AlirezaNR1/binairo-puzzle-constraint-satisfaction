# each cell in puzzle
class Cell:
    def __init__(self, x, y, domain=None, value='_'):
        if domain is None:
            domain = ['w', 'b']
        self.x = x
        self.y = y
        self.domain = domain
        self.value = value
