from src.impl.misc_filters import fade_filter

from src.impl.utils.enable_settings_utils import effective_feature_start

def alpha_filter(alpha):
    return (
        f"format=argb,colorchannelmixer=aa={alpha}"
    )

def fade_in_filter(
    fade_in_duration,
    fade_out_duration,

    fade_cyclical,

    fade_cyclical_peak,
    fade_cyclical_trough,

    feature_start_at,
    feature_pause, feature_active, feature_invert_pause,

    video_duration
):

    if fade_cyclical and fade_out_duration == 0:
        raise ValueError("Cyclical fade set with no fadeout duration")

    actual_feature_start = effective_feature_start(
        feature_start_at,
        feature_pause,
        feature_invert_pause
    )

    fade_in_start_at = actual_feature_start

    # The total time of an in-out cycle.
    # In the case of a non-cyclical fade, peak is irrelevant.
    total_fade_time = fade_in_duration + (fade_cyclical_peak) + fade_out_duration

    return (
        f'''format=argb,geq=r='p(X,Y)':a={fade_filter(
            type = "in",
            start_frame = fade_in_start_at,
            end_frame = fade_in_start_at + fade_in_duration,
            video_duration = video_duration,
            n_expression = (
                "N" if not fade_cyclical
                else f"mod(N - {actual_feature_start}, {total_fade_time + fade_cyclical_trough})"
            ),
            cyclical_offset = actual_feature_start if fade_cyclical else 0
        )}'''
    )

def fade_out_filter(
    fade_out_duration,
    fade_in_duration,

    fade_cyclical,

    fade_cyclical_peak,
    fade_cyclical_trough,

    feature_start_at,
    feature_end_at,
    feature_pause, feature_active, feature_invert_pause,

    video_duration
):

    if fade_cyclical and fade_in_duration == 0:
        raise ValueError("Cyclical fade set with no fadein duration")

    actual_feature_start = effective_feature_start(
        feature_start_at,
        feature_pause,
        feature_invert_pause
    )

    # The total time of an in-out cycle.
    # In the case of a non-cyclical fade, peak is irrelevant.
    # FIXME : honestly, duplicating this seems like the lesser of two evils.
    total_fade_time = fade_in_duration + (fade_cyclical_peak) + fade_out_duration

    fade_out_end_at = (
        feature_end_at if not fade_cyclical
        else actual_feature_start + total_fade_time # = fade_in_start_at + total_fade_time
    )

    # The min between end frame and duration has to preemptively happen here,
    # Otherwise the start frame is incorrect.
    return (
        f'''format=argb,geq=r='p(X,Y)':a={fade_filter(
            type = "out",
            start_frame = min(fade_out_end_at, video_duration) - fade_out_duration,
            end_frame = fade_out_end_at,
            video_duration = video_duration,
            n_expression = (
                "N" if not fade_cyclical
                else f"mod(N - {actual_feature_start}, {total_fade_time + fade_cyclical_trough})"
            ),
            cyclical_offset = actual_feature_start if fade_cyclical else 0
        )}'''
    )
