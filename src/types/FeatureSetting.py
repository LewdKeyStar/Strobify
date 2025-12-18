from dataclasses import dataclass
from collections.abc import Callable

from src.types.abstract.Shortenable import Shortenable

@dataclass
class FeatureSetting(Shortenable):
    name: str
    default: any = 0
    type: any = int
    active_condition: Callable[[any], bool] = lambda x: True
