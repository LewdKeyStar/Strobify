def yuva420p_format_filter():
    return "format=yuva420p"

def eq_filter(contrast, brightness, saturation, gamma, gamma_r, gamma_g, gamma_b, gamma_weight):
    return (
        f"eq="
        f"contrast={contrast}:"
        f"brightness={brightness}:"
        f"saturation={saturation}:"
        f"gamma={gamma}:"
        f"gamma_r={gamma_r}:"
        f"gamma_g={gamma_g}:"
        f"gamma_b={gamma_b}:"
        f"gamma_weight={gamma_weight}"
    )

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"

def split_filter(primary_name, secondary_name):
    return f"split[{primary_name}][{secondary_name}];"

def alpha_filter(alpha, primary_name, to_alpha_name):
    return (
        f"[{to_alpha_name}]format=argb,colorchannelmixer=aa={alpha}[alpha];"
        f"[{primary_name}][alpha]overlay=" # On purpose : enable option provided by feature call.
    )
