from src.types.Feature import Feature
from src.decl.feature_list import prioritized_features
from src.decl.filter_enable_settings_list import settings

from os.path import splitext
from re import sub

def feature_section(
    args,
    feature: Feature
):

    if not getattr(args, feature.name): # Never None, either True or False
        return ''

    def conditional_setting(setting, active_condition):

        setting_value = getattr(args, f'{feature.name}_{setting}')

        return (
            "_".join([f"{setting}", f"{setting_value}"])
            if active_condition(setting_value)
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
        *[conditional_setting(setting, active_condition) for (setting, active_condition) in settings.items()]
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
