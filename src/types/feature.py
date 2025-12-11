from abc import ABC
from dataclasses import dataclass, field

from src.utils.text_utils import abbreviate

from src.decl.filter_enable_settings_list import settings

import src.impl.feature_filters
from src.impl.filter_enable_settings import *

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

    @property
    def parameter_names(self):
        return [param.name for param in self.parameters]

    def get_param_value(self, args, param_name):
        if param_name not in self.parameter_names:
            raise ValueError("Invalid parameter :", param_name)
            
        return getattr(args, f"{self.name}_{param_name}")

    def get_setting_value(self, args, setting_name):
        if setting_name not in settings.keys():
            raise ValueError("Invalid setting :", setting_name)

        return getattr(args, f"{self.name}_{setting_name}")

    def __call__(self, args, *supp_args):

        if not getattr(args, self.name):
            return ''

        return getattr(src.impl.feature_filters, f"{self.name}_filter")(
            *supp_args,

            *[self.get_param_value(args, param_name) for param_name in self.parameter_names],

            *[self.get_setting_value(args, setting_name) for setting_name in settings.keys()]
        ) + (
            f'''enable={join_and(
                enable_from(self.get_setting_value(args, "start_at")),
                enable_until(self.get_setting_value(args, "end_at")),
                enable_every(
                    self.get_setting_value(args, "start_at"),
                    self.get_setting_value(args, "every")
                ),
                enable_at_interval(
                    self.get_setting_value(args, "start_at"),
                    self.get_setting_value(args, "invert_pause"),
                    pause_interval = self.get_setting_value(args, "pause"),
                    active_interval = self.get_setting_value(args, "active")
                )
            )}'''
        )
