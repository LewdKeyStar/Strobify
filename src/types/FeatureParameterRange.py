from dataclasses import dataclass
from typing import Union

@dataclass(repr = False)
class FeatureParameterRange:

    min: Union[int, float] = 0
    max: Union[int, float] = 0

    # ...it's still better to check though.

    def __post_init__(self):
        if (
            not all([
                isinstance(bound, int)
                or isinstance(bound, float)
                for bound in (self.min, self.max)
            ])
        ):
            raise TypeError("Range created with non-numerical bounds")

    def __contains__(self, value):
        return value >= self.min and value <= self.max

    def __repr__(self):
        return (
            f"[{self.min}, {self.max}]"
            if self.min is not None and self.max is not None
            else ''
        )
