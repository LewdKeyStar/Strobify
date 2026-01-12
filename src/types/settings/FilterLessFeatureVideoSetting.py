from dataclasses import dataclass

from src.types.settings.FeatureVideoSetting import FeatureVideoSetting

@dataclass(kw_only = True)
class FilterLessFeatureVideoSetting(FeatureVideoSetting):
    pass
