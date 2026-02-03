from src.types.settings.FeatureMetaSetting import FeatureMetaSetting

# Unlike enable and video settings, all features receive meta settings.
# They are not applied on feature call ; rather, they give information about the feature
# To higher-level parts of the program.

meta_settings: list[FeatureMetaSetting] = [
    FeatureMetaSetting(
        name = "priority",
        special_shorthand = "r"
    ),
]
