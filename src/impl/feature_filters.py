from src.impl.filter_enable_settings import interval_total_length
from src.constants import VALID_AXES, VALID_COLORS, TRANSPARENT_FFMPEG_COLOR

def strobe_filter(
    strobe_gamma
):

    gamma_negval = f"pow((negval-minval)/(maxval-minval)\,{strobe_gamma})*(maxval-minval)+minval"

    return f"lutrgb=r={gamma_negval}:g={gamma_negval}:b={gamma_negval}"

def rgb_shift_filter(
    shift_axis,
    shift_intensity,
    shift_colors
):
    if shift_axis not in VALID_AXES:
        raise ValueError("Invalid axis :", shift_axis)

    direction = "h" if shift_axis == "x" else "v"

    if shift_colors not in VALID_COLORS:
        raise ValueError("Invalid colors :", shift_colors)

    return (
        f"rgbashift="
        f"{shift_colors[0]}{direction}={shift_intensity}:"
        f"{shift_colors[1]}{direction}={-shift_intensity}"
    )

def shake_filter(
    shake_axis,

    shake_amplitude,
    shake_frequency,
    shake_dampen,

    shake_blur_radius,

    start_shake_at,

    shake_pause,
    shake_active,

    fps
):

    if shake_axis not in VALID_AXES:
        raise ValueError("Invalid axis :", shake_axis)

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
        f"*{shake_amplitude}*sin(2*PI*{shake_frequency}*{t_modulo_interval()})'"
    )

def zoom_filter(
    zoom_factor,
    zoom_center_x,
    zoom_center_y,

    res,
    fps
):
    return (
        f"zoompan=s={res}:fps={fps}:"
        f"z={zoom_factor}:d=1:"
        f"x={zoom_center_x} - {zoom_center_x}/zoom:y={zoom_center_y} - {zoom_center_y}/zoom"
    )

def frame_randomizer_filter(
    frame_randomizer_max_frames,
    frame_randomizer_seed
):
    return (
        f"random=frames={frame_randomizer_max_frames}:"
        f"seed={frame_randomizer_seed}"
    )

def afterimages_filter(
    afterimages_amount,
    afterimages_delay,

    afterimages_alpha
):

    def amount_range():
        return range(1, afterimages_amount + 1)

    def overlay_step(i):
        return (
            f"overlay_step{i}"
            if i > 0
            else "before_afterimages"
        )

    return (
        f"split={afterimages_amount+1}[before_afterimages]{''.join([f'[clone{i}]' for i in amount_range()])};"
        f'''{''.join([
            f"[clone{i}]tpad=start={i*afterimages_delay}:color={TRANSPARENT_FFMPEG_COLOR}[afterimage{i}];"
            f"[afterimage{i}]format=argb,colorchannelmixer=aa={afterimages_alpha}[afterimage{i}_alpha];"
            f"[{overlay_step(i-1)}][afterimage{i}_alpha]overlay[{overlay_step(i)}];"
            for i in amount_range()
        ])}'''
    ).removesuffix(f"[{overlay_step(afterimages_amount)}];") # no output name for the last step

def speed_change_filter(
    speed_change_factor,
    speed_change_preserve_pitch,
    speed_change_preserve_formants
):

    return (
        f"setpts={1/speed_change_factor}*PTS"
    )

def speed_change_filter_audio_component(
    speed_change_factor,
    speed_change_preserve_pitch,
    speed_change_preserve_formants
):

    return (
        f"rubberband=tempo={speed_change_factor}:"
        f"pitch={speed_change_factor if not speed_change_preserve_pitch else 1}:"
        f"transients=mixed:"
        f"detector=percussive:"
        f"phase=independent:"
        f"window=short:"
        f"smoothing=on:"
        f"formant={'shifted' if not speed_change_preserve_formants else 'preserved'}:"
        f"pitchq=quality:"
        f"channels=together"
    )
