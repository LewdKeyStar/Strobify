from src.constants import UINT32_MAX, VALID_FADE_FUNCTIONS, DEFAULT_FADE_FUNCTION

from src.types.settings.FeatureEnableSetting import FeatureEnableSetting
from src.types.settings.FilterBearingFeatureVideoSetting import FilterBearingFeatureVideoSetting
from src.types.settings.FilterLessFeatureVideoSetting import FilterLessFeatureVideoSetting

from src.types.settings.FeatureSettingRange import FeatureSettingRange
from src.types.settings.FeatureSettingChoices import FeatureSettingChoices

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
        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda args, feature_name, value: (
            getattr(args, f"{feature_name}_bpm") > 0
        )
    )
]

filter_bearing_video_settings: list[FilterBearingFeatureVideoSetting] = [
    FilterBearingFeatureVideoSetting(
        name = "alpha",
        special_shorthand = "l",
        type = float,

        requires_overlay = True,

        range = FeatureSettingRange(0.0, 1.0),
        default = 1.0,
        include_in_filename = lambda x: x < 1.0
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_in",
        include_in_filename = lambda x: x > 0,

        requires_overlay = True,

        video_settings_used_in_setting_filter = ["fade_in_function"],

        enable_settings_used_in_setting_filter = [
            "start_at",
            "pause",
            "invert_pause"
        ],

        video_info_used_in_setting_filter = ["duration"]
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_out",
        include_in_filename = lambda x: x > 0,

        requires_overlay = True,

        video_settings_used_in_setting_filter = ["fade_out_function"],

        enable_settings_used_in_setting_filter = ["end_at"],

        video_info_used_in_setting_filter = ["duration"]
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_cyclical",
        type = bool,

        requires_overlay = True,

        video_settings_used_in_setting_filter = [
            "fade_in",
            "fade_out",
            "fade_in_function",
            "fade_out_function",
            "fade_cyclical_peak",
            "fade_cyclical_trough",
            "fade_cyclical_sync",
            "fade_cyclical_sync_in_percent",
            "fade_cyclical_sync_out_percent"
        ],

        enable_settings_used_in_setting_filter = [
            "start_at",
            "end_at",
            "pause",
            "active",
            "invert_pause"
        ],

        video_info_used_in_setting_filter = ["duration"],

        default = False,
        include_in_filename = lambda x: x
    )
]

filterless_video_settings: list[FilterLessFeatureVideoSetting] = [
    FilterLessFeatureVideoSetting(
        name = "fade_in_function",
        type = str,
        choices = FeatureSettingChoices(VALID_FADE_FUNCTIONS),
        default = DEFAULT_FADE_FUNCTION,

        include_in_filename = lambda args, feature_name, value: (
            getattr(args, f"{feature_name}_fade_in")
            or
            getattr(args, f"{feature_name}_fade_cyclical")
        )
    ),

    FilterLessFeatureVideoSetting(
        name = "fade_out_function",
        type = str,
        choices = FeatureSettingChoices(VALID_FADE_FUNCTIONS),
        default = DEFAULT_FADE_FUNCTION,

        include_in_filename = lambda args, feature_name, value: (
            getattr(args, f"{feature_name}_fade_out")
            or
            getattr(args, f"{feature_name}_fade_cyclical")
        )
    ),

    # The number of frames in a non-synced cyclical fade between the in and out phase,
    # where the filter stays at full opacity.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_peak",
        include_in_filename = lambda x: x > 0
    ),

    # The number of frames separating two full in-out cycles of a non-synced cyclical fade.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_trough",
        include_in_filename = lambda x: x > 0
    ),

    # Sync a cyclical fade a to a feature's active period.
    # If this is enabled, the fade in, fade out, peak and trough values are ignored.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync",
        type = bool,
        default = False,
        include_in_filename = lambda x: x
    ),

    # These percentages are used instead, with peak and trough deduced from them.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync_in_percent",
        type = float,
        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,
        include_in_filename = lambda args, feature_name, value: (
            getattr(args, f"{feature_name}_fade_cyclical_sync")
        )
    ),

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync_out_percent",
        type = float,
        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,
        include_in_filename = lambda args, feature_name, value: (
            getattr(args, f"{feature_name}_fade_cyclical_sync")
        )
    )
]

video_settings = filter_bearing_video_settings + filterless_video_settings
settings = enable_settings + video_settings

valid_setting_names = [setting.name for setting in settings]
valid_video_setting_filter_names = [setting.name for setting in filter_bearing_video_settings]
