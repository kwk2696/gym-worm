import numpy as np

from gym_worm.envs.worm import Gold
from gym_worm.envs.worm import Trash
from gym_worm.envs.worm import Worm

class Grid():
    """
    This class generates the 3D numpy array of pixels. 
    """
   
    def __init__(self, cell_width, cell_height, worm, golds, trashes, n_gold, n_trash):
        self.n_gold = n_gold
        self.n_trash = n_trash
        self.grid = np.zeros((self.n_gold + self.n_trash + 1,2))
        self.update_grid(worm, golds, trashes)
        
        # RGB = 3
        # self.grid = np.zeros((cell_height, cell_width, 1))
        # self.update_grid(worm, golds, trashes)
        
    def update_grid(self, worm, golds, trashes):
        self.gridtail(worm)
        self.gridgold(worm, golds)
        if self.n_trash > 0:
            self.gridtrash(worm, trashes)
    
    def gridtail(self, worm):
        length = len(worm.coordinate)
        self.grid[0][0] = worm.coordinate[0]['x'] - worm.coordinate[length - 1]['x'] 
        self.grid[0][1] = worm.coordinate[0]['x'] - worm.coordinate[length - 1]['y']
        
    def gridgold(self, worm, gold):
        self.grid[1][0] = worm.coordinate[0]['x'] - gold[0].x
        self.grid[1][1] = worm.coordinate[0]['y'] - gold[0].y

    def gridtrash(self, worm, trash):
        self.grid[2][0] = worm.coordinate[0]['x'] - trash[0].x
        self.grid[2][1] = worm.coordinate[0]['y'] - trash[0].y

