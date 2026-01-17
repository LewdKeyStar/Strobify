from dataclasses import dataclass

from src.types.abstract.FeatureOption import FeatureOption

# This class is for options shared across all features :
# Enable conditions, alpha, fade parameters, etc.

@dataclass
class FeatureSetting(FeatureOption):
    pass
