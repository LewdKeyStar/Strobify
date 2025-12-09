from abc import ABC
from dataclasses import dataclass, field

from src.text_utils import abbreviate

@dataclass
class FeatureDefaultValues:
    every: int = 1
    pause: int = 0

@dataclass(kw_only = True)
class Shortenable(ABC):
    special_shorthand: str = None

    @property
    def shorthand(self):
        return (
            self.special_shorthand
            if self.special_shorthand is not None
            else abbreviate(self.name)
        )

@dataclass
class FeatureParameter(Shortenable):
    name: str
    default: any = 0
    unit: str = ""
    type: any = int

@dataclass
class Feature(Shortenable):
    name: str
    default_values: FeatureDefaultValues = FeatureDefaultValues()
    parameters: list[FeatureParameter] = field(default_factory=list)
    enable_default: bool = False
