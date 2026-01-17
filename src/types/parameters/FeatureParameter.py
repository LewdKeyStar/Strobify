from dataclasses import dataclass

from src.types.abstract.FeatureOption import FeatureOption
from src.types.parameters.FeatureParameterApplicableComponent import FeatureParameterApplicableComponent

# This is a class for feature-specific parameters, which are unique to this feature,
# As opposed to FeatureSetting.
# In practice, though, almost their entire implementation is the same.

@dataclass
class FeatureParameter(FeatureOption):
    applicable_component: FeatureParameterApplicableComponent = (
        FeatureParameterApplicableComponent.VIDEO_COMPONENT_ONLY
    )
