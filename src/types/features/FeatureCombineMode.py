from enum import Enum

# TODO : migrate to Python 3.11 to use StrEnum instead
class FeatureCombineMode(Enum):
    # Can NEVER receive an alpha value ; will always overwrite the original video.
    REPLACE = -1

    # Can receive an alpha value, but will overwrite the original video if that alpha is 1.
    MERGE = 0

    # Can receive an alpha value, but will use an overlay even if that alpha is 1.
    OVERLAY = 1

    # Can receive an alpha value, but will handle and use it in the filterexpr itself,
    # with no post-filter application.
    PRE_MERGED = 2
