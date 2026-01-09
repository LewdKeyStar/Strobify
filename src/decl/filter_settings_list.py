from src.constants import UINT32_MAX

from src.types.settings.FeatureEnableSetting import FeatureEnableSetting
from src.types.settings.FeatureVideoSetting import FeatureVideoSetting

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

enable_settings: list[FeatureEnableSetting] = [
    FeatureEnableSetting(
        name = "start_at",
        active_condition = lambda x: x > 0,
        special_shorthand = "s"
    ),

    FeatureEnableSetting(
        name = "end_at",
        active_condition = lambda x: x < UINT32_MAX,
        special_shorthand = "e",
        default = UINT32_MAX
    ),

    FeatureEnableSetting(
        name = "every",
        active_condition = lambda x: x > 1,
        special_shorthand = "n",
        default = 1
    ),

    FeatureEnableSetting(
        name = "pause",
        active_condition = lambda x: x > 0
    ),

    FeatureEnableSetting(
        name = "active",
        active_condition = lambda x: x > 0
    ),

    FeatureEnableSetting(
        name = "invert_pause",
        type = bool,
        active_condition = lambda x: x,
        default = False
    ),

    # If a syncing BPM is provided, the "pause" and "active" options are ignored.

    # FIXME : This is not very clean ; ideally it should be impossible to provided them together.
    # However argparse has deprecated nesting argument groups, such that something like :
    # [[-p -a] | [-bpm -bap]]
    # Cannot be done.
    # The only alternative would be subcommands :
    # fascinate [pause-mode [-p -a] | bpm-mode [-bpm -bap]]
    # which is not feasible since the same "subcommand" could be invoked multiple times, one for each filter...

    FeatureEnableSetting(
        name = "bpm",
        special_shorthand = "bpm",
        type = float,
        active_condition = lambda x: x > 0
    ),

    FeatureEnableSetting(
        name = "bpm_active_percent",
        type = float,
        active_condition = lambda x: x > 0
    )
]

video_settings: list[FeatureVideoSetting] = [
    FeatureVideoSetting(
        name = "alpha",
        requires_formatting = True,
        type = float,
        special_shorthand = "l",
        default = 1.0
    )
]

settings = enable_settings + video_settings

valid_setting_names = [setting.name for setting in settings]
