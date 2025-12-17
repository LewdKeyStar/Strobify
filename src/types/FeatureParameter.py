from dataclasses import dataclass

from src.types.Shortenable import Shortenable

@dataclass
class FeatureParameter(Shortenable):
    name: str
    default: any = 0
    unit: str = ""
    type: any = int
