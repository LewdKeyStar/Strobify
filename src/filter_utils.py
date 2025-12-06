from math import lcm

# Returns an FFMPEG "and" condition combining the desired filters.

def join_and(*conditions):
    return '*'.join(conditions)

# Enable a filter only after or before a starting/ending frame.

def enable_from(start):
    return f"'gte(n, {start})'"

def enable_until(end):
    return f"'lte(n, {end})'"

# Trigger filter only every n frames.

def enable_every(start, freq):
    return f"'eq(mod(n-{start}, {freq}), 0)'"

# Trigger a filter only for a certain interval of time,
# Then pause for that same interval and so on.

def enable_at_interval(start, interval, should_invert):

    compar_func = "gte" if should_invert else "lt"

    return "1" if interval == 0 \
    else f"'{compar_func}(mod(n-{start}, {2*interval}), {interval})'"
