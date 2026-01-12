from math import floor, modf

def effective_feature_start(feature_start_at, feature_pause, feature_invert_pause):
    return feature_start_at + (feature_pause if feature_invert_pause else 0)

def bpm_synced_intervals(bpm, active_percent, fps, start, should_invert):

    if bpm == 0 :
        active_interval = pause_interval = 0
    else:
        beat_period = 1 / (bpm / 60) # in seconds

        period_whole, period_frac = modf(beat_period)

        beat_duration = (
            round(period_whole * fps + (round(period_frac*100) / ((1 / fps) * 100)))
        ) # in frames

        active_interval = round(active_percent * beat_duration)
        pause_interval = beat_duration - active_interval

    return (pause_interval, active_interval)

# TODO : this was written *after* enable_at_interval, because of the shake filter.
# Should rewrite enable_at_interval to use it.

def interval_total_length(pause_interval, active_interval):

    if pause_interval == 0:
        return 1

    elif active_interval == 0:
        return 2*pause_interval

    else:
        return pause_interval+active_interval
