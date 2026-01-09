from src.constants import *
import src.constants

from src.types.Feature import Feature

from src.types.FeatureCombineMode import FeatureCombineMode

from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterRange import FeatureParameterRange
from src.types.parameters.FeatureParameterChoices import FeatureParameterChoices

from src.types.settings.FeatureSettingDefaultValues import FeatureSettingDefaultValues

# A declarative list of features for the script.
# Once a feature is declared here and implemented as its filter function,
# It will automatically become available.

def eq_filter_parameters(suffix):

    param_name_list = [
        "contrast",
        "brightness",
        "saturation",
        "gamma",
        "gamma_r",
        "gamma_g",
        "gamma_b",
        "gamma_weight"
    ]

    return [
        FeatureParameter(
            name,
            special_shorthand = "sat" if name == "saturation" else None, # avoid conflict with start_at
            type = float,
            range = FeatureParameterRange(
                getattr(src.constants, f"MIN_EQ_{name.upper()}_{suffix}"),
                getattr(src.constants, f"MAX_EQ_{name.upper()}_{suffix}")
            ),
            default = getattr(src.constants, f"DEFAULT_EQ_{name.upper()}_{suffix}")
        )

        for name in param_name_list
    ]

features: list[Feature] = [

    Feature(
        name = "speed_change",

        has_audio_component = True,

        can_receive_enable_settings = False,
        can_receive_video_settings = False,

        combine_mode = FeatureCombineMode.REPLACE,

        parameters = (
            FeatureParameter("factor", type = float, default = DEFAULT_SPEED_CHANGE_FACTOR),
            FeatureParameter("preserve_pitch", type = bool, default = DEFAULT_SPEED_CHANGE_PRESERVE_PITCH),
            FeatureParameter("preserve_formants", type = bool, default = DEFAULT_SPEED_CHANGE_PRESERVE_FORMANTS)
        )
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
                range = FeatureParameterRange(MIN_HUE_SATURATION_HUE, MAX_HUE_SATURATION_HUE)
            ),

            FeatureParameter(
                "saturation",
                special_shorthand = "sat",
                type = float,
                range = FeatureParameterRange(MIN_HUE_SATURATION_SATURATION, MAX_HUE_SATURATION_SATURATION),
                default = DEFAULT_HUE_SATURATION_SATURATION
            ),

            FeatureParameter(
                "brightness",
                type = float,
                range = FeatureParameterRange(MIN_HUE_SATURATION_BRIGHTNESS, MAX_HUE_SATURATION_BRIGHTNESS),
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
                unit = "px",
                default = DEFAULT_ZOOM_CENTER_X
            ),
            FeatureParameter(
                "center_y",
                special_shorthand = "y",
                type = float,
                unit = "px",
                default = DEFAULT_ZOOM_CENTER_Y
            ),
            FeatureParameter(
                "relative_mode",
                type = bool,
                default = DEFAULT_ZOOM_RELATIVE_MODE
            )
        ],

        video_info_used_in_filter = ["resolution", "fps"]
    )
]

# A util function that enforces the priority values given by users at call time.
# Used for the order of feature application, and the order of feature sections in the output name.

def prioritized_features(args):
    return sorted(
        features,
        key = lambda f: getattr(args, f"{f.name}_priority"),
        reverse = True
    )
