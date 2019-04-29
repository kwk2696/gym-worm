# gym-worm

#### The original pygame code came from [Here](https://inventwithpython.com/pygame/chapter6.html).

## Rendering
1. clone the repo:
```
$ git clone https://github.com/kwk2696/gym-worm
```
2. `cd` into `gym-worm` and run:
```
$ pip install -e .
```
3. use `import gym_worm` and `gym.make('worm-v0')` to make a new worm envrionment

## Game Details
You're probably familiar with the game of snake. 
This is an OpenAI gym implementation of the game with multi gold and multi trashes options.

#### Game Options
Currently the default options are given like below:
```
grid_size = [15, 15]
num_gold = 1
num_trash = 0
```

#### Rewards
A +1 reward is returned when a worm gets the gold.

A -1 reward is returned when a worm gets the trash.

A -1 reward is returned when a worm hits its tail or wall.

A  0 reward is returned in other cases.

#### Action Space
spaces.Descrete(4): ↑ up(273), ↓ down(274), → right(275), ↓ left(276)

#### Observation space
spaces.Box(2, 2): relative position of worm head to gold & tail.

p.s. If you want to give trash, you should adjust the size of the Box to 3

#### Examle Code
Following is the example code to run the worm game, you should see a window pop up for rendering:
```
import gym
import gym_worm

#Create the worm environment
env = gym.make('worm-v0')

for i_episode in range(2):
    observation = env.reset()
    for t in range(1000):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
```

#### Reinforcement Learning
Using [stable-baselines](https://github.com/hill-a/stable-baselines) to apply reienforcement learning to worm game.

Following is the example code to apply reinforcement learning using **DQN** with **mlp policy**:
```
import gym
import gym_worm
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN

# Create and wrap the environment
env = gym.make('worm-v0')
env = DummyVecEnv([lambda: env])

# Create a model
model = DQN(
    env=env,
    policy=MlpPolicy,
    verbose=1
)

# Train the agent
model.learn(total_timesteps=1000000)

# Save the trained model
print("Saving model to worm_model.pkl")
model.save("worm_model.pkl")
```

Following is the example code to run the **trained** worm game, you should see a window pop up for rendering:
```
env = gym.make("worm-v0")
model = DQN.load("worm_model.pkl")
    
obs = env.reset()
env.render()

for t in range(10000):
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        print('episode finished after {} timesteps'.format(t), info)
        break     
