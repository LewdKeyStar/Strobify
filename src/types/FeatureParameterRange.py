from dataclasses import dataclass

@dataclass(repr = False)
class FeatureParameterRange:

    # This would be int | float...but Python's builtin type annotations don't do unions :)))
    # Even TypeScript has them...

    min: any = 0
    max: any = 0

    # ...so now, since we can't test if these are numbers,
    # We have to test if they can be compared...
    # Look at this fucking clownery.

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
