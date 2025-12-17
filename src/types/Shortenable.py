from dataclasses import dataclass
from abc import ABC

from src.utils.text_utils import abbreviate

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
