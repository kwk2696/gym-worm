import random

class Gold():
    
    def __init__(self, cell_width, cell_height):
        self.cell_width = cell_width
        self.cell_height = cell_height
        
        self.set_random_position()

    def set_random_position(self):
        self.x = random.randint(0, self.cell_width - 1)
        self.y = random.randint(0, self.cell_height - 1)