from src.constants import UINT32_MAX

from src.types.FeatureSetting import FeatureSetting

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

settings: list[FeatureSetting] = [
    FeatureSetting(
        name = "start_at",
        active_condition = lambda x: x > 0,
        special_shorthand = "s"
    ),

    FeatureSetting(
        name = "end_at",
        active_condition = lambda x: x < UINT32_MAX,
        special_shorthand = "e",
        default = UINT32_MAX
    ),

    FeatureSetting(
        name = "every",
        active_condition = lambda x: x > 1,
        special_shorthand = "n",
        default = 1
    ),

    FeatureSetting(
        name = "pause",
        active_condition = lambda x: x > 0
    ),

    FeatureSetting(
        name = "active",
        active_condition = lambda x: x > 0
    ),

    FeatureSetting(
        name = "invert_pause",
        type = bool,
        active_condition = lambda x: x,
        default = False
    )
]

valid_setting_names = [setting.name for setting in settings]
