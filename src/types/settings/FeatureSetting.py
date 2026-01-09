from dataclasses import dataclass

from src.types.abstract.Shortenable import Shortenable

@dataclass(kw_only = True)
class FeatureSetting(Shortenable):
    name: str
    default: any = 0
    type: any = int
