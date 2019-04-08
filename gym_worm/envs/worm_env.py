import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_worm.envs.worm import Game

class WormEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    # TODO: define observation_space
    def __init__(self, grid_width = 640, grid_height = 480, cell_size = 10, 
    n_worm = 1, n_gold = 1, n_trash = 1):
        self.action_space = spaces.Discrete(4)
        self.viewer = None
        
        self.width = grid_width
        self.height = grid_height
        self.cell_size = cell_size
        self.n_worm = n_worm
        self.n_gold = n_gold
        self.n_trash = n_trash
        
    def step(self, action):
        self.obs, reward, done, info = self.game.step(action)
        return self.obs, reward, done, info
        
    def reset(self):
        self.game = Game(self.width, self.height, self.cell_size)
        self.obs = self.game.grid.grid.copy()
        return self.obs

    def render(self, mode='human', close=False):
        return self.game.update_display()
    
    def seed(self, seed):
        pass