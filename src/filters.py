from src.filter_utils import *

def invert_filter(
    start_strobe_at,
    end_strobe_at,

    strobe_every,

    strobe_pause,
    should_invert_strobe_pause
):
    return (
        "lutrgb=r=negval:g=negval:b=negval:"
        f'''enable={join_and(
            enable_from(start_strobe_at),
            enable_until(end_strobe_at),
            enable_every(strobe_every),
            enable_at_interval(strobe_every, strobe_pause, should_invert_strobe_pause)
        )}'''
    )

def rgbshift_filter(shift_intensity, shift_every):
    return (
        f"rgbashift=rh={shift_intensity}:gh={-shift_intensity}:"
        f"enable={enable_every(shift_every)}"
    )

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"
