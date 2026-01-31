from src.constants import UINT32_MAX, VALID_FADE_FUNCTIONS, DEFAULT_FADE_FUNCTION

from src.types.settings.FeatureEnableSetting import FeatureEnableSetting
from src.types.settings.FilterBearingFeatureVideoSetting import FilterBearingFeatureVideoSetting
from src.types.settings.FilterLessFeatureVideoSetting import FilterLessFeatureVideoSetting

from src.types.settings.FeatureSettingRange import FeatureSettingRange
from src.types.settings.FeatureSettingChoices import FeatureSettingChoices

from src.parser_namespace import runtime_value, is_enabled_at_runtime

from src.decl.utils.common_decl_utils import (
    percentage_format,
    relative_format,
    percentage_unit
)

from src.decl.utils.setting_decl_utils import (
    crop_corner_mode_enabled,
    crop_center_mode_enabled
)

from math import floor, modf

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

enable_settings: list[FeatureEnableSetting] = [
    FeatureEnableSetting(
        name = "start_at",
        include_in_filename = lambda feature_name, value: value > 0,
        special_shorthand = "s"
    ),

    FeatureEnableSetting(
        name = "end_at",
        include_in_filename = lambda feature_name, value: value < UINT32_MAX,
        special_shorthand = "e",
        default = UINT32_MAX
    ),

    FeatureEnableSetting(
        name = "every",
        include_in_filename = lambda feature_name, value: value > 1,
        special_shorthand = "n",
        default = 1
    ),

    FeatureEnableSetting(
        name = "pause",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    FeatureEnableSetting(
        name = "active",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    FeatureEnableSetting(
        name = "invert_pause",
        type = bool,
        include_in_filename = lambda feature_name, value: value,
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

        include_in_filename = lambda feature_name, value: value > 0,

        value_format = lambda feature_name, value: (
            int(value) if modf(value)[0] == 0
            else value
        )
    ),

    FeatureEnableSetting(
        name = "bpm_active_percent",
        type = float,
        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            runtime_value(feature_name, "bpm") > 0
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FeatureEnableSetting(
        name = "random",
        special_shorthand = "rand",
        type = bool,

        default = False,

        include_in_filename = lambda feature_name, value: value
    ),

    FeatureEnableSetting(
        name = "random_seed",
        special_shorthand = "seed",
        type = int,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(feature_name, "random")
        )
    ),

    FeatureEnableSetting(
        name = "random_probability",
        special_shorthand = "prob",
        type = float,

        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(feature_name, "random")
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    )
]

filter_bearing_video_settings: list[FilterBearingFeatureVideoSetting] = [
    FilterBearingFeatureVideoSetting(
        name = "alpha",
        special_shorthand = "l",
        type = float,
        unit = "%",

        requires_overlay = True,

        range = FeatureSettingRange(0.0, 1.0),
        default = 1.0,

        include_in_filename = lambda feature_name, value: value < 1.0,

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_in",
        include_in_filename = lambda feature_name, value: value > 0,

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
        include_in_filename = lambda feature_name, value: value > 0,

        requires_overlay = True,

        video_settings_used_in_setting_filter = ["fade_out_function"],

        enable_settings_used_in_setting_filter = ["end_at"],

        video_info_used_in_setting_filter = ["duration"]
    ),

    FilterBearingFeatureVideoSetting(
        name = "fade_cyclical",
        type = bool,

        requires_overlay = True,

        own_value_used_in_setting_filter = False,

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
        include_in_filename = lambda feature_name, value: value
    ),

    FilterBearingFeatureVideoSetting(
        name = "crop",
        special_shorthand = "cr",
        type = bool,

        requires_overlay = True,

        own_value_used_in_setting_filter = False,

        video_settings_used_in_setting_filter = [
            "crop_top", "crop_bottom", "crop_left", "crop_right",

            "crop_center_x", "crop_center_y",
            "crop_width", "crop_height",

            "crop_edge_fade",

            "crop_center_mode", "crop_relative_mode"
        ],

        video_info_used_in_setting_filter = ["resolution"],

        default = False,
        include_in_filename = lambda feature_name, value: value
    )
]

filterless_video_settings: list[FilterLessFeatureVideoSetting] = [
    FilterLessFeatureVideoSetting(
        name = "fade_in_function",
        type = str,
        choices = FeatureSettingChoices(VALID_FADE_FUNCTIONS),
        default = DEFAULT_FADE_FUNCTION,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_in")
            or
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical")
        )
    ),

    FilterLessFeatureVideoSetting(
        name = "fade_out_function",
        type = str,
        choices = FeatureSettingChoices(VALID_FADE_FUNCTIONS),
        default = DEFAULT_FADE_FUNCTION,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_out")
            or
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical")
        )
    ),

    # The number of frames in a non-synced cyclical fade between the in and out phase,
    # where the filter stays at full opacity.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_peak",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    # The number of frames separating two full in-out cycles of a non-synced cyclical fade.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_trough",
        include_in_filename = lambda feature_name, value: value > 0
    ),

    # Sync a cyclical fade a to a feature's active period.
    # If this is enabled, the fade in, fade out, peak and trough values are ignored.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync",
        type = bool,
        default = False,
        include_in_filename = lambda feature_name, value: value
    ),

    # These percentages are used instead, with peak and trough deduced from them.

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync_in_percent",
        type = float,
        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical_sync")
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FilterLessFeatureVideoSetting(
        name = "fade_cyclical_sync_out_percent",
        type = float,
        unit = "%",

        range = FeatureSettingRange(0.0, 1.0),
        default = 0.5,

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "fade_cyclical_sync")
        ),

        value_format = lambda feature_name, value: percentage_format(value)
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_top",
        special_shorthand = "crt",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_bottom",
        special_shorthand = "crb",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_left",
        special_shorthand = "crl",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_right",
        special_shorthand = "crr",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_corner_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_center_x",
        special_shorthand = "crx",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_center_y",
        special_shorthand = "cry",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_width",
        special_shorthand = "crw",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_height",
        special_shorthand = "crh",
        type = float,

        default = -1,

        unit = lambda feature_name, value: (
            percentage_unit(if_is_relative = f"{feature_name}_crop")
        ),

        value_format = lambda feature_name, value: (
            relative_format(value, feature_name = f"{feature_name}_crop")
        ),

        include_in_filename = crop_center_mode_enabled
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_edge_fade",
        special_shorthand = "cref",

        include_in_filename = lambda feature_name, value: (
            is_enabled_at_runtime(f"{feature_name}", "crop")
            and
            value > 0
        )
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_center_mode",
        special_shorthand = "crcm",
        type = bool,
        default = False,

        include_in_filename = False
    ),

    FilterLessFeatureVideoSetting(
        name = "crop_relative_mode",
        special_shorthand = "crrm",
        type = bool,
        default = False,

        include_in_filename = False
    ),
]

video_settings = filter_bearing_video_settings + filterless_video_settings
settings = enable_settings + video_settings

valid_setting_names = [setting.name for setting in settings]
valid_video_setting_filter_names = [setting.name for setting in filter_bearing_video_settings]
