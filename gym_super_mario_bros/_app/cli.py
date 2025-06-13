"""Super Mario Bros for OpenAI Gym."""

import argparse
import re
import sys

import gymnasium as gym
from nes_py.app.play_human import play_human  # pyright: ignore[reportMissingImports]
from nes_py.app.play_random import play_random  # pyright: ignore[reportMissingImports]
from nes_py.wrappers import JoypadSpace  # pyright: ignore[reportMissingImports]

from ..actions import COMPLEX_MOVEMENT, RIGHT_ONLY, SIMPLE_MOVEMENT

# a key mapping of action spaces to wrap with
_ACTION_SPACES = {
    "right": RIGHT_ONLY,
    "simple": SIMPLE_MOVEMENT,
    "complex": COMPLEX_MOVEMENT,
}


def _get_args():
    """Parse command line arguments and return them."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--env",
        "-e",
        type=str,
        default="SuperMarioBros-Vanilla",
        help="The name of the environment to play",
    )
    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        default="human",
        choices=["human", "random"],
        help="The execution mode for the emulation",
    )
    parser.add_argument(
        "--actionspace",
        "-a",
        type=str,
        default="nes",
        choices=["nes", "right", "simple", "complex"],
        help="the action space wrapper to use",
    )
    parser.add_argument(
        "--steps",
        "-s",
        type=int,
        default=500,
        help="The number of random steps to take.",
    )
    parser.add_argument(
        "--stages_1",
        "-S1",
        type=str,
        nargs="*",
        default=[],
        metavar="<world>-<stage>",
        help="The random stages to sample from for a Super Mario Bros. random stage env. (ex: --stages_1 1-1 1-2 2-4)",
    )
    parser.add_argument(
        "--stages_2",
        "-S2",
        type=str,
        nargs="*",
        default=[],
        metavar="<world>-<stage>",
        help="The random stages to sample from for a Super Mario Bros. 2 (Lost Levels) random stage env. (ex: --stages_2 1-1 1-2 2-4)",
    )
    parser.add_argument(
        "--list_envs",
        "-l",
        action="store_true",
        help="List all available Super Mario Bros. environments.",
    )
    # parse arguments and return them
    return parser.parse_args()


def parse_world_stage(s: str) -> tuple[int, int]:
    """Parse a string of the form '<world>-<stage>' into a tuple of integers.

    World range: 1-12, Stage range: 1-4.

    Args:
        s (str): the string from the command line to parse

    Returns:
        tuple[int, int]: the world and stage as a tuple of int
    """
    match = re.fullmatch(r"(\d|1[0-2])-([1-4])", s)
    if not match:
        raise ValueError(
            f"Invalid stage format: '{s}'. Expected format '<world>-<stage>' with world 1-12 and stage 1-4."
        )
    world, stage = map(int, match.groups())
    return (world, stage)


def main():
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args()

    # print all available environments if the list_envs flag is set
    if args.list_envs:
        available_envs = [
            e.id
            for e in gym.envs.registration.registry.values()  # pyright: ignore[reportAttributeAccessIssue]
            if "SuperMarioBros" in e.id
        ]
        for env_id in available_envs:
            print(env_id)
        return

    if (args.stages_1 or args.stages_2) and not args.env.startswith(
        "SuperMarioBrosRandomStages"
    ):
        print(
            "--stages_1, -S1, --stages_2, -S2 should only be specified for SuperMarioBrosRandomStages environments."
        )
        sys.exit(1)

    # if the environment is a random stage environment, create it with the specified stages
    if args.env.startswith("SuperMarioBrosRandomStages"):
        smb_only_stages = list(map(parse_world_stage, args.stages_1))
        lost_levels_only_stages = list(map(parse_world_stage, args.stages_2))
        env = gym.make(args.env, stages=(smb_only_stages, lost_levels_only_stages))
    else:
        env = gym.make(args.env)
    # wrap the environment with an action space if specified
    if args.actionspace != "nes":
        print(args.actionspace)
        # unwrap the actions list by key
        actions = _ACTION_SPACES[args.actionspace]
        # wrap the environment with the new action space
        env = JoypadSpace(env, actions)
    # play the environment with the given mode
    if args.mode == "human":
        play_human(env)
    else:
        play_random(env, args.steps)


# explicitly define the outward facing API of this module
__all__ = [main.__name__]  # pyright: ignore [reportUnsupportedDunderAll]
