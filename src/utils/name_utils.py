from src.types.Feature import Feature
from src.decl.feature_list import prioritized_features
from src.decl.filter_settings_list import enable_settings, video_settings

from os.path import splitext
from re import sub

from inspect import signature

def feature_section(
    args,
    feature: Feature
):

    if not getattr(args, feature.name): # Never None, either True or False
        return ''

    def conditional_setting(setting):

        setting_value = getattr(args, f'{feature.name}_{setting.name}')

        include_in_filename = (
            setting.include_in_filename(setting_value)
            if len(signature(setting.include_in_filename).parameters) == 1 # YEOUCH!
            else setting.include_in_filename(args, feature.name, setting_value)
            # Surely we can hide this bit of ugliness somewhere else...
        )

        return (
            "_".join([f"{setting.name}", f"{setting_value}"])
            if include_in_filename
            else ''
        )

    def param_print(param):
        if not param.include_in_filename: # Unlike settings, this is just a yes or no flag.
            return ""

        param_value = param.get_named_value_for_feature(args, feature.name)
        param_unit = param.unit if not callable(param.unit) else param.unit(args)
        return "_".join([f"{param.shorthand}", f"{param_value}"+f"{param_unit}"])

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
