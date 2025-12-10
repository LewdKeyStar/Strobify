from abc import ABC
from dataclasses import dataclass, field

from src.text_utils import abbreviate

from src.filter_enable_settings_list import settings

import src.filters

@dataclass
class FeatureDefaultValues:
    every: int = 1
    pause: int = 0

@dataclass(kw_only = True)
class Shortenable(ABC):
    special_shorthand: str = None

    @property
    def shorthand(self):
        return (
            self.special_shorthand
            if self.special_shorthand is not None
            else abbreviate(self.name)
        )

@dataclass
class FeatureParameter(Shortenable):
    name: str
    default: any = 0
    unit: str = ""
    type: any = int

@dataclass
class Feature(Shortenable):
    name: str
    enable_default: bool = False

    default_values: FeatureDefaultValues = FeatureDefaultValues()
    parameters: list[FeatureParameter] = field(default_factory=list)

    supplemental_arguments: list[str] = field(default_factory=list)

    def __call__(self, args, *supp_args):

        if not getattr(args, self.name):
            return ''

        return getattr(src.filters, f"{self.name}_filter")(
            *supp_args,

            *[getattr(args, f"{self.name}_{param.name}") for param in self.parameters],

            *[getattr(args, f"{self.name}_{setting}") for setting in settings.keys()]
        )
