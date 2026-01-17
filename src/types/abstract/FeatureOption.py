from dataclasses import dataclass, field

from typing import Union, Callable

from argparse import Namespace

from src.types.abstract.Shortenable import Shortenable
from src.types.abstract.Choices import Choices
from src.types.abstract.Range import Range

# This is a base class for FeatureParameter (a feature's unique, characteristic traits)
# And FeatureSetting (options shared across all features : enable intervals, alpha, etc.)

@dataclass
class FeatureOption(Shortenable):
    name: str
    default: any = 0
    unit: Union[
        str,
        Callable[[Namespace], str],
        Callable[[Namespace, str], str]
    ] = ""

    type: any = int

    include_in_filename: Union[
        bool, # used for all parameters for now
        Callable[[any], bool], # option_value => bool
        Callable[[Namespace, str, any], bool] # args, feature_name, option_value => bool
    ] = True

    # Normally, choices and a range should not coexist...but who knows.

    choices: Choices = None # ...and not an empty set of choices, otherwise argparse will accept no values.
    range: Range = None # ...so that if a range is instantiated, it will always mean something.

    desc: str = ""

    renamed_values: dict[any, str] = field(default_factory = dict)
    value_format: Callable[[Namespace, any], str] = lambda x, y: y

    # FIXME : those line breaks are not preserved in the help message.
    # This is probably due to the built-in formatter.

    @property
    def help(self):
        return f'''
        {self.desc}
        Type : {str(self.type.__name__)}
        {f'Range : {self.range}' if self.range is not None else ''}
        {f'Possible choices : {self.choices}' if self.choices is not None else ''}
        '''

    # This method is for exclusive use in the filename utils.
    # The actual logic uses Feature methods,
    # for the obvious reason of having direct access to the Feature name.

    def get_named_value_for_feature(self, args, feature_name):
        actual_value = getattr(args, f"{feature_name}_{self.name}")

        return (
            self.value_format(args, actual_value)
            if actual_value not in self.renamed_values
            else self.renamed_values[actual_value]
        )
