from dataclasses import dataclass, field

from src.types.abstract.Shortenable import Shortenable

from src.types.settings.FeatureSettingDefaultValues import FeatureSettingDefaultValues

from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent
from src.types.parameters.FeatureParameter import FeatureParameter
from src.types.FeatureCombineMode import FeatureCombineMode

from src.decl.filter_settings_list import (
    settings,
    enable_settings,
    video_settings,
    filter_bearing_video_settings,
    filterless_video_settings,
    valid_setting_names,
    valid_video_setting_filter_names
)

import src.impl.feature_filters
import src.impl.filter_video_settings
from src.impl.filter_enable_settings import * # TODO : automate those too through the same kind of list iteration

from src.impl.misc_filters import (
    split_filter,
    overlay_filter
)
from src.utils.filter_utils import (
    filter_input,
    filter_output,
    filter_option_separator,
    filter_separator
)

from src.impl.utils.enable_settings_utils import (
    bpm_synced_intervals
)

from src.utils.misc_utils import array_find

@dataclass
class Feature(Shortenable):
    name: str

    enable_default: bool = False # Now that the invert feature is no longer enabled by default, this goes unused.

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

    def get_param_value(self, args, param_name):
        if param_name not in self.parameter_names:
            raise ValueError("Invalid parameter :", param_name)

        return getattr(args, f"{self.name}_{param_name}")

    def check_param_value_ranges(self, args):
        for param in self.parameters:
            if (
                param.range is not None
                and self.get_param_value(args, param.name) not in param.range
            ):
                raise ValueError((
                    f"Parameter value out of range : "
                    f"{self.name}_{param.name} with value {self.get_param_value(args, param.name)}"
                    f" is not in range {param.range}"
                ))

    def default_setting_value(self, setting_name):
        return (
            self.default_setting_values[setting_name]
            if setting_name in self.default_setting_values
            else None # Ouch! I don't like this!
            # But the alternative is to run a find() on the settings list...
        )

    def get_setting_value(self, args, setting_name):
        if setting_name not in valid_setting_names:
            raise ValueError("Invalid setting :", setting_name)

        return getattr(args, f"{self.name}_{setting_name}")

    def override_setting_value(self, args, setting_name, setting_value):
        if setting_name not in valid_setting_names:
            raise ValueError("Invalid setting :", setting_name)

        setattr(args, f"{self.name}_{setting_name}", setting_value)

    def check_setting_value_ranges(self, args):

        def check_setting_value_range(args, setting):
            if(
                setting.range is not None
                and self.get_setting_value(args, setting.name) not in setting.range
            ):
                raise ValueError((
                    f"Setting value out of range : "
                    f"{self.name}_{setting.name} with value {self.get_setting_value(args, setting.name)}"
                    f" is not in range {setting.range}"
                ))

        if self.can_receive_enable_settings:
            for setting in enable_settings:
                check_setting_value_range(args, setting)

        if self.can_receive_video_settings:
            for setting in video_settings:
                check_setting_value_range(args, setting)

    def video_setting_filter(self, setting_name):
        if setting_name not in valid_video_setting_filter_names:
            raise ValueError("Invalid video setting :", setting_name)

        return getattr(src.impl.filter_video_settings, f"{setting_name}_filter")

    # I don't particularly like having ffmpeg-related strings in this submodule.
    # They're not *technically* part of the FFMPEG filtergraph, but...still.
    # It's out of place.

    @property
    def filter_io_label_before_feature(self):
        return f"before_{self.name}"

    @property
    def filter_io_label_to_feature(self):
        return f"to_{self.name}"

    @property
    def filter_io_label_to_video_effects(self):
        return f"{self.name}_to_video_effects"

    @property
    def filter_io_label_after_video_effects(self):
        return f"{self.name}_after_video_effects"

    def feature_filterstr(self, args, video_info, audio = False):

        component_function = (
            self.feature_filter
            if not audio
            else self.feature_filter_audio_component
        )

        def applies_to_component(param):
            return (
                (
                    not audio and param.applicable_component != \
                    FeatureParameterApplicableComponent.AUDIO_COMPONENT_ONLY
                )

                or

                (
                    audio and param.applicable_component != \
                    FeatureParameterApplicableComponent.VIDEO_COMPONENT_ONLY
                )
            )

        return component_function(
            *[
                self.get_param_value(args, param.name)
                for param in self.parameters
                if applies_to_component(param)
            ],

            *[
                self.get_setting_value(args, setting_name)
                for setting_name in self.settings_used_in_filter
            ],

            *[
                getattr(video_info, required_info)
                for required_info in self.video_info_used_in_filter
            ]
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
                )
            )}'''
        )

    def should_apply_alpha(self, args):

        return (
            (self.combine_mode not in (FeatureCombineMode.REPLACE, FeatureCombineMode.PRE_MERGED))
            and
            (self.combine_mode != FeatureCombineMode.MERGE or self.get_setting_value(args, "alpha") != 1.0)
        )

    def apply_video_settings(self, filterstr, args, video_info):

        if not self.can_receive_video_settings:
            return filterstr

        # Alpha should not always be applied, even if it appears in settings.

        alpha_setting = array_find(filter_bearing_video_settings, lambda setting: setting.name == "alpha")
        alpha_setting.enabled = self.should_apply_alpha

        # Surprisingly, this argument bait and switch works.
        # Thank the Devil for dynamic typing :)

        enabled_video_settings = [
            setting for setting in filter_bearing_video_settings
            if setting.enabled(
                self.get_setting_value(args, setting.name)
                if setting.name != "alpha"
                else args
            )
        ]

        def should_apply_overlay_affixes():
            return any([setting.requires_overlay for setting in enabled_video_settings])

        if should_apply_overlay_affixes():
            filterstr = filter_separator(named_io = True).join([
                split_filter(
                    self.filter_io_label_before_feature,
                    self.filter_io_label_to_feature
                ),
                (
                    filter_input(self.filter_io_label_to_feature)
                    + filterstr
                )
             ])

        for video_setting in enabled_video_settings:
            filterstr = filter_separator(named_io = False).join([
                filterstr,
                self.video_setting_filter(video_setting.name)(
                    *(
                        [self.get_setting_value(args, video_setting.name)]
                        if video_setting.own_value_used_in_setting_filter
                        else []
                    ),

                    *[
                        self.get_setting_value(
                            args, required_filterless_video_setting_name
                        )
                        for required_filterless_video_setting_name in video_setting.video_settings_used_in_setting_filter
                    ],

                    *[
                        self.get_setting_value(
                            args, required_enable_setting_name
                        )
                        for required_enable_setting_name in video_setting.enable_settings_used_in_setting_filter
                    ],

                    *[
                        getattr(video_info, required_info)
                        for required_info in video_setting.video_info_used_in_setting_filter
                    ]
                )
            ])

        if should_apply_overlay_affixes():
            filterstr = filter_separator(named_io = True).join([
                (
                    filterstr
                    + filter_output(self.filter_io_label_after_video_effects)
                ),
                overlay_filter(
                    self.filter_io_label_before_feature,
                    self.filter_io_label_after_video_effects
                )
            ])

        return (
            filterstr
            + filter_option_separator(
                is_first_option = (
                    self.combine_mode == FeatureCombineMode.PRE_MERGED
                    or should_apply_overlay_affixes()
                )
            )
        )

    def video_component(self, args, video_info):

        # FIXME : there is no better place to put this.
        # If we put it in apply_enable_settings, video settings can't use this information.

        if self.can_receive_video_settings and self.get_setting_value(args, "bpm") != 0:
            bpm_pause_interval, bpm_active_interval = bpm_synced_intervals(
                self.get_setting_value(args, "bpm"),
                self.get_setting_value(args, "bpm_active_percent"),
                video_info.fps,
                self.get_setting_value(args, "start_at"),
                self.get_setting_value(args, "invert_pause")
            )

            self.override_setting_value(args, "pause", bpm_pause_interval)
            self.override_setting_value(args, "active", bpm_active_interval)

        return (
            (
                self.apply_video_settings(
                    self.feature_filterstr(args, video_info),
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
            )
        )

    def audio_component(self, args, video_info):
        if not self.has_audio_component:
            return ''

        return self.feature_filterstr(args, video_info, audio = True)

    def __call__(self, args, video_info, seeking_audio_component = False):

        if not self.is_enabled(args):
            return ''

        self.check_param_value_ranges(args)
        self.check_setting_value_ranges(args)

        return (
            self.video_component(args, video_info)
            if not seeking_audio_component
            else self.audio_component(args, video_info)
        )
