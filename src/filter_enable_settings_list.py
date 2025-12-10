from src.constants import UINT32_MAX

# A declarative list of filter enable settings,
# And the respective conditions for which they are considered "active".
# For use in output naming and reflective feature calls.

settings = {
    "start_at": lambda x: x > 0,
    "end_at": lambda x: x < UINT32_MAX,
    "every": lambda x: x > 1,
    "pause": lambda x: x > 0,
    "active": lambda x: x > 0,
    "invert_pause": lambda x: x
}
