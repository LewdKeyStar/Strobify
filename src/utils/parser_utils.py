from argparse import BooleanOptionalAction

from src.constants import UINT32_MAX

from src.types.Feature import Feature

from src.utils.text_utils import to_kebab, abbreviate

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

    parser.add_argument(
        f"-{feature.shorthand}s",
        f"--{to_kebab(feature.name)}-start-at",
        type = int,
        nargs = "?",
        default = 0
    )

    parser.add_argument(
        f"-{feature.shorthand}e",
        f"--{to_kebab(feature.name)}-end-at",
        type = int,
        nargs = "?",
        default = UINT32_MAX
    )

    parser.add_argument(
        f"-{feature.shorthand}n",
        f"--{to_kebab(feature.name)}-every",
        type = int,
        nargs = "?",
        default = feature.default_values.every
    )

    parser.add_argument(
        f"-{feature.shorthand}a",
        f"--{to_kebab(feature.name)}-active",
        type = int,
        nargs = "?",
        default = feature.default_values.pause
    )

    parser.add_argument(
        f"-{feature.shorthand}p",
        f"--{to_kebab(feature.name)}-pause",
        type = int,
        nargs = "?",
        default = feature.default_values.pause
    )

    parser.add_argument(
        f"-{feature.shorthand}ip",
        f"--{to_kebab(feature.name)}-invert-pause",
        default = False,
        action = BooleanOptionalAction
    )

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

        parser.add_argument(
            f"-{feature.shorthand}{param.shorthand}",
            f"--{to_kebab(feature.name)}-{to_kebab(param.name)}",
            type = param.type,
            nargs = "?",
            default = param.default
        )
