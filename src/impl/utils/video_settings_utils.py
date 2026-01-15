def fade_cyclical_sync_values(
    feature_pause,
    feature_active,
    fade_cyclical_sync_in_percent,
    fade_cyclical_sync_out_percent
):

    if feature_active == 0:
        feature_active = feature_pause

    fade_in_duration = fade_cyclical_sync_in_percent * feature_active
    fade_out_duration = fade_cyclical_sync_out_percent * feature_active
    fade_out_cyclical_peak = feature_active - (fade_in_duration + fade_out_duration)
    fade_out_cyclical_trough = feature_pause

    return (
        fade_in_duration,
        fade_out_duration,
        fade_out_cyclical_peak,
        fade_out_cyclical_trough
    )
