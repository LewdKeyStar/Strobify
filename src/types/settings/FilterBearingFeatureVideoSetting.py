from dataclasses import dataclass, field
from collections.abc import Callable

from src.types.settings.FeatureVideoSetting import FeatureVideoSetting

@dataclass(kw_only = True)
class FilterBearingFeatureVideoSetting(FeatureVideoSetting):
    enabled: Callable[[any], bool] = lambda x: True

    requires_overlay: bool = False

    video_settings_used_in_setting_filter: list[str] = field(default_factory = list)
    enable_settings_used_in_setting_filter: list[str] = field(default_factory = list)
    video_info_used_in_setting_filter: list[str] = field(default_factory = list)

    def __post_init__(self):
        self.enabled = self.include_in_filename
