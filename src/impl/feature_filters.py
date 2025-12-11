from src.impl.filter_enable_settings import *

def strobe_filter(
    start_strobe_at,
    end_strobe_at,

    strobe_every,

    strobe_pause,
    strobe_active,
    should_invert_strobe_pause
):
    return (
        "lutrgb=r=negval:g=negval:b=negval:"
        f'''enable={join_and(
            enable_from(start_strobe_at),
            enable_until(end_strobe_at),
            enable_every(start_strobe_at, strobe_every),
            enable_at_interval(
                start_strobe_at,
                should_invert_strobe_pause,
                pause_interval = strobe_pause,
                active_interval = strobe_active
            )
        )}'''
    )

def rgb_shift_filter(
    shift_intensity,

    start_shift_at,
    end_shift_at,

    shift_every,

    shift_pause,
    shift_active,
    should_invert_shift_pause
):
    return (
        f"rgbashift=rh={shift_intensity}:gh={-shift_intensity}:"
        f'''enable={join_and(
            enable_from(start_shift_at),
            enable_until(end_shift_at),
            enable_every(start_shift_at, shift_every),
            enable_at_interval(
                start_shift_at,
                should_invert_shift_pause,
                pause_interval = shift_pause,
                active_interval = shift_active
            )
        )}'''
    )

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

    def t_modulo_interval():
        return f'mod(t-{start_shake_at/fps},{interval_total_length(shake_pause, shake_active)/fps})'

    return (
        f"split[orig][moving];"
        f"[moving]dblur=angle={'0' if shake_axis == 'x' else '90'}"
        f":radius={shake_blur_radius}[moving_blurred];"
        f"[orig][moving_blurred]overlay={shake_axis}='"
        f"exp(-{shake_dampen}*{t_modulo_interval()})"
        f"*{shake_amplitude}*sin(2*PI*{shake_frequency}*{t_modulo_interval()})':"
        f'''enable={join_and(
            enable_from(start_shake_at),
            enable_until(end_shake_at),
            enable_every(start_shake_at, shake_every),
            enable_at_interval(
                start_shake_at,
                should_invert_shake_pause,
                pause_interval = shake_pause,
                active_interval = shake_active
            )
        )}'''
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
        f'''[orig][zoomed_alpha]overlay=enable={join_and(
            enable_from(start_zoom_at),
            enable_until(end_zoom_at),
            enable_every(start_zoom_at, zoom_every),
            enable_at_interval(
                start_zoom_at,
                should_invert_zoom_pause,
                pause_interval = zoom_pause,
                active_interval = zoom_active
            )
        )}'''
    )
