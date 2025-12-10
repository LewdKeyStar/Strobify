from src.filter_enable_settings import *

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
        f"x={zoom_center_x}/{zoom_factor}:y={zoom_center_y}/{zoom_factor}[zoomed];"
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

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"
