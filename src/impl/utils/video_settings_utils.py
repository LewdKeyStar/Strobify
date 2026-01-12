def fade_cyclical_sync_values(
    feature_pause,
    feature_active,
    fade_cyclical_sync_in_percent,
    fade_cyclical_sync_out_percent
):

    # FIXME : this is ALL bad.
    # The pause/active system is bad enough,
    # But not being able to default to 0.5 for the percentages is stupider.
    # (As a reminder, it's because otherwise they appear in the filename)

    if feature_active == 0:
        feature_active = feature_pause

    if fade_cyclical_sync_in_percent == 0:
        fade_cyclical_sync_in_percent = 0.5

    if fade_cyclical_sync_out_percent == 0:
        fade_cyclical_sync_out_percent = 0.5

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
