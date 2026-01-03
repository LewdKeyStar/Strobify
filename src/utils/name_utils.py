from src.types.Feature import Feature
from src.decl.feature_list import prioritized_features
from src.decl.filter_settings_list import enable_settings, video_settings

from os.path import splitext
from re import sub

def feature_section(
    args,
    feature: Feature
):

    if not getattr(args, feature.name): # Never None, either True or False
        return ''

    def conditional_setting(setting):

        setting_value = getattr(args, f'{feature.name}_{setting.name}')

        return (
            "_".join([f"{setting.name}", f"{setting_value}"])
            if setting.active_condition(setting_value)
            else ''
        )

    def param_print(param):
        param_value = getattr(args, f"{feature.name}_{param.name}")
        return "_".join([f"{param.shorthand}", f"{param_value}"+f"{param.unit}"])

    def print_feature_params():
        return "_".join([param_print(param) for param in feature.parameters])

    return "_".join([
        f"{feature.name}",
        print_feature_params(),
        *(
            [conditional_setting(enable_setting) for enable_setting in enable_settings]
            if feature.can_receive_enable_settings
            else []
        ),
        *(
            [conditional_setting(video_setting) for video_setting in video_settings]
            if feature.can_receive_video_settings
            else []
        )
    ])

def to_output_name(args):
    input_name, input_ext = splitext(args.input)

    return sub(
        "_" + "{2,}", # Replace generated chained underscores
        "_", # with single underscores.
        "_".join([
            input_name,
            "_".join([feature_section(args, feature) for feature in prioritized_features(args)])
        ]).rstrip("_") + input_ext
    )

def is_gif(input_name):
    return splitext(input_name)[1].lower() == ".gif"
