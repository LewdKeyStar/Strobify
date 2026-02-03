from dataclasses import dataclass

from src.types.settings.FeatureSetting import FeatureSetting

@dataclass(kw_only = True)
class FeatureMetaSetting(FeatureSetting):

    # Because meta settings are...meta,
    # They're not part of the filename ; ideally, they influence it in other ways.
    # For instance, priority changes the order of the name, it's not indicated.

    include_in_filename = False
