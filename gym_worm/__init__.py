from gym.envs.registration import register

register(
    id='worm-v0',
    entry_point='gym_worm.envs:WormEnv',
)
# register(
    # id='worm-extrahard-v0',
    # entry_point='gym_worm.envs:WormExtraHardEnv',
# )