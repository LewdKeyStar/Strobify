from dataclasses import dataclass
from collections.abc import Callable

from src.types.settings.FeatureSetting import FeatureSetting

@dataclass(kw_only = True)
class FeatureEnableSetting(FeatureSetting):
    active_condition: Callable[[any], bool] = lambda x: True
