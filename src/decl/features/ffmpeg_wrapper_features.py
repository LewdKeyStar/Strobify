from src.constants import *

from src.types.features.FFMPEGWrapperFeature import FFMPEGWrapperFeature

from src.types.features.FeatureCombineMode import FeatureCombineMode

from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent
from src.types.parameters.FeatureParameterRange import FeatureParameterRange
from src.types.parameters.FeatureParameterChoices import FeatureParameterChoices

from src.types.settings.FeatureSettingDefaultValues import FeatureSettingDefaultValues

from src.parser_namespace import runtime_value

from src.decl.utils.feature_decl_utils import (
    eq_filter_parameters
)

ffmpeg_wrapper_features: list[FFMPEGWrapperFeature] = [
    FFMPEGWrapperFeature(
        name = "fade_in",

        default_priority = HIGHEST_PRIORITY,

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

    FFMPEGWrapperFeature(
        name = "fade_out",

        default_priority = HIGHEST_PRIORITY,

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

    FFMPEGWrapperFeature(
        name = "frame_randomizer",

        combine_mode = FeatureCombineMode.OVERLAY,

        parameters = [
            FeatureParameter("max_frames", special_shorthand = "max", default = DEFAULT_RANDOMIZER_MAX_FRAMES),
            FeatureParameter("seed", special_shorthand = "sd")
        ]
    ),

    FFMPEGWrapperFeature(
        name = "darken",

        parameters = eq_filter_parameters("DARKEN")
    ),

    FFMPEGWrapperFeature(
        name = "lighten",

        parameters = eq_filter_parameters("LIGHTEN")
    ),

    FFMPEGWrapperFeature(
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

    FFMPEGWrapperFeature(
        name = "invert",

        default_setting_values = FeatureSettingDefaultValues({
            "every": DEFAULT_INVERT_EVERY,
            "pause": DEFAULT_INVERT_PAUSE
        }),

        parameters = [
            FeatureParameter("gamma", type = float, default = DEFAULT_INVERT_GAMMA)
        ]
    ),



    FFMPEGWrapperFeature(
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

    FFMPEGWrapperFeature(
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
]
