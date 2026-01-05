from argparse import BooleanOptionalAction

from src.decl.filter_settings_list import enable_settings, video_settings

from src.types.Feature import Feature

from src.utils.text_utils import to_kebab, abbreviate

def parser_compatible_type(setting_or_param):
    return (
        {
            "type": setting_or_param.type,
            "nargs": "?"
        }
        if setting_or_param.type != bool
        else {
            "action": BooleanOptionalAction
        }
    )

def register_feature_setting(
    parser,
    feature,
    setting
):

    parser.add_argument(
        f"-{feature.shorthand}{setting.shorthand}",
        f"--{to_kebab(feature.name)}-{to_kebab(setting.name)}",

        **parser_compatible_type(setting),

        # I don't like this default override scheme,
        # I don't like that the Feature has to return None
        # If it doesn't override the setting's "default default".

        default = (
            feature.default_setting_value(setting.name)
            if feature.default_setting_value(setting.name) is not None
            else setting.default
        )
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

    if feature.can_receive_enable_settings:

        for enable_setting in enable_settings:

            register_feature_setting(parser, feature, enable_setting)

    if feature.can_receive_video_settings:

        for video_setting in video_settings:

            register_feature_setting(parser, feature, video_setting)

    # Feature priority is different from other arguments :
    # It's not a setting on the filter itself,
    # And therefore is not borne by the Feature instance or registered in the settings list.

    parser.add_argument(
        f"-{feature.shorthand}r",
        f"--{to_kebab(feature.name)}-priority",
        type = int,
        nargs = "?",
        default = 0
    )

    for param in feature.parameters:

        # TODO : this could/should be unified with register_feature_setting()

        parser.add_argument(
            f"-{feature.shorthand}{param.shorthand}",
            f"--{to_kebab(feature.name)}-{to_kebab(param.name)}",
            **parser_compatible_type(param),
            default = param.default
        )
