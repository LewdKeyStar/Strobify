from dataclasses import dataclass, field

from src.types.abstract.Shortenable import Shortenable
from src.types.FeatureSettingDefaultValues import FeatureSettingDefaultValues
from src.types.FeatureParameter import FeatureParameter

from src.decl.filter_settings_list import enable_settings, valid_setting_names

import src.impl.feature_filters
from src.impl.misc_filters import (
    split_filter,
    alpha_filter
)
from src.utils.filter_utils import (
    filter_input,
    filter_output,
    filter_option_separator
)

from src.impl.filter_enable_settings import *

@dataclass
class Feature(Shortenable):
    name: str
    enable_default: bool = False

    default_setting_values: FeatureSettingDefaultValues = FeatureSettingDefaultValues()
    parameters: list[FeatureParameter] = field(default_factory=list)

    video_info_used_in_filter: list[str] = field(default_factory=list)
    settings_used_in_filter: list[str] = field(default_factory=list)

    combine_mode: str = "merge"

    @property
    def feature_filter(self):
        return getattr(src.impl.feature_filters, f"{self.name}_filter")

    @property
    def parameter_names(self):
        return [param.name for param in self.parameters]

    def default_setting_value(self, setting_name):
        return (
            self.default_setting_values[setting_name]
            if setting_name in self.default_setting_values
            else None # Ouch! I don't like this!
            # But the alternative is to run a find() on the settings list...
        )

    def get_param_value(self, args, param_name):
        if param_name not in self.parameter_names:
            raise ValueError("Invalid parameter :", param_name)

        return getattr(args, f"{self.name}_{param_name}")

    def get_setting_value(self, args, setting_name):
        if setting_name not in valid_setting_names:
            raise ValueError("Invalid setting :", setting_name)

        return getattr(args, f"{self.name}_{setting_name}")

    # I don't particularly like having ffmpeg-related strings in this submodule.
    # They're not *technically* part of the FFMPEG filtergraph, but...still.
    # It's out of place.

    @property
    def filterstr_before_feature(self):
        return f"before_{self.name}"

    @property
    def filterstr_before_alpha(self):
        return f"{self.name}_before_alpha"

    @property
    def filterstr_to_alpha(self):
        return f"{self.name}_to_alpha"

    def enable_conditions(self, args):
        return (
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

    # TODO : maybe we'll generalize this too.

    def apply_alpha(self, args, feature_filterstr):

        alpha = self.get_setting_value(args, "alpha")

        # This is a veeeery slight difference in result.
        # It does make processing faster, though.
        if alpha == 1.0 and self.combine_mode == "merge":
            return feature_filterstr + filter_option_separator()

        return (
            split_filter(
                self.filterstr_before_feature,
                self.filterstr_before_alpha
            )
            + filter_input(self.filterstr_before_alpha)
            + feature_filterstr
            + filter_output(self.filterstr_to_alpha)
            + alpha_filter(
                alpha,
                self.filterstr_before_feature,
                self.filterstr_to_alpha
            )
        )

    def __call__(self, args, video_info):

        if not getattr(args, self.name):
            return ''

        feature_filterstr = self.feature_filter(
            *[self.get_param_value(args, param_name) for param_name in self.parameter_names],

            *[self.get_setting_value(args, setting_name) for setting_name in self.settings_used_in_filter],

            *[getattr(video_info, required_info) for required_info in self.video_info_used_in_filter]
        )

        return (
            self.apply_alpha(
                args,
                feature_filterstr
            )
            +
            self.enable_conditions(
                args
            )
        )
