from argparse import BooleanOptionalAction

from src.decl.filter_settings_list import enable_settings, video_settings, meta_settings

from src.types.features.Feature import Feature
from src.types.settings.FeatureSetting import FeatureSetting

from src.utils.text_utils import to_kebab, abbreviate

def parser_compatible_type(option):
    return (
        {
            "type": option.type,
            "nargs": "?"
        }
        if option.type != bool
        else {
            "action": BooleanOptionalAction
        }
    )

def register_feature_option(
    parser,
    feature,
    option
):

    parser.add_argument(
        f"-{feature.shorthand}{option.shorthand}",
        f"--{to_kebab(feature.name)}-{to_kebab(option.name)}",

        **parser_compatible_type(option),

        choices = option.choices,

        default = (
            # I don't like this default override scheme,
            # I don't like that the Feature has to return None
            # If it doesn't override the setting's "default default".
            (
                feature.default_setting_value(option.name)
                if feature.default_setting_value(option.name) is not None
                else option.default
            )
            if isinstance(option, FeatureSetting)
            else option.default
        ),

        help = option.help
    )

def register_feature(
    parser,
    feature: Feature
):

    parser.add_argument(
        f"-{feature.shorthand}",
        f"--{to_kebab(feature.name)}",
        default = feature.enable_default,
        action = BooleanOptionalAction
    )

    for meta_setting in meta_settings:

        register_feature_option(parser, feature, meta_setting)

    if feature.can_receive_enable_settings:

        for enable_setting in enable_settings:

            register_feature_option(parser, feature, enable_setting)

    if feature.can_receive_video_settings:

        for video_setting in video_settings:

            register_feature_option(parser, feature, video_setting)

    for param in feature.parameters:

        register_feature_option(parser, feature, param)
