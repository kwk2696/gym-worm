import numpy as np

from gym_worm.envs.worm import Gold
from gym_worm.envs.worm import Trash
from gym_worm.envs.worm import Worm

#COLOR                 R    G    B
WHITE     = np.array((255, 255, 255), dtype=np.uint8)
BLACK     = np.array((  0,   0,   0), dtype=np.uint8)
RED       = np.array((255,   0,   0), dtype=np.uint8)
GREEN     = np.array((  0, 255,   0), dtype=np.uint8)
YELLOW    = np.array((255, 255,   0), dtype=np.uint8)
DARKGREEN = np.array((  0, 155,   0), dtype=np.uint8)
DARKGRAY  = np.array(( 40,  40,  40), dtype=np.uint8)
BGCOLOR = BLACK

class Grid():
    """
    This class generates the 3D numpy array of pixels. 
    """
   
    def __init__(self, cell_width, cell_height, worm, golds, trashes):

        RGB = 3
        self.grid = np.zeros((cell_height, cell_width, RGB), dtype=np.uint8)
        self.update_grid(worm, golds, trashes)
        
    def update_grid(self, worm, golds, trashes):
        self.gridsurf()
        self.gridworm(worm)
        self.gridgold(golds)
        self.gridtrash(trashes)
        
    def gridsurf(self):
        self.grid[:,:,:] = BGCOLOR
    
    def gridworm(self, worm):
        for coord in worm.coordinate:
            temp = np.array([coord['x'], coord['y']])
            self.draw(temp, GREEN)
            
    def gridgold(self, golds):
        for gold in golds:
            coord = np.array([gold.x, gold.y])
            self.draw(coord, YELLOW)
            
    def gridtrash(self, trashes):
        for trash in trashes:
            coord = np.array([trash.x, trash.y])
            self.draw(coord, RED)
            
    def draw(self, coord, color):
        x = int(coord[0])
        y = int(coord[1])
        self.grid[y:y+1, x:x+1, :] = color
