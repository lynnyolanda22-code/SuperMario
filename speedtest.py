"""A script to test the speed of the Super Mario Bros. environment."""

import tqdm

from gym_super_mario_bros import SuperMarioBrosEnv

env = SuperMarioBrosEnv()

terminated = True

try:
    for _ in tqdm.tqdm(range(5000)):
        if terminated:
            observation, info = env.reset()
            terminated = False
        else:
            observation, reward, terminated, truncated, info = env.step(
                env.action_space.sample()
            )
except KeyboardInterrupt:
    pass
