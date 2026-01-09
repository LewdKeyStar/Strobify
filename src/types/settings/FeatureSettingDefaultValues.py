from dataclasses import dataclass, field

from src.decl.filter_settings_list import settings, valid_setting_names

@dataclass
class FeatureSettingDefaultValues:
    values: dict[str, any] = field(default_factory=dict)

    @property
    def provided_setting_names(self):
        return self.values.keys()

    def __post_init__(self):
        for provided_setting_name in self.provided_setting_names:
            if provided_setting_name not in valid_setting_names:
                raise ValueError("Default value declared for nonexistent setting")

    def __contains__(self, setting_name):
        return setting_name in self.provided_setting_names

    def __getitem__(self, setting_name):
        return self.values[setting_name]
