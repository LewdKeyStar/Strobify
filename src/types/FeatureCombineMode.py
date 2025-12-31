from enum import Enum

# TODO : migrate to Python 3.11 to use StrEnum instead
class FeatureCombineMode(Enum):
    MERGE = 0
    OVERLAY = 1
    PRE_MERGED = 2
