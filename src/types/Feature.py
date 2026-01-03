from dataclasses import dataclass, field

from src.types.abstract.Shortenable import Shortenable
from src.types.FeatureSettingDefaultValues import FeatureSettingDefaultValues
from src.types.FeatureParameter import FeatureParameter
from src.types.FeatureCombineMode import FeatureCombineMode

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

    has_audio_component: bool = False

    can_receive_enable_settings: bool = True
    can_receive_video_settings: bool = True

    default_setting_values: FeatureSettingDefaultValues = FeatureSettingDefaultValues()
    parameters: list[FeatureParameter] = field(default_factory=list)

    video_info_used_in_filter: list[str] = field(default_factory=list)
    settings_used_in_filter: list[str] = field(default_factory=list)

    combine_mode: FeatureCombineMode = FeatureCombineMode.MERGE

    def __post_init__(self):
        if (
            self.can_receive_video_settings == True
            and self.combine_mode == FeatureCombineMode.REPLACE
        ):
            raise ValueError("Replace-type feature declared with alpha parameter")

        if(
            self.can_receive_video_settings == False
            and self.combine_mode != FeatureCombineMode.REPLACE

        ):
            raise ValueError("Non-replace-type feature declared without alpha parameter")

        if (
            self.combine_mode == FeatureCombineMode.PRE_MERGED
            and "alpha" not in self.settings_used_in_filter
        ):
            raise ValueError("Pre-merged feature declared without access to alpha")

    def is_enabled(self, args):
        return getattr(args, self.name)

    @property
    def feature_filter(self):
        return getattr(src.impl.feature_filters, f"{self.name}_filter")

    @property
    def feature_filter_audio_component(self):
        return getattr(src.impl.feature_filters, f"{self.name}_filter_audio_component")

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

    def feature_filterstr(self, args, video_info, audio = False):

        component_function = (
            self.feature_filter
            if not audio
            else self.feature_filter_audio_component
        )

        return component_function(
            *[self.get_param_value(args, param_name) for param_name in self.parameter_names],

            *[self.get_setting_value(args, setting_name) for setting_name in self.settings_used_in_filter],

            *[getattr(video_info, required_info) for required_info in self.video_info_used_in_filter]
        )

    def apply_enable_settings(self, args, video_info):
        if not self.can_receive_enable_settings:
            return ''

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
                    self.get_setting_value(args, "pause"),
                    self.get_setting_value(args, "active")
                ) if self.get_setting_value(args, "bpm") == 0
                else sync_with_bpm(
                    self.get_setting_value(args, "bpm"),
                    self.get_setting_value(args, "bpm_active_percent"),
                    video_info.fps,
                    self.get_setting_value(args, "start_at"),
                    self.get_setting_value(args, "invert_pause")
                )
            )}'''
        )

    def should_skip_alpha(self, args):

        return (
            self.combine_mode in (FeatureCombineMode.REPLACE, FeatureCombineMode.PRE_MERGED)
            or
            self.combine_mode == FeatureCombineMode.MERGE and self.get_setting_value(args, "alpha") == 1.0
        )

    def feature_filterstr_without_alpha(self, args, video_info):
        return (
            self.feature_filterstr(
                args,
                video_info
            )
            +
            filter_option_separator(
                is_first_option = self.combine_mode == FeatureCombineMode.PRE_MERGED
            )
        )

    def feature_filterstr_with_alpha(self, args, video_info):

        alpha = self.get_setting_value(args, "alpha")

        return (
            split_filter(
                self.filterstr_before_feature,
                self.filterstr_before_alpha
            )
            + filter_input(self.filterstr_before_alpha)
            + self.feature_filterstr(args, video_info)
            + filter_output(self.filterstr_to_alpha)
            + alpha_filter(
                alpha,
                self.filterstr_before_feature,
                self.filterstr_to_alpha
            )
        )

    def video_component(self, args, video_info):

        return (
            (
                self.feature_filterstr_with_alpha(
                    args,
                    video_info
                )
                if not self.should_skip_alpha(args)
                else self.feature_filterstr_without_alpha(
                    args,
                    video_info
                )
            )
            +
            (
                self.apply_enable_settings(
                    args,
                    video_info
                )
                if self.can_receive_enable_settings
                else ''
            )
        )

    def audio_component(self, args, video_info):
        if not self.has_audio_component:
            return ''

        return self.feature_filterstr(args, video_info, audio = True)

    def __call__(self, args, video_info, seeking_audio_component = False):

        if not self.is_enabled(args):
            return ''

        return (
            self.video_component(args, video_info)
            if not seeking_audio_component
            else self.audio_component(args, video_info)
        )
