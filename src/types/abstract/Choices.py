from dataclasses import dataclass, field

from abc import ABC

@dataclass(repr = False)
class Choices(ABC):
    choices: list[any] = field(default_factory = list) # this is never used in practice,
    # Since the applicable classes have a default value of None for their choices.
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
                '{'
                f"{', '.join(self)}"
                '}'
            )
            if len(self) > 0
            else '' # since choices are set to None by default,
            # This is never used.
        )
