from dataclasses import dataclass, field

@dataclass(repr = False)
class FeatureParameterChoices:

    choices: list[any] = field(default_factory = list) # this is never used in practice,
    # Since FeatureParameter has a default value of None for its choices.
    # This is because argparse treats any non-None choices argument as valid,
    # And so it will not accept any valid if passed an empty collection.

    def __getitem__(self, index):
        return self.choices.__getitem__(index)

    def __iter__(self):
        return self.choices.__iter__()

    def __len__(self):
        return self.choices.__len__()

    def __repr__(self):
        return (
            (
                "Possible choices : "
                '{'
                f"{', '.join(self)}"
                '}'
            )
            if len(self) > 0
            else '' # since FeatureParameter has choices set to None by default,
            # This is never used.
        )
