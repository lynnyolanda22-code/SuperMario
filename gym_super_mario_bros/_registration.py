"""Registration code of Gym environments in this package."""

import gymnasium as gym

from .enums import SuperMarioBrosRandomMode, SuperMarioBrosROMMode


def _register_mario_env(id, is_random=False, **kwargs):
    """Register a Super Mario Bros. (1/2) environment with OpenAI Gym.

    Args:
        id (str): id for the env to register
        is_random (bool): whether to use the random levels environment
        kwargs (dict): keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    # if the is random flag is set
    if is_random:
        # set the entry point to the random level environment
        entry_point = "gym_super_mario_bros:SuperMarioBrosRandomStagesEnv"
    else:
        # set the entry point to the standard Super Mario Bros. environment
        entry_point = "gym_super_mario_bros:SuperMarioBrosEnv"
    # register the environment
    gym.envs.registration.register(  # pyright: ignore[reportAttributeAccessIssue]
        id=id,
        entry_point=entry_point,
        reward_threshold=9999999,
        kwargs=kwargs,
        nondeterministic=True,
    )


# Super Mario Bros.
for rom_mode in SuperMarioBrosROMMode:
    _register_mario_env(
        f"SuperMarioBros-{rom_mode.value.capitalize()}", rom_mode=rom_mode.value
    )


# Super Mario Bros. Random Levels
for random_mode in SuperMarioBrosRandomMode:
    for rom_mode in SuperMarioBrosROMMode:
        if random_mode.has_lost_levels and not rom_mode.suitable_for_lost_levels:
            continue
        _register_mario_env(
            f"SuperMarioBrosRandomStages-{rom_mode.value.capitalize()}-{random_mode.value}",
            is_random=True,
            rom_mode=rom_mode.value,
            random_mode=random_mode,
        )


# Super Mario Bros. 2 (Lost Levels)
for rom_mode in SuperMarioBrosROMMode.lost_levels_values():
    _register_mario_env(
        f"SuperMarioBros2-{rom_mode.capitalize()}",
        lost_levels=True,
        rom_mode=rom_mode,
    )


def _register_mario_stage_env(id, **kwargs):
    """Register a Super Mario Bros. (1/2) stage environment with OpenAI Gym.

    Args:
        id (str): id for the env to register
        kwargs (dict): keyword arguments for the SuperMarioBrosEnv initializer

    Returns:
        None

    """
    # register the environment
    gym.envs.registration.register(  # pyright: ignore[reportAttributeAccessIssue]
        id=id,
        entry_point="gym_super_mario_bros:SuperMarioBrosEnv",
        reward_threshold=9999999,
        kwargs=kwargs,
        nondeterministic=True,
    )


# iterate over all the rom modes for Super Mario Bros., worlds (1-8), and stages (1-4)
for rom_mode in SuperMarioBrosROMMode.rom_modes_values():
    for world in range(1, 9):
        for stage in range(1, 5):
            # create the target
            target = (world, stage)
            # setup the frame-skipping environment
            env_id = f"SuperMarioBros-{world}-{stage}-{rom_mode.capitalize()}"
            _register_mario_stage_env(env_id, rom_mode=rom_mode, target=target)

# iterate over all the rom modes for Super Mario Bros. 2 (Lost Levels), worlds (1-12), and stages (1-4)
for rom_mode in SuperMarioBrosROMMode.lost_levels_values():
    for world in range(1, 13):
        for stage in range(1, 5):
            # create the target
            target = (world, stage)
            # setup the frame-skipping environment
            env_id = f"SuperMarioBros2-{world}-{stage}-{rom_mode.capitalize()}"
            _register_mario_stage_env(
                env_id, rom_mode=rom_mode, target=target, lost_levels=True
            )


# create an alias to gym.make for ease of access
make = gym.make

# define the outward facing API of this module (none, gym provides the API)
__all__ = [make.__name__]  # pyright: ignore [reportUnsupportedDunderAll]
