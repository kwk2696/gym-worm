import random, pygame, sys
from pygame.locals import *

from gym_worm.envs.worm import Worm
from gym_worm.envs.worm import Gold
from gym_worm.envs.worm import Trash
from gym_worm.envs.worm import Grid

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

#COLOR        R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
YELLOW    = (255, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

#NUMBER of objects
num_gold = 5
num_trash = 1

class Game():

    def __init__(self, window_width = 150, window_height = 150, cell_size = 10):
        
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size

        assert self.window_width % self.cell_size == 0, "Window width must be a multiple of cell size."
        assert self.window_height % self.cell_size == 0, "Window height must be a multiple of cell size."
        
        self.cell_width = int(self.window_width / self.cell_size)
        self.cell_height = int(self.window_height / self.cell_size)
        
        self.worm = Worm(self.cell_width, self.cell_height)
        self.gold = [Gold(self.cell_width, self.cell_height) for i in range(num_gold)]
        self.trash = [Trash(self.cell_width, self.cell_height) for i in range(num_trash)]
        self.score = self.checkScore()
        
        #check object is overlapped1
        while True:            
            overlap = self.check_overlapped_object()
            if(overlap == 0):
                break;
            elif(overlap > 0):            
                self.gold[overlap].set_random_position()
            else:
                self.trash[-overlap].set_random_position()
               
        self.grid = Grid(self.cell_width, self.cell_height, self.worm, self.gold, self.trash)
    
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode((self.window_width, self.window_height))
        self.basic_font = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Wormy')
        
    def step(self, action):
        if action == 0:
            direct = 273
        elif action == 1:
            direct = 274
        elif action == 2:
            direct = 275
        else:
            direct = 276
            
        self.worm.set_direction(direct)
        self.worm.move_to_direction()
        
        #update grid        
        self.grid.update_grid(self.worm, self.gold, self.trash)
        
        #check if worm has hit itself or the edge
        if self.worm.check_collision() == True:
            return self.grid.grid.copy(), -1, True, {"Score":self.score, "End":1, "Action": direct,
            "HEADx":self.worm.coordinate[0]['x'], "HEADy":self.worm.coordinate[0]['y']}

        #check worm gets gold/trash
        self.reward = 0.0
        self.reward_g = self.worm.check_eaten_gold(self.gold, num_gold)
        self.reward_t = self.worm.check_eaten_trash(self.trash, num_trash)
        
        self.reward += self.reward_g 
        self.reward += self.reward_t
        self.score = self.checkScore()
        
        #update grid        
        self.grid.update_grid(self.worm, self.gold, self.trash)
        
        #check if worm is dead
        if self.check_worm_dead():
            return self.grid.grid.copy(), -1, True, {"Score":self.score, "End":2, "Action": direct}
        
        self.old_grid = self.grid.grid.copy()
        
        #check object is overlapped2
        while True:
            overlap = self.check_overlapped_object()
            if(overlap == 0):
                break;
            elif(overlap > 0):            
                self.gold[overlap].set_random_position()
            else:
                self.trash[-overlap].set_random_position()
        
        #update grid        
        self.grid.update_grid(self.worm, self.gold, self.trash)
        
        
        return self.grid.grid.copy(), self.reward, False, {"Score":self.score}
    
    def check_worm_dead(self):
        if len(self.worm.coordinate) == 0:
            return True
        return False   
        
    def check_overlapped_object(self):
        #check gold & worm
        for wormBody in self.worm.coordinate:
            for i in range(num_gold):
                if wormBody['x'] == self.gold[i].x and wormBody['y'] == self.gold[i].y:
                    return i
          
        #check trash
        for wormBody in self.worm.coordinate:
            for i in range(num_trash):
                if wormBody['x'] == self.trash[i].x and wormBody['y'] == self.trash[i].y:
                    return -i
        
        #check gold & worm        
        for i in range(num_gold):
            for j in range(num_trash):
                if self.gold[i].x == self.trash[j].x and self.gold[i].y == self.trash[j].y:
                    return i          
        return 0
        
    def checkScore(self):
        return len(self.worm.coordinate) - 3
    
    """ diplay rendering """
    def update_display(self):
        self.display_surf.fill(BGCOLOR)
        self.drawGrid()
        self.drawWorm()
        self.drawGold()
        self.drawTrash()
        self.drawScore()
            
        pygame.display.update()
        
    def drawScore(self):
        score = self.checkScore()
        scoreSurf = self.basic_font.render('Score: %s' % (score), True, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.window_width - 120, 10)
        self.display_surf.blit(scoreSurf, scoreRect)


    def drawWorm(self):
        for coord in self.worm.coordinate:
            x = coord['x'] * self.cell_size
            y = coord['y'] * self.cell_size
            wormSegmentRect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.display_surf, DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, self.cell_size - 8, self.cell_size - 8)
            pygame.draw.rect(self.display_surf, GREEN, wormInnerSegmentRect)

    def drawGold(self):
        #for gold in self.gold:
        for i in range(num_gold):
            x = self.gold[i].x * self.cell_size
            y = self.gold[i].y * self.cell_size
            goldRect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.display_surf, YELLOW, goldRect)
		
    def drawTrash(self):
        for i in range(num_trash):
            x = self.trash[i].x * self.cell_size
            y = self.trash[i].y * self.cell_size
            trashRect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(self.display_surf, RED, trashRect)


    def drawGrid(self):
        for x in range(0, self.window_width, self.cell_size): # draw vertical lines
            pygame.draw.line(self.display_surf, DARKGRAY, (x, 0), (x, self.window_height))
        for y in range(0, self.window_width, self.cell_size): # draw horizontal lines
            pygame.draw.line(self.display_surf, DARKGRAY, (0, y), (self.window_width, y))
            
# if __name__ == '__main__':
    # wormy = Game()
    # wormy.update_display()
    
    # while True:
        # x = int(input())
        # wormy.step(x)
        # wormy.update_display()