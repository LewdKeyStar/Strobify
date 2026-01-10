from src.constants import UINT32_MAX

from src.types.settings.FeatureEnableSetting import FeatureEnableSetting
from src.types.settings.FeatureVideoSetting import FeatureVideoSetting

from src.types.settings.FeatureSettingRange import FeatureSettingRange

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

enable_settings: list[FeatureEnableSetting] = [
    FeatureEnableSetting(
        name = "start_at",
        include_in_filename = lambda x: x > 0,
        special_shorthand = "s"
    ),

    FeatureEnableSetting(
        name = "end_at",
        include_in_filename = lambda x: x < UINT32_MAX,
        special_shorthand = "e",
        default = UINT32_MAX
    ),

    FeatureEnableSetting(
        name = "every",
        include_in_filename = lambda x: x > 1,
        special_shorthand = "n",
        default = 1
    ),

    FeatureEnableSetting(
        name = "pause",
        include_in_filename = lambda x: x > 0
    ),

    FeatureEnableSetting(
        name = "active",
        include_in_filename = lambda x: x > 0
    ),

    FeatureEnableSetting(
        name = "invert_pause",
        type = bool,
        include_in_filename = lambda x: x,
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
        include_in_filename = lambda x: x > 0
    ),

    FeatureEnableSetting(
        name = "bpm_active_percent",
        type = float,
        include_in_filename = lambda x: x > 0
    )
]

video_settings: list[FeatureVideoSetting] = [
    FeatureVideoSetting(
        name = "alpha",
        special_shorthand = "l",
        type = float,

        requires_overlay = True,

        range = FeatureSettingRange(0.0, 1.0),
        default = 1.0,
        include_in_filename = lambda x: x < 1.0
    ),

    FeatureVideoSetting(
        name = "fade_in",
        include_in_filename = lambda x: x > 0,

        requires_overlay = True,

        enable_settings_used_in_setting_filter = ["start_at"],
        video_info_used_in_setting_filter = ["duration"]
    ),

    FeatureVideoSetting(
        name = "fade_out",
        include_in_filename = lambda x: x > 0,

        requires_overlay = True,

        enable_settings_used_in_setting_filter = ["end_at"],
        video_info_used_in_setting_filter = ["duration"]
    )
]

settings = enable_settings + video_settings

valid_setting_names = [setting.name for setting in settings]
valid_video_setting_names = [setting.name for setting in video_settings]
