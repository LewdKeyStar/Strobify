from dataclasses import dataclass
from collections.abc import Callable

from src.types.abstract.Shortenable import Shortenable

from src.types.settings.FeatureSettingChoices import FeatureSettingChoices
from src.types.settings.FeatureSettingRange import FeatureSettingRange

@dataclass(kw_only = True)
class FeatureSetting(Shortenable):
    name: str
    default: any = 0
    type: any = int
    include_in_filename: Callable[[any], bool] = lambda x: True

    choices: FeatureSettingChoices = None
    range: FeatureSettingRange = None
