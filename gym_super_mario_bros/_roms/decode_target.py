"""A method to decode target values for a ROM stage environment."""


def decode_target(
    target: tuple[int, int] | None, lost_levels: bool
) -> tuple[int, int, int] | tuple[None, None, None]:
    """Return the target area for target world and target stage.

    Args:
        target (tuple[int, int] | None): the target world and stage to load
            as a tuple of (world, stage) or None if no target is specified
        lost_levels (bool): whether to use lost levels game

    Returns tuple[int, int, int] | tuple[None, None, None]:
        the area to target to load the target world and stage

    """
    # Type and value check the lost levels parameter
    if not isinstance(lost_levels, bool):
        raise TypeError(
            f"lost_levels argument must be of type: bool. Got: {type(lost_levels).__name__}"
        )
    # if there is no target, the world, stage, and area targets are all None
    if target is None:
        return None, None, None

    if not isinstance(target, (tuple, list)):
        raise TypeError(
            f"target argument must be of type tuple. Got: {type(target).__name__}."
        )

    if len(target) != 2:
        raise ValueError(
            f"target argument must contain exactly two integers. Got length: {len(target)}"
        )
    # unwrap the target world and stage
    target_world, target_stage = target

    # Type and value check the target world parameter
    if not isinstance(target_world, int):
        raise TypeError("target_world must be of type: int")
    if lost_levels:
        if not 1 <= target_world <= 12:
            raise ValueError("target_world must be in {1, ..., 12}")
    elif not 1 <= target_world <= 8:
        raise ValueError("target_world must be in {1, ..., 8}")

    # Type and value check the target level parameter
    if not isinstance(target_stage, int):
        raise TypeError("target_stage must be of type: int")
    if not 1 <= target_stage <= 4:
        raise ValueError("target_stage must be in {1, ..., 4}")

    # setup target area if target world and stage are specified
    target_area = target_stage
    # setup the target area depending on whether this is SMB 1 or 2
    if lost_levels:
        # setup the target area depending on the target world and stage
        if target_world in {1, 3}:
            if target_stage >= 2:
                target_area = target_area + 1
        elif target_world >= 5:
            # TODO: figure out why all worlds greater than 5 fail.
            # for now just raise a value error
            worlds = set(range(5, 12 + 1))
            msg = f"lost levels worlds {worlds} not supported"
            raise ValueError(msg)
    else:
        # setup the target area depending on the target world and stage
        if target_world in {1, 2, 4, 7}:
            if target_stage >= 2:
                target_area = target_area + 1

    return target_world, target_stage, target_area


# explicitly define the outward facing API of this module
__all__ = [decode_target.__name__]  # pyright: ignore [reportUnsupportedDunderAll]
