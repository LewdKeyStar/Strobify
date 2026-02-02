from abc import ABC, abstractmethod

from dataclasses import dataclass

from src.parser_namespace import runtime_value

from src.types.features.Feature import Feature
from src.types.abstract.options.FeatureOption import FeatureOption

@dataclass(repr = False)
class FeatureOptionFormatter(ABC):
    feature: Feature
    option: FeatureOption

    @property
    def option_value(self):
        return runtime_value(self.feature.name, self.option.name)

    @abstractmethod
    def _include_in_filename(self):
        pass

    def should_include_option_in_filename(self):
        return (
            self.option.include_in_filename
            if not callable(self.option.include_in_filename)
            else self._include_in_filename()
        )

    @abstractmethod
    def _value_format(self):
        pass

    @property
    def named_option_value(self):
        actual_value = self.option_value

        if actual_value in self.option.renamed_values:
            return self.option.renamed_values[actual_value]

        return self._value_format()

    @abstractmethod
    def _unit(self):
        pass

    @property
    def option_unit(self):
        return (
            self.option.unit if not callable(self.option.unit)
            else self._unit()
        )

    def __repr__(self):
        return (
            "_".join([f"{self.option.shorthand}", f"{self.named_option_value}"+f"{self.option_unit}"])
            if self.should_include_option_in_filename()
            else ""
        )
