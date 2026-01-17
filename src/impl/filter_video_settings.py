from src.impl.misc_filters import fade_in_filter_generic, fade_out_filter_generic
from src.utils.filter_utils import filter_separator

def alpha_filter(alpha):
    return (
        f"format=argb,colorchannelmixer=aa={alpha}"
    )

def fade_in_filter(
    fade_in_duration,

    fade_in_function,

    feature_start_at,
    feature_pause,
    feature_invert_pause,

    video_duration
):
    return fade_in_filter_generic(
        fade_in_duration = fade_in_duration,

        fade_in_function = fade_in_function,

        feature_start_at = feature_start_at,
        feature_pause = feature_pause,
        feature_invert_pause = feature_invert_pause,

        video_duration = video_duration
    )

def fade_out_filter(
    fade_out_duration,

    fade_out_function,

    feature_end_at,

    video_duration
):
    return fade_out_filter_generic(
        fade_out_duration = fade_out_duration,

        fade_out_function = fade_out_function,

        feature_end_at = feature_end_at,

        video_duration = video_duration
    )

def fade_cyclical_filter(
    fade_in_duration,
    fade_out_duration,

    fade_in_function,
    fade_out_function,

    fade_cyclical_peak,
    fade_cyclical_trough,

    fade_cyclical_sync,
    fade_cyclical_sync_in_percent,
    fade_cyclical_sync_out_percent,

    feature_start_at,
    feature_end_at,
    feature_pause,
    feature_active,
    feature_invert_pause,

    video_duration
):

    # Look.
    # It's either this, or we set them all to False and zero in the above calls.
    # Just go with it.

    return filter_separator(named_io=False).join([
        fade_in_filter_generic(
            fade_in_duration = fade_in_duration,
            fade_out_duration = fade_out_duration,
            fade_in_function = fade_in_function,
            fade_cyclical = True,
            fade_cyclical_peak = fade_cyclical_peak,
            fade_cyclical_trough = fade_cyclical_trough,
            fade_cyclical_sync = fade_cyclical_sync,
            fade_cyclical_sync_in_percent = fade_cyclical_sync_in_percent,
            fade_cyclical_sync_out_percent = fade_cyclical_sync_out_percent,
            feature_start_at = feature_start_at,
            feature_pause = feature_pause,
            feature_active = feature_active,
            feature_invert_pause = feature_invert_pause,
            video_duration = video_duration
        ),

        fade_out_filter_generic(
            fade_out_duration = fade_out_duration,
            fade_in_duration = fade_in_duration,
            fade_out_function = fade_out_function,
            fade_cyclical = True,
            fade_cyclical_peak = fade_cyclical_peak,
            fade_cyclical_trough = fade_cyclical_trough,
            fade_cyclical_sync = fade_cyclical_sync,
            fade_cyclical_sync_in_percent = fade_cyclical_sync_in_percent,
            fade_cyclical_sync_out_percent = fade_cyclical_sync_out_percent,
            feature_start_at = feature_start_at,
            feature_end_at = feature_end_at,
            feature_pause = feature_pause,
            feature_active = feature_active,
            feature_invert_pause = feature_invert_pause,
            video_duration = video_duration
        )
    ])
