"""An OpenAI Gym Super Mario Bros. environment that randomly selects levels."""

from collections.abc import Callable
from typing import TypeAlias, Union

import gymnasium as gym
import numpy as np

from .enums import SuperMarioBrosRandomMode, SuperMarioBrosROMMode
from .smb_env import SuperMarioBrosEnv

StageCollection = Union[
    set[tuple[int, int]], list[tuple[int, int]], tuple[tuple[int, int], ...]
]
StageTuple: TypeAlias = tuple[StageCollection, StageCollection]


def validate_stages(stages: StageTuple) -> None:
    """Validate the structure and types of the `stages` argument.

    Args:
        stages (StageTuple): subset of stages which are randomly picked at each episode. The first part of it is for Super Mario Bros. levels and the second one for Super Mario Bros. 2 levels.
    """
    if not isinstance(stages, (list, tuple)):
        raise TypeError(
            f"`stages` must be a list or tuple of two set, list or tuple of (int, int) pairs. Got type: {type(stages).__name__}"
        )
    if len(stages) != 2:
        raise ValueError(
            f"`stages` must contain exactly two elements (one per stage type). Got: {len(stages)} elements."
        )

    for i, stage_group in enumerate(stages):
        if not isinstance(stage_group, (set, list, tuple)):
            raise TypeError(
                f"Element {i} of `stages` must be a set, list or tuple of int. Got type: {type(stage_group).__name__}"
            )

        for j, pair in enumerate(stage_group):
            if not isinstance(pair, (tuple, list)):  #
                raise TypeError(
                    f"Element {j} in stage group {i} must be a tuple or list of two integers. Got: {repr(pair)} of type {type(pair).__name__}"
                )
            if len(pair) != 2:
                raise ValueError(
                    f"tuple {j} in stage group {i} must contain exactly two integers. Got length: {len(pair)} — value: {repr(pair)}"
                )
            if not all(isinstance(x, int) for x in pair):
                types = tuple(type(x).__name__ for x in pair)
                raise TypeError(
                    f"Both elements of tuple {j} in stage group {i} must be integers. Got types: {types} — value: {repr(pair)}"
                )


def flatten_stages(
    stages: StageTuple, random_mode: SuperMarioBrosRandomMode
) -> list[tuple[bool, tuple[int, int]]]:
    """Flatten the stages argument. Turns it into a valid environment dictionary key.

    Args:
        stages (StageTuple): subset of stages which are randomly picked at each episode. The first part of it is for Super Mario Bros. levels and the second one for Super Mario Bros. 2 levels.
        random_mode (SuperMarioBrosRandomMode): the random mode used in the environment. It determines which ROM are used.

    Returns:
        list[tuple[bool, tuple[int, int]]]:
            A flattened list of stage keys used in the environment dictionary.
    """
    smb_only_stages, lost_levels_only_stages = stages
    stage_pool = []

    if random_mode.has_smb:
        stage_pool.extend([(False, stage) for stage in smb_only_stages])

    if random_mode.has_lost_levels:
        stage_pool.extend([(True, stage) for stage in lost_levels_only_stages])

    return stage_pool


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
        rom_mode: str = "vanilla",
        random_mode: SuperMarioBrosRandomMode = SuperMarioBrosRandomMode.SMB_ONLY,
        stages: StageTuple = (set(), set()),
        max_episode_steps: int | None = None,
        truncate_function: Callable | None = None,
    ):
        """Initialize a new Random Stage Super Mario Bros environment.

        This environment randomly selects stages from the Super Mario Bros. game(s) selected.

        Args:
            rom_mode (str): the ROM mode to use when loading ROMs from disk.
            random_mode (SuperMarioBrosRandomMode): the mode to use for selecting stages.
            stages (StageTuple): subset of stages which are randomly picked at each episode. The first part of it is for Super Mario Bros. levels and the second one for Super Mario Bros. 2 levels.
            max_episode_steps (int, optional): the maximum number of steps per episode before truncation.
            truncate_function (Callable, None): a function to determine if the episode should be truncated it must take the 3 following arguments:
            - self: the environment instance (to possibly access / add instance variables)
            - reward: the reward received from the last step
            - info: the info dictionary returned from the last step

        Returns:
            None

        """
        # save the random mode used
        self.random_mode = random_mode

        if (
            rom_mode not in SuperMarioBrosROMMode.lost_levels_values()
            and random_mode.has_lost_levels
        ):
            raise ValueError(
                f"rom_mode argument must be 'vanilla' or 'downsample' if you want to load stages from Super Mario Bros. 2 (Lost Levels). Got: {random_mode} mode."
            )

        # create a dedicated random number generator for the environment
        self.np_random = np.random.default_rng()
        # setup the environments dictionary
        self.envs = dict()

        # Check the correct typing of stages
        validate_stages(stages)
        self.stage_pool_keys = flatten_stages(stages, self.random_mode)

        if random_mode.has_smb:
            all_smb_keys = [
                (False, (world, stage))
                for world in range(1, 9)
                for stage in range(1, 5)
            ]
            # if the stages are not provided, create a default set of stages
            if len(stages[0]) == 0:
                self.stage_pool_keys.extend(all_smb_keys)
            for key in all_smb_keys:
                lost_levels, target = key
                self.envs[key] = SuperMarioBrosEnv(
                    rom_mode=rom_mode,
                    lost_levels=lost_levels,
                    target=target,
                    max_episode_steps=max_episode_steps,
                    truncate_function=truncate_function,
                )

        if random_mode.has_lost_levels:
            all_lost_levels_keys = [
                (True, (world, stage)) for world in range(1, 5) for stage in range(1, 5)
            ]
            # if the stages are not provided, create a default set of stages
            if len(stages[1]) == 0:
                self.stage_pool_keys.extend(all_lost_levels_keys)
            for key in all_lost_levels_keys:
                lost_levels, target = key
                self.envs[key] = SuperMarioBrosEnv(
                    rom_mode=rom_mode,
                    lost_levels=lost_levels,
                    target=target,
                    max_episode_steps=max_episode_steps,
                    truncate_function=truncate_function,
                )
        # get the first env of the dictionary using the first key of the pool
        self.env = self.envs[self.stage_pool_keys[0]]
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

        if options is not None and "stages" in options and isinstance(options, dict):
            # Choose a random level by overriding the input pool
            stages = options["stages"]
            validate_stages(stages)
            new_stage_pool_keys = flatten_stages(stages, self.random_mode)
            if len(new_stage_pool_keys) == 0:
                raise ValueError(
                    "You cannot provide an empty collection of levels to choose from."
                )
            idx = self.np_random.integers(len(new_stage_pool_keys))
            chosen_key = new_stage_pool_keys[idx]
        else:
            # Choose a random level according to the input pool
            idx = self.np_random.integers(len(self.stage_pool_keys))
            chosen_key = self.stage_pool_keys[idx]

        # Select the level
        try:
            self.env = self.envs[chosen_key]
        except KeyError:
            raise KeyError(
                f"The chosen (<world>-<stage>) <game> combination does not exists. Chosen: level {chosen_key[1]} for {'Super Mario Bros. 2 (Lost Levels)' if chosen_key[0] else 'Super Mario Bros.'} ."
                f"Available: {[(key[1], 'Super Mario Bros. 2 (Lost Levels)' if key[0] else 'Super Mario Bros.') for key in list(self.envs.keys())]}"
            )
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
        for env in self.envs.values():
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
        return SuperMarioBrosEnv.render(self, mode=mode)

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
