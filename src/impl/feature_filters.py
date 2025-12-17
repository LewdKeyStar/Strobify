from src.impl.filter_enable_settings import interval_total_length

def strobe_filter(
    start_strobe_at,
    end_strobe_at,

    strobe_every,

    strobe_pause,
    strobe_active,
    should_invert_strobe_pause
):
    return "lutrgb=r=negval:g=negval:b=negval:"

def rgb_shift_filter(
    shift_intensity,

    start_shift_at,
    end_shift_at,

    shift_every,

    shift_pause,
    shift_active,
    should_invert_shift_pause
):
    return f"rgbashift=rh={shift_intensity}:gh={-shift_intensity}:"

def shake_filter(
    fps,

    shake_axis,

    shake_amplitude,
    shake_frequency,
    shake_dampen,

    shake_blur_radius,

    start_shake_at,
    end_shake_at,

    shake_every,

    shake_pause,
    shake_active,
    should_invert_shake_pause
):

    if shake_axis not in ("x", "y"):
        return ''

    # This single use case is the reason why ALL filters are forced to bear enable conditions.
    # Isn't there a way to solve this??
    def t_modulo_interval():
        return f'mod(t-{start_shake_at/fps},{interval_total_length(shake_pause, shake_active)/fps})'

    return (
        f"split[orig][moving];"
        f"[moving]dblur=angle={'0' if shake_axis == 'x' else '90'}"
        f":radius={shake_blur_radius}[moving_blurred];"
        f"[orig][moving_blurred]overlay={shake_axis}='"
        f"exp(-{shake_dampen}*{t_modulo_interval()})"
        f"*{shake_amplitude}*sin(2*PI*{shake_frequency}*{t_modulo_interval()})':"
    )

def zoom_filter(
    res,
    fps,

    zoom_factor,
    zoom_center_x,
    zoom_center_y,
    zoom_alpha,

    start_zoom_at,
    end_zoom_at,

    zoom_every,

    zoom_pause,
    zoom_active,
    should_invert_zoom_pause,
):
    return (
        f"split[orig][to_zoom];"
        f"[to_zoom]zoompan=s={res}:fps={fps}:"
        f"z={zoom_factor}:d=1:"
        f"x={zoom_center_x} - {zoom_center_x}/zoom:y={zoom_center_y} - {zoom_center_y}/zoom[zoomed];"
        f"[zoomed]format=argb,colorchannelmixer=aa={zoom_alpha}[zoomed_alpha];"
        f'''[orig][zoomed_alpha]overlay=''' # On purpose : enable option provided by feature call.
    )

def frame_randomizer_filter(
    frame_randomizer_max_frames,
    frame_randomizer_seed,

    start_frame_randomizer_at,
    end_frame_randomizer_at,

    frame_randomizer_every,

    frame_randomizer_pause,
    frame_randomizer_active,
    should_invert_frame_randomizer_pause
):
    return (
        f"split[orig][to_randomize];"
        f"[to_randomize]random=frames={frame_randomizer_max_frames}:"
        f"seed={frame_randomizer_seed}[randomized];"
        f"[orig][randomized]overlay="
    )
