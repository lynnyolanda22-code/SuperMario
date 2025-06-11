"""An OpenAI Gym Super Mario Bros. environment that randomly selects levels."""

from collections.abc import Callable, Iterable

import gymnasium as gym
import numpy as np

from .enums import SuperMarioBrosRandomMode, SuperMarioBrosROMMode
from .smb_env import SuperMarioBrosEnv


class SuperMarioBrosRandomStagesEnv(gym.Env):
    """A Super Mario Bros. environment that randomly selects levels."""

    # relevant meta-data about the environment
    metadata = SuperMarioBrosEnv.metadata

    # the legal range of rewards for each step
    reward_range = SuperMarioBrosEnv.reward_range

    # observation space for the environment is static across all instances
    observation_space = SuperMarioBrosEnv.observation_space

    # action space is a bitmap of button press values for the 8 NES buttons
    action_space = SuperMarioBrosEnv.action_space

    def __init__(
        self,
        rom_mode="vanilla",
        random_mode: SuperMarioBrosRandomMode = SuperMarioBrosRandomMode.SMB_ONLY,
        stages: tuple[Iterable[str], Iterable[str]] = (set(), set()),
        max_episode_steps: int | None = None,
        truncate_function: Callable | None = None,
    ):
        """Initialize a new Random Stage Super Mario Bros environment.

        This environment randomly selects stages from the Super Mario Bros. game(s) selected.

        Args:
            rom_mode (str): the ROM mode to use when loading ROMs from disk.
            random_mode (SuperMarioBrosRandomMode): the mode to use for selecting stages.
            stages (tuple[list[str], list[str]]): select stages at random from a specific subset. The first one for Super Mario Bros. level and the second one for Super Mario Bros. 2 levels.
            max_episode_steps (int, optional): the maximum number of steps per episode before truncation.
            truncate_function (Callable, None): a function to determine if the episode should be truncated it must take the 3 following arguments:
            - self: the environment instance (to possibly access / add instance variables)
            - reward: the reward received from the last step
            - info: the info dictionary returned from the last step

        Returns:
            None

        """
        if (
            rom_mode not in SuperMarioBrosROMMode.lost_levels_values()
            and random_mode.has_lost_levels
        ):
            raise ValueError(
                f"rom_mode argument must be 'vanilla' or 'downsample' if you want to load stages from Super Mario Bros. 2 (Lost Levels). Got: {random_mode} mode."
            )

        # create a dedicated random number generator for the environment
        self.np_random = np.random.default_rng()
        # setup the environments
        self.envs = []

        # Check the correctness of the arguments
        if (
            not isinstance(stages, tuple)
            or len(stages) != 2
            or not isinstance(stages[0], Iterable)
            or not isinstance(stages[1], Iterable)
        ):
            inside_types = []
            if isinstance(stages, Iterable):
                inside_types = [type(element) for element in stages]
            raise ValueError(
                f"stages argument must be of type tuple containing two elements of type set. Got stages of type: {type(stages)}. Containing: {inside_types}."
            )
        smb_only_stages, lost_levels_only_stages = stages
        # if the stages are not provided, create a default set of stages
        if random_mode.has_smb:
            if not smb_only_stages:
                smb_only_stages = {
                    (world, stage) for world in range(1, 9) for stage in range(1, 5)
                }
            for target in smb_only_stages:
                self.envs.append(
                    SuperMarioBrosEnv(
                        rom_mode=rom_mode,
                        target=target,
                        max_episode_steps=max_episode_steps,
                        truncate_function=truncate_function,
                    )
                )

        # if the stages are not provided, create a default set of stages
        if random_mode.has_lost_levels:
            if not lost_levels_only_stages:
                lost_levels_only_stages = {
                    (world, stage) for world in range(1, 5) for stage in range(1, 5)
                }
            for target in lost_levels_only_stages:
                self.envs.append(
                    SuperMarioBrosEnv(
                        rom_mode=rom_mode,
                        lost_levels=True,
                        target=target,
                        max_episode_steps=max_episode_steps,
                        truncate_function=truncate_function,
                    )
                )

        self.env = self.envs[0]
        # create a placeholder for the image viewer to render the screen
        self.viewer = None

    @property
    def screen(self):
        """Return the screen from the underlying environment."""
        assert self.env is not None, "Environment not initialized or closed."
        return self.env.screen

    def seed(self, seed=None):
        """Set the seed for this environment's random number generator.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.

        """
        # if there is no seed, return an empty list
        if seed is None:
            return []
        # set the random number seed for the NumPy random number generator
        self.np_random = np.random.default_rng(seed)
        # return the list of seeds used by RNG(s) in the environment
        return [seed]

    def reset(self, *, seed=None, options=None):
        """Reset the observation of the environment and returns an initial observation.

        Args:
            seed (int): an optional random number seed for the next episode
            options (dict): An optional options for resetting the environment.
                Can include the key 'stages' to override the random set of
                stages to sample from.

        Returns:
            observation (np.ndarray): next frame as a result of the given action

        """
        # Seed the RNG for this environment.
        self.seed(seed)
        # Choose a random level
        self.env = self.np_random.choice(self.envs)
        # reset the environment
        return self.env.reset(seed=seed, options=options)

    def step(self, action):
        """Run one frame of the NES and return the relevant observation data.

        Args:
            action (byte): the bitmap determining which buttons to press

        Returns:
            a tuple of:
            - observation (np.ndarray): next frame as a result of the given action
            - reward (float) : amount of reward returned after given action
            - terminated (boolean): whether the episode has ended naturally or not (e.g., Mario died, Mario completed the stage)
            - truncated (boolean): whether the episode was truncated due to a time limit
            - info (dict): contains auxiliary diagnostic information

        """
        assert self.env is not None, "Environment not initialized or closed."
        return self.env.step(action)

    def close(self):
        """Close the environment."""
        # make sure the environment hasn't already been closed
        if self.env is None:
            raise ValueError("env has already been closed.")
        # iterate over each list of stages
        for env in self.envs:
            env.close()
        # close the environment permanently
        self.env = None
        # if there is an image viewer open, delete it
        if self.viewer is not None:
            self.viewer.close()

    def render(self, mode="human"):
        """Render the environment.

        Args:
            mode (str): the mode to render with:
            - human: render to the current display
            - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
              representing RGB values for an x-by-y pixel image

        Returns:
            a numpy array if mode is 'rgb_array', None otherwise

        """
        return SuperMarioBrosEnv.render(self.env, mode=mode)

    def get_keys_to_action(self):
        """Return the dictionary of keyboard keys to actions."""
        assert self.env is not None, "Environment not initialized or closed."
        return self.env.get_keys_to_action()

    def get_action_meanings(self):
        """Return the list of strings describing the action space actions."""
        assert self.env is not None, "Environment not initialized or closed."
        return self.env.get_action_meanings()


# explicitly define the outward facing API of this module
__all__ = [
    SuperMarioBrosRandomStagesEnv.__name__,
    SuperMarioBrosRandomMode.__name__,
]  # pyright: ignore [reportUnsupportedDunderAll]
