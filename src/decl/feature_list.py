from src.constants import *

from src.types.Feature import Feature
from src.types.FeatureParameter import FeatureParameter
from src.types.FeatureDefaultValues import FeatureDefaultValues

# A declarative list of features for the script.
# Once a feature is declared here and implemented as its filter function,
# It will automatically become available.

features: list[Feature] = [
    Feature(
        name = "strobe",
        special_shorthand = "", # TODO : this is done for ease on the options,
        # but in practice it also means there is an option called "-" !
        # I'm not sure how valid that is

        default_values = FeatureDefaultValues(
            DEFAULT_STROBE_EVERY,
            DEFAULT_STROBE_PAUSE
        ),

        enable_default = True
    ),

    Feature(
        name = "rgb_shift",

        default_values = FeatureDefaultValues(
            DEFAULT_RGB_SHIFT_EVERY,
            DEFAULT_RGB_SHIFT_PAUSE
        ),

        parameters = [
            FeatureParameter("intensity", default = DEFAULT_RGB_SHIFT_INTENSITY, unit = "px")
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

        parameters = [
            FeatureParameter("factor", default = DEFAULT_ZOOM_FACTOR, type = float),
            FeatureParameter("center_x", special_shorthand = "x", unit = "px"),
            FeatureParameter("center_y", special_shorthand = "y", unit = "px"),
            FeatureParameter(
                "alpha",
                special_shorthand = "l",
                default = DEFAULT_ZOOM_ALPHA,
                type = float,
            )
        ],

        supplemental_arguments = ["resolution", "fps"]
    ),

    Feature(
        name = "frame_randomizer",

        parameters = [
            FeatureParameter("max_frames", special_shorthand = "max", default = DEFAULT_RANDOMIZER_MAX_FRAMES),
            FeatureParameter("seed", special_shorthand = "sd")
        ]
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
