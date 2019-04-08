import random, pygame
from pygame.locals import *

from gym_worm.envs.worm import Gold

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

class Worm():
    
    
    def __init__(self, cell_width, cell_height):
        self.cell_width = cell_width
        self.cell_height = cell_height
    
        self.startx = random.randint(5, self.cell_width - 6)
        self.starty = random.randint(5, self.cell_height - 6)
        
        self.coordinate =   [{'x': self.startx,     'y': self.starty},
                                  {'x': self.startx - 1, 'y': self.starty},
                                  {'x': self.startx - 2, 'y': self.starty},
                                  {'x': self.startx - 3, 'y': self.starty}]
        self.direction = RIGHT

    def check_collision(self):
        if self.coordinate[HEAD]['x'] == -1 or self.coordinate[HEAD]['x'] == self.cell_width or self.coordinate[HEAD]['y'] == -1 or self.coordinate[HEAD]['y'] == self.cell_height:
            return True
        for wormBody in self.coordinate[1:]:
            if wormBody['x'] == self.coordinate[HEAD]['x'] and wormBody['y'] == self.coordinate[HEAD]['y']:
                return True
        return False

    def check_eaten_gold(self, gold, num_gold = None):
        ate = 0
        
        for i in range(num_gold):
            if self.coordinate[HEAD]['x'] == gold[i].x and self.coordinate[HEAD]['y'] == gold[i].y:
                gold[i].set_random_position()
                ate = 1
              
        if ate == 0:
            del self.coordinate[-1]
            return 0
        else:
            return 1
            
    def check_eaten_trash(self, trash, num_trash = None):
        ate = 0
        
        if(len(self.coordinate) < 1): print("len == 0")
        if(len(trash) < num_trash): print("assert")
        for i in range(num_trash):
            if self.coordinate[HEAD]['x'] == trash[i].x and self.coordinate[HEAD]['y'] == trash[i].y:
                trash[i].set_random_position()
                del self.coordinate[-1]
                ate = 1
                break
        
        if ate == 0:
            return 0
        else:
            return -1

    def set_direction(self, key):
        if (key == K_LEFT or key == K_a) and self.direction != RIGHT:
            self.direction = LEFT
        elif (key == K_RIGHT or key == K_d) and self.direction != LEFT:
            self.direction = RIGHT
        elif (key == K_UP or key == K_w) and self.direction != DOWN:
            self.direction = UP
        elif (key == K_DOWN or key == K_s) and self.direction != UP:
            self.direction = DOWN

    def move_to_direction(self):
        # move the worm by adding a segment in the direction it is moving
        if self.direction == UP:
            newHead = {'x': self.coordinate[HEAD]['x'], 'y': self.coordinate[HEAD]['y'] - 1}
        elif self.direction == DOWN:
            newHead = {'x': self.coordinate[HEAD]['x'], 'y': self.coordinate[HEAD]['y'] + 1}
        elif self.direction == LEFT:
            newHead = {'x': self.coordinate[HEAD]['x'] - 1, 'y': self.coordinate[HEAD]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.coordinate[HEAD]['x'] + 1, 'y': self.coordinate[HEAD]['y']}
        self.coordinate.insert(0, newHead)
            
