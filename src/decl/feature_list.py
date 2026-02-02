from src.constants import *
import src.constants

from src.types.features.Feature import Feature

from src.types.features.FeatureCombineMode import FeatureCombineMode

from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent
from src.types.parameters.FeatureParameterRange import FeatureParameterRange
from src.types.parameters.FeatureParameterChoices import FeatureParameterChoices

from src.types.settings.FeatureSettingDefaultValues import FeatureSettingDefaultValues

from src.parser_namespace import runtime_value, is_enabled_at_runtime

from src.decl.utils.common_decl_utils import (
    percentage_format,
    relative_format,
    percentage_unit
)

from src.decl.utils.feature_decl_utils import (
    eq_filter_parameters
)

# A declarative list of features for the script.
# Once a feature is declared here and implemented as its filter function,
# It will automatically become available.

features: list[Feature] = [

    Feature(
        name = "speed_change",

        has_audio_component = True,

        can_receive_enable_settings = False,
        can_receive_video_settings = False,

        combine_mode = FeatureCombineMode.REPLACE,

        parameters = (
            FeatureParameter(
                "factor",
                applicable_component = FeatureParameterApplicableComponent.BOTH_COMPONENTS,
                type = float,
                default = DEFAULT_SPEED_CHANGE_FACTOR
            ),
            FeatureParameter(
                "preserve_pitch",
                applicable_component = FeatureParameterApplicableComponent.AUDIO_COMPONENT_ONLY,
                type = bool,
                default = DEFAULT_SPEED_CHANGE_PRESERVE_PITCH
            ),
            FeatureParameter(
                "preserve_formants",
                applicable_component = FeatureParameterApplicableComponent.AUDIO_COMPONENT_ONLY,
                type = bool,
                default = DEFAULT_SPEED_CHANGE_PRESERVE_FORMANTS
            )
        )
    ),

    Feature(
        name = "fade_in",

        can_receive_enable_settings = False,
        can_receive_video_settings = False,

        combine_mode = FeatureCombineMode.REPLACE,

        parameters = (
            FeatureParameter(
                "duration",
                default = DEFAULT_FADE_DURATION
            ),
            FeatureParameter(
                "color",
                type = str,
                default = DEFAULT_FADE_COLOR
            )
        ),

        video_info_used_in_filter = ["duration"]
    ),

    Feature(
        name = "fade_out",

        can_receive_enable_settings = False,
        can_receive_video_settings = False,

        combine_mode = FeatureCombineMode.REPLACE,

        parameters = (
            FeatureParameter(
                "duration",
                default = DEFAULT_FADE_DURATION
            ),
            FeatureParameter(
                "color",
                type = str,
                default = DEFAULT_FADE_COLOR
            )
        ),

        video_info_used_in_filter = ["duration"]
    ),

    Feature(
        name = "afterimages",

        special_shorthand = "afi",

        combine_mode = FeatureCombineMode.PRE_MERGED,

        default_setting_values = FeatureSettingDefaultValues({
            "alpha": DEFAULT_AFTERIMAGES_ALPHA
        }),

        parameters = (
            FeatureParameter("start_white", special_shorthand = "w", type = bool, default = DEFAULT_AFTERIMAGES_START_WHITE),
            FeatureParameter("amount", special_shorthand = "m", default = DEFAULT_AFTERIMAGES_AMOUNT),
            FeatureParameter("delay", default = DEFAULT_AFTERIMAGES_DELAY)
        ),

        settings_used_in_filter = ["alpha"]

    ),

    Feature(
        name = "frame_randomizer",

        combine_mode = FeatureCombineMode.OVERLAY,

        parameters = [
            FeatureParameter("max_frames", special_shorthand = "max", default = DEFAULT_RANDOMIZER_MAX_FRAMES),
            FeatureParameter("seed", special_shorthand = "sd")
        ]
    ),

    Feature(
        name = "invert",

        default_setting_values = FeatureSettingDefaultValues({
            "every": DEFAULT_INVERT_EVERY,
            "pause": DEFAULT_INVERT_PAUSE
        }),

        parameters = [
            FeatureParameter("gamma", type = float, default = DEFAULT_INVERT_GAMMA)
        ]
    ),

    Feature(
        name = "darken",

        parameters = eq_filter_parameters("DARKEN")
    ),

    Feature(
        name = "lighten",

        parameters = eq_filter_parameters("LIGHTEN")
    ),

    Feature(
        name = "hue_saturation",

        parameters = [
            FeatureParameter(
                "hue",
                type = float,
                range = FeatureParameterRange(
                    MIN_HUE_SATURATION_HUE,
                    MAX_HUE_SATURATION_HUE
                )
            ),

            FeatureParameter(
                "saturation",
                special_shorthand = "sat",
                type = float,
                range = FeatureParameterRange(
                    MIN_HUE_SATURATION_SATURATION,
                    MAX_HUE_SATURATION_SATURATION
                ),
                default = DEFAULT_HUE_SATURATION_SATURATION
            ),

            FeatureParameter(
                "brightness",
                type = float,
                range = FeatureParameterRange(
                    MIN_HUE_SATURATION_BRIGHTNESS,
                    MAX_HUE_SATURATION_BRIGHTNESS
                ),
            )
        ]
    ),

    Feature(
        name = "rgb_shift",

        default_setting_values = FeatureSettingDefaultValues({
            "every": DEFAULT_RGB_SHIFT_EVERY,
            "pause": DEFAULT_RGB_SHIFT_PAUSE
        }),

        parameters = [
            FeatureParameter(
                "axis",
                special_shorthand = "ax",
                type = str,
                choices = FeatureParameterChoices(VALID_AXES),
                default = DEFAULT_RGB_SHIFT_AXIS
            ),
            FeatureParameter(
                "intensity",
                default = DEFAULT_RGB_SHIFT_INTENSITY,
                unit = "px"
            ),
            FeatureParameter(
                "colors",
                type = str,
                choices = FeatureParameterChoices(VALID_COLORS),
                default = DEFAULT_RGB_SHIFT_COLORS
            )
        ]
    ),

    Feature(
        name = "gaussian_blur",

        parameters = [
            FeatureParameter(
                "sigma",
                special_shorthand = "sig",
                type = float,
                default = DEFAULT_GAUSSIAN_BLUR_SIGMA
            ),
            FeatureParameter(
                "steps",
                special_shorthand = "stp",
                default = DEFAULT_GAUSSIAN_BLUR_STEPS
            )
        ]
    ),

    Feature(
        name = "shake",

        special_shorthand = "ss",

        parameters = [
            FeatureParameter(
                "axis",
                special_shorthand = "ax",
                type = str,
                choices = FeatureParameterChoices(VALID_AXES),
                default = DEFAULT_SHAKE_AXIS
            ),
            FeatureParameter(
                "amplitude",
                special_shorthand = "amp",
                default = DEFAULT_SHAKE_AMPLITUDE,
                unit = "px"
            ),
            FeatureParameter(
                "frequency",
                type = float,
                default = DEFAULT_SHAKE_FREQUENCY,
                unit = "hz"
            ),
            FeatureParameter("dampen", type = float, default = DEFAULT_SHAKE_DAMPEN),
            FeatureParameter("blur_radius", type = int, default = DEFAULT_SHAKE_BLUR)
        ],

        video_info_used_in_filter = ["fps"],
        settings_used_in_filter = ["start_at", "pause", "active"]
    ),

    Feature(
        name = "zoom",

        combine_mode = FeatureCombineMode.OVERLAY,

        default_setting_values = FeatureSettingDefaultValues({
            "alpha": DEFAULT_ZOOM_ALPHA
        }),

        parameters = [
            FeatureParameter(
                "factor",
                type = float,
                range = FeatureParameterRange(MIN_ZOOM_FACTOR, MAX_ZOOM_FACTOR),
                default = DEFAULT_ZOOM_FACTOR,
            ),
            FeatureParameter(
                "center_x",
                special_shorthand = "x",

                type = float,

                default = DEFAULT_ZOOM_CENTER_X,

                unit = lambda value: (
                    "" if runtime_value("zoom", "center_x") == DEFAULT_ZOOM_CENTER_X
                    else percentage_unit(if_is_relative = "zoom")
                ),

                renamed_values = {DEFAULT_ZOOM_CENTER_X: "center"},
                value_format = lambda value: relative_format(value, feature_name = "zoom")
            ),
            FeatureParameter(
                "center_y",
                special_shorthand = "y",

                type = float,

                default = DEFAULT_ZOOM_CENTER_Y,

                unit = lambda value: (
                    "" if runtime_value("zoom", "center_y") == DEFAULT_ZOOM_CENTER_Y
                    else percentage_unit(if_is_relative = "zoom")
                ),

                renamed_values = {DEFAULT_ZOOM_CENTER_Y: "center"},
                value_format = lambda value: relative_format(value, feature_name = "zoom")
            ),
            FeatureParameter(
                "relative_mode",
                type = bool,
                default = DEFAULT_ZOOM_RELATIVE_MODE,
                include_in_filename = False
            )
        ],

        video_info_used_in_filter = ["resolution", "fps"]
    )
]

# A util function that enforces the priority values given by users at call time.
# Used for the order of feature application, and the order of feature sections in the output name.

def prioritized_features():
    return sorted(
        features,
        key = lambda f: runtime_value(f"{f.name}", "priority"),
        reverse = True
    )
