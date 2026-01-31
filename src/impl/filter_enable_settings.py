from src.constants import UINT32_MAX

# Returns an FFMPEG "and" condition combining the desired filters.

def join_and(*conditions):
    return '*'.join(conditions).replace('*1', '') # '*1' means "and True"

# Enable a filter only after or before a starting/ending frame.

def enable_from(start):
    return (
        "1" if start == 0
        else f"'gte(n, {start})'"
    )

def enable_until(end):
    return (
        "1" if end == UINT32_MAX
        else f"'lte(n, {end})'"
    )

# Trigger filter only every n frames.

def enable_every(start, freq):
    return (
        "1" if freq == 1
        else f"'eq(mod(n-{start}, {freq}), 0)'"
    )

# Trigger a filter only for a certain interval of time,
# Then pause for either another interval,
# Or, if none is provided (which defaults to a value of 0), for as long as the pause.
# Then, repeat.

# If should_invert is true, begin by a pause period, then an active period, and so on.

def enable_at_interval(start, should_invert, pause_interval, active_interval):

    compar_func = "gte" if should_invert else "lt"

    if pause_interval == 0:
        return "1"

    elif active_interval == 0:
        return f"'{compar_func}(mod(n-{start}, {2*pause_interval}), {pause_interval})'"

    else:
        return (
            f"'{compar_func}"
            f"(mod(n-{start}, {pause_interval+active_interval}),"
            f"{pause_interval if should_invert else active_interval})'"
        )

def enable_at_random(random_enabled, random_seed, random_probability):

    if (not random_enabled) or (random_seed < 0):
        return "1"

    return (
        f"'if(eq(n, 0), st(1, {random_seed}));"
        f"min(max(round(random(1)+ {random_probability - 0.5}), 0), 1)'"
    )
