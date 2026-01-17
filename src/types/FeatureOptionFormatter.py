from dataclasses import dataclass

from inspect import signature

from argparse import Namespace
from src.types.Feature import Feature
from src.types.abstract import FeatureOption

@dataclass(repr = False)
class FeatureOptionFormatter:
    args: Namespace
    feature: Feature
    option: FeatureOption

    @property
    def option_value(self):
        return getattr(self.args, f"{self.feature.name}_{self.option.name}")

    def should_include_option_in_filename(self):
        return (
            self.option.include_in_filename
            if not callable(self.option.include_in_filename)
            else self.option.include_in_filename(
                self.option_value
            )
            if len(signature(self.option.include_in_filename).parameters) == 1
            else self.option.include_in_filename(
                self.args,
                self.feature.name,
                self.option_value
            )
        )

    @property
    def named_option_value(self):
        return self.option.get_named_value_for_feature(self.args, self.feature.name)

    @property
    def option_unit(self):
        return (
            self.option.unit if not callable(self.option.unit)
            else self.option.unit(
                self.args
            )
            if len(signature(self.option.unit).parameters) == 1
            else self.option.unit(
                self.args,
                self.feature.name,
                self.option_value
            )
        )

    def __repr__(self):
        return (
            "_".join([f"{self.option.shorthand}", f"{self.named_option_value}"+f"{self.option_unit}"])
            if self.should_include_option_in_filename()
            else ""
        )
