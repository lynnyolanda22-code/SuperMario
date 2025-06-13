"""Common enums used throughout the code base."""

from enum import Enum


class SuperMarioBrosROMMode(Enum):
    """An enumaretion of the different ROM mode available for each game."""

    VANILLA = "vanilla"
    """The basic game graphics."""
    DOWNSAMPLE = "downsample"
    PIXEL = "pixel"
    RECTANGLE = "rectangle"

    @classmethod
    def lost_levels_modes(cls):
        """Returns all the ROM modes suitable for Super Mario Bros. 2 (Lost Levels)."""
        return [cls.VANILLA, cls.DOWNSAMPLE]

    @classmethod
    def lost_levels_values(cls):
        """Returns all the ROM modes suitable for Super Mario Bros. 2 (Lost Levels) as a string."""
        return [cls.VANILLA.value, cls.DOWNSAMPLE.value]

    @classmethod
    def capitalized_lost_levels_values(cls):
        """Returns all the ROM modes suitable for Super Mario Bros. 2 (Lost Levels) as a string with a capitalized letter.

        This is used in order to name environments.
        """
        return [cls.VANILLA.value.capitalize(), cls.DOWNSAMPLE.value.capitalize()]

    @classmethod
    def rom_modes_values(cls):
        """Returns all the ROM modes suitable for Super Mario Bros. as a string."""
        return [
            cls.VANILLA.value,
            cls.DOWNSAMPLE.value,
            cls.PIXEL.value,
            cls.RECTANGLE.value,
        ]

    @classmethod
    def capitalized_rom_modes(cls):
        """Returns all the ROM modes suitable for Super Mario Bros. as a string with a capitalized letter.

        This is used in order to name environments.
        """
        return [
            cls.VANILLA.value.capitalize(),
            cls.DOWNSAMPLE.value.capitalize(),
            cls.PIXEL.value.capitalize(),
            cls.RECTANGLE.value.capitalize(),
        ]

    @property
    def suitable_for_lost_levels(self):
        """Check if a ROM mode is compatible with Super Mario Bros. 2 (Lost Levels)."""
        return self in {self.VANILLA, self.DOWNSAMPLE}


class SuperMarioBrosRandomMode(Enum):
    """An enumeration of the different modes of selection for the random stages environment."""

    SMB_ONLY = "SmbOnly"
    """Only the stages from the original Super Mario Bros. game."""
    LOST_LEVELS_ONLY = "LostLevelsOnly"
    """Only the stages from Super Mario Bros. 2 (Lost Levels)."""
    BOTH = "Both"
    """Randomly select stages from both Super Mario Bros. and Super Mario Bros. 2 (Lost Levels)."""

    @property
    def has_smb(self):
        """Check if the random mode can use levels from Super Mario Bros."""
        return self in {
            SuperMarioBrosRandomMode.SMB_ONLY,
            SuperMarioBrosRandomMode.BOTH,
        }

    @property
    def has_lost_levels(self):
        """Check if the random mode can use levels from Super Mario Bros. 2 (Lost Levels)."""
        return self in {
            SuperMarioBrosRandomMode.LOST_LEVELS_ONLY,
            SuperMarioBrosRandomMode.BOTH,
        }


# explicitly define the outward facing API of this module
__all__ = [
    SuperMarioBrosROMMode.__name__,
    SuperMarioBrosRandomMode.__name__,
]  # pyright: ignore [reportUnsupportedDunderAll]
