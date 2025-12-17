from dataclasses import dataclass, field

from src.types.Shortenable import Shortenable
from src.types.FeatureDefaultValues import FeatureDefaultValues
from src.types.FeatureParameter import FeatureParameter

from src.decl.filter_enable_settings_list import settings

import src.impl.feature_filters
from src.impl.filter_enable_settings import *

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

            # This is a leftover from when conditions were applied in the feature filter function.
            # However, it remains necessary for the sake of the shake filter,
            # Which NEEDS its start, pause and active values for the sinusoidal equation!
            # This has the terrible consequence of requiring every other filter needlessly take its condition settings,
            # Even if they don't use them, for the sake of interface uniformity.
            # Yikes!
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
