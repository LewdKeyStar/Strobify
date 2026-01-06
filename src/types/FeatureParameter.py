from dataclasses import dataclass

from src.types.abstract.Shortenable import Shortenable
from src.types.FeatureParameterRange import FeatureParameterRange
from src.types.FeatureParameterChoices import FeatureParameterChoices

# This is a class for feature-specific parameters, which are unique to this feature,
# As opposed to FeatureSetting.

@dataclass
class FeatureParameter(Shortenable):
    name: str
    default: any = 0
    unit: str = ""
    type: any = int

    # Normally, choices and a range should not coexist...but who knows.

    choices: FeatureParameterChoices = None # ...and not an empty set of choices, otherwise argparse will accept no values.
    range: FeatureParameterRange = FeatureParameterRange()

    desc: str = ""

    # FIXME : those line breaks are not preserved in the help message.
    # This is probably due to the built-in formatter.

    @property
    def help(self):
        return f'''
        {self.desc}
        Type : {str(self.type.__name__)}
        {self.range}
        {self.choices if self.choices is not None else ''}
        '''
