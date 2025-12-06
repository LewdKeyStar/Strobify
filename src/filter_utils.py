from math import lcm

# Returns an FFMPEG "and" condition combining the desired filters.

def join_and(*conditions):
    return '*'.join(conditions)

# Enable a filter only after or before a starting frame.

def enable_from(start):
    return f"'gte(n, {start})'"

def enable_until(end):
    return f"'lte(n, {end})'"

# Trigger filter only every n frames.

def enable_every(freq):
    return f"'eq(mod(n, {freq}), 0)'"

# Assuming a filter is enabled every n frames, trigger it only for a certain interval of time,
# Then pause for that same interval and so on.
# This can be generalized to a filter that isn't enabled every n frames,
# Just by defining freq = 1.

def enable_at_interval(freq, interval, should_invert):

    compar_func = "gte" if should_invert else "lt"

    return "1" if interval == 0 \
    else f"'{compar_func}(mod(n, {2*lcm(freq, interval)}), {lcm(freq, interval)})'"
