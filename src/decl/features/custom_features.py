from src.constants import *

from src.types.features.CustomFeature import CustomFeature

from src.types.features.FeatureCombineMode import FeatureCombineMode

from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent
from src.types.parameters.FeatureParameterRange import FeatureParameterRange
from src.types.parameters.FeatureParameterChoices import FeatureParameterChoices

from src.types.settings.FeatureSettingDefaultValues import FeatureSettingDefaultValues

from src.parser_namespace import runtime_value

from src.decl.utils.common_decl_utils import (
    relative_format,
    percentage_unit
)

custom_features: list[CustomFeature] = [
    CustomFeature(
        name = "speed_change",

        default_priority = HIGHEST_PRIORITY,

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

    CustomFeature(
        name = "afterimages",

        default_priority = HIGHER_PRIORITY,

        special_shorthand = "afi",

        combine_mode = FeatureCombineMode.PRE_MERGED,

        default_setting_values = FeatureSettingDefaultValues({
            "alpha": DEFAULT_AFTERIMAGES_ALPHA
        }),

        parameters = (
            FeatureParameter("amount", special_shorthand = "m", default = DEFAULT_AFTERIMAGES_AMOUNT),
            FeatureParameter("delay", default = DEFAULT_AFTERIMAGES_DELAY),
            FeatureParameter(
                "start_white",
                special_shorthand = "w",
                type = bool,
                default = DEFAULT_AFTERIMAGES_START_WHITE
            ),
            FeatureParameter(
                "extend",
                special_shorthand = "x",
                type = bool,
                default = DEFAULT_AFTERIMAGES_EXTEND
            )
        ),

        settings_used_in_filter = ["alpha"]

    ),

    CustomFeature(
        name = "shake",

        default_priority = LOWEST_PRIORITY,

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

    CustomFeature(
        name = "zoom",

        default_priority = LOWEST_PRIORITY,

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
