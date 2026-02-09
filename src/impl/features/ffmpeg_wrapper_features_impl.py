from src.impl.utils.feature_utils import eq_filter

def invert_filter(
    invert_gamma
):

    gamma_negval = f"pow((negval-minval)/(maxval-minval)\,{invert_gamma})*(maxval-minval)+minval"

    return f"lutrgb=r={gamma_negval}:g={gamma_negval}:b={gamma_negval}"

def rgb_shift_filter(
    shift_axis,
    shift_intensity,
    shift_colors
):

    direction = "h" if shift_axis == "x" else "v"

    return (
        f"rgbashift="
        f"{shift_colors[0]}{direction}={shift_intensity}:"
        f"{shift_colors[1]}{direction}={-shift_intensity}"
    )

def darken_filter(
    darken_contrast,
    darken_brightness,
    darken_saturation,
    darken_gamma,
    darken_gamma_r,
    darken_gamma_g,
    darken_gamma_b,
    darken_gamma_weight
):
    return eq_filter(
        darken_contrast,
        darken_brightness,
        darken_saturation,
        darken_gamma,
        darken_gamma_r,
        darken_gamma_g,
        darken_gamma_b,
        darken_gamma_weight
    )

def lighten_filter(
    lighten_contrast,
    lighten_brightness,
    lighten_saturation,
    lighten_gamma,
    lighten_gamma_r,
    lighten_gamma_g,
    lighten_gamma_b,
    lighten_gamma_weight
):
    return eq_filter(
        lighten_contrast,
        lighten_brightness,
        lighten_saturation,
        lighten_gamma,
        lighten_gamma_r,
        lighten_gamma_g,
        lighten_gamma_b,
        lighten_gamma_weight
    )

def hue_saturation_filter(
    hue_saturation_hue,
    hue_saturation_saturation,
    hue_saturation_brightness
):

    return (
        f"hue="
        f"h={hue_saturation_hue}:"
        f"s={hue_saturation_saturation}:"
        f"b={hue_saturation_brightness}"
    )

def fade_in_filter(
    fade_in_duration,
    fade_in_color,

    video_duration
):
    return (
        f"fade=t=in:"
        f"n={min(fade_in_duration, video_duration)}:"
        f"c={fade_in_color}"
    )

def fade_out_filter(
    fade_out_duration,
    fade_out_color,

    video_duration
):
    return (
        f"fade=t=out:"
        f"s={max(0, video_duration-fade_out_duration)}:"
        f"n={min(fade_out_duration, video_duration)}:"
        f"c={fade_out_color}"
    )

def gaussian_blur_filter(
    gaussian_blur_sigma,
    gaussian_blur_steps
):
    return (
        f"gblur=sigma={gaussian_blur_sigma}:steps={gaussian_blur_steps}"
    )
