from src.constants import *

from src.types.Feature import Feature
from src.types.FeatureParameter import FeatureParameter
from src.types.FeatureSettingDefaultValues import FeatureSettingDefaultValues

# A declarative list of features for the script.
# Once a feature is declared here and implemented as its filter function,
# It will automatically become available.

features: list[Feature] = [
    Feature(
        name = "frame_randomizer",

        combine_mode = "overlay",

        parameters = [
            FeatureParameter("max_frames", special_shorthand = "max", default = DEFAULT_RANDOMIZER_MAX_FRAMES),
            FeatureParameter("seed", special_shorthand = "sd")
        ]
    ),

    Feature(
        name = "strobe",
        special_shorthand = "", # TODO : this is done for ease on the options,
        # but in practice it also means there is an option called "-" !
        # I'm not sure how valid that is

        default_setting_values = FeatureSettingDefaultValues({
            "every": DEFAULT_STROBE_EVERY,
            "pause": DEFAULT_STROBE_PAUSE
        }),

        parameters = [
            FeatureParameter("gamma", type = float, default = DEFAULT_STROBE_GAMMA)
        ],

        enable_default = True
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

        supplemental_arguments = ["fps"]
    ),

    Feature(
        name = "zoom",

        combine_mode = "overlay",

        default_setting_values = FeatureSettingDefaultValues({
            "alpha": DEFAULT_ZOOM_ALPHA
        }),

        parameters = [
            FeatureParameter("factor", default = DEFAULT_ZOOM_FACTOR, type = float),
            FeatureParameter("center_x", special_shorthand = "x", unit = "px"),
            FeatureParameter("center_y", special_shorthand = "y", unit = "px")
        ],

        supplemental_arguments = ["resolution", "fps"]
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
