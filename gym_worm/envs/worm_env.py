import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from gym_worm.envs.worm import Game

class WormEnv(gym.Env):
    metadata = {'render.modes': ['human'] }
    
    # TODO: define observation_space
    def __init__(self, grid_width = 150, grid_height = 150, cell_size = 10, 
    n_worm = 1, n_gold = 1, n_trash = 0):
        self.width = grid_width
        self.height = grid_height
        self.cell_size = cell_size
        self.n_worm = n_worm
        self.n_gold = n_gold
        self.n_trash = n_trash
        self.cell_width = int(self.width / self.cell_size)
        self.cell_height = int(self.height / self.cell_size)
        
        self.action_space = spaces.Discrete(4)
        self.observation_size = self.n_gold + self.n_trash + 1
        self.observation_space = spaces.Box(low = -100, high = 100, shape = (self.observation_size,2))
        
        #self.observation_space = spaces.Box(low = 0, high = 3, shape = (self.cell_height, self.cell_width, 1))
        self.viewer = None
        
    def step(self, action):
        obs, reward, done, info = self.game.step(action)
        return obs, reward, done, info
        
    def reset(self):
        self.game = Game(self.width, self.height, self.cell_size, self.n_gold, self.n_trash)
        obs = self.game.grid.grid.copy()
        return obs

    def render(self, mode='human', close=False):
        return self.game.update_display()
    
    def seed(self, seed=None):
        pass