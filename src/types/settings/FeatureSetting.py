from dataclasses import dataclass
from typing import Union, Callable

from argparse import Namespace

from src.types.abstract.Shortenable import Shortenable

from src.types.settings.FeatureSettingChoices import FeatureSettingChoices
from src.types.settings.FeatureSettingRange import FeatureSettingRange

@dataclass(kw_only = True)
class FeatureSetting(Shortenable):
    name: str
    default: any = 0
    type: any = int
    include_in_filename: Union[
        Callable[[any], bool], # setting_value => bool
        Callable[[Namespace, str, any], bool] # args, feature_name, setting_value => bool
    ] = lambda x: True

    choices: FeatureSettingChoices = None
    range: FeatureSettingRange = None
