from argparse import BooleanOptionalAction

from src.constants import UINT32_MAX

def register_feature(
    feature_name,
    feature_specific_params: list[str] = [],
    feature_specific_param_properties: dict[str, dict[str, any]] = {},

    *,

    parser,

    default_values,

    shorthand_prefix = None,
    enable_default = False
):

    def to_kebab(snake):
        return snake.replace("_", "-")

    def abbreviate(snake_name):
        return "".join([word[0] for word in snake_name.split("_")])

    def prefix():
        return (
            shorthand_prefix
            if shorthand_prefix is not None
            else abbreviate(feature_name)
        )

    def param_info(param, info, default):
        return (
            feature_specific_param_properties[param][info]
            if (
                feature_specific_param_properties is not None
                and param in feature_specific_param_properties
                and info in feature_specific_param_properties[param]
            )
            else default
        )

    def param_shorthand(param):
        return param_info(param, "shorthand", abbreviate(param))

    def param_type(param):
        return param_info(param, "type", int)

    def param_default(param):
        return param_info(param, "default", 0)

    parser.add_argument(
        f"-{prefix()}",
        f"--{to_kebab(feature_name)}",
        default = enable_default,
        action = BooleanOptionalAction
    )

    parser.add_argument(
        f"-{prefix()}s",
        f"--{to_kebab(feature_name)}-start-at",
        type = int,
        nargs = "?",
        default = 0
    )

    parser.add_argument(
        f"-{prefix()}e",
        f"--{to_kebab(feature_name)}-end-at",
        type = int,
        nargs = "?",
        default = UINT32_MAX
    )

    parser.add_argument(
        f"-{prefix()}n",
        f"--{to_kebab(feature_name)}-every",
        type = int,
        nargs = "?",
        default = default_values["every"]
    )

    parser.add_argument(
        f"-{prefix()}a",
        f"--{to_kebab(feature_name)}-active",
        type = int,
        nargs = "?",
        default = default_values["pause"]
    )

    parser.add_argument(
        f"-{prefix()}p",
        f"--{to_kebab(feature_name)}-pause",
        type = int,
        nargs = "?",
        default = default_values["pause"]
    )

    parser.add_argument(
        f"-{prefix()}ip",
        f"--{to_kebab(feature_name)}-invert-pause",
        type = int,
        nargs = "?",
        default = False
    )

    for param in feature_specific_params:

        parser.add_argument(
            f"-{prefix()}{param_shorthand(param)}",
            f"--{to_kebab(feature_name)}-{to_kebab(param)}",
            type = param_type(param),
            nargs = "?",
            default = param_default(param)
        )
