from src.constants import *

from src.feature import (
    Feature,
    FeatureParameter,
    FeatureDefaultValues
)

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
        name = "zoom",

        parameters = [
            FeatureParameter("factor", default = DEFAULT_ZOOM_FACTOR),
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
    )
]
