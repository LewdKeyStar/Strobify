from src.types.Feature import Feature

from src.types.FeatureOptionFormatter import FeatureOptionFormatter

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

    def print_option(option):
        return str(FeatureOptionFormatter(args, feature, option))

    return "_".join([
        f"{feature.name}",
        *[
            print_option(param) for param in feature.parameters
        ],
        *(
            [print_option(enable_setting) for enable_setting in enable_settings]
            if feature.can_receive_enable_settings
            else []
        ),
        *(
            [print_option(video_setting) for video_setting in video_settings]
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
