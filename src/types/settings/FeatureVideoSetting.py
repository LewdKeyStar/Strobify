from dataclasses import dataclass
from src.types.settings.FeatureSetting import FeatureSetting

@dataclass(kw_only = True)
class FeatureVideoSetting(FeatureSetting):
    requires_formatting: bool = False
