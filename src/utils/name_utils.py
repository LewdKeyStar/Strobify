from src.types.features.Feature import Feature

from src.types.parameters.FeatureParameterFormatter import FeatureParameterFormatter
from src.types.settings.FeatureSettingFormatter import FeatureSettingFormatter

from src.parser_namespace import runtime_value

from src.decl.feature_list import prioritized_features
from src.decl.filter_settings_list import enable_settings, video_settings

from os.path import splitext
from re import sub

def feature_section(feature: Feature):

    if not feature.is_enabled: # Feature enable flag
        return ''

    def print_param(param):
        return str(FeatureParameterFormatter(feature, param))

    def print_setting(setting):
        return str(FeatureSettingFormatter(feature, setting))

    return "_".join([
        f"{feature.name}",
        *[
            print_param(param) for param in feature.parameters
        ],
        *(
            [print_setting(enable_setting) for enable_setting in enable_settings]
            if feature.can_receive_enable_settings
            else []
        ),
        *(
            [print_setting(video_setting) for video_setting in video_settings]
            if feature.can_receive_video_settings
            else []
        )
    ])

def to_output_name(input_path):
    input_name, input_ext = splitext(input_path)

    return sub(
        "_" + "{2,}", # Replace generated chained underscores
        "_", # with single underscores.
        "_".join([
            input_name,
            "_".join([feature_section(feature) for feature in prioritized_features()])
        ]).rstrip("_") + input_ext
    )

def is_gif(input_name):
    return splitext(input_name)[1].lower() == ".gif"
