from math import lcm

def invert_filter(strobe_every, strobe_pause, should_invert_strobe_pause):
    def enforce_strobe_every(strobe_every):
        return f"eq(mod(n, {strobe_every}), 0)"

    def enforce_strobe_pause(strobe_every, strobe_pause, should_invert_strobe_pause):

        compar_func = "gte" if should_invert_strobe_pause else "lt"

        return "1" if strobe_pause == 0 \
        else f"{compar_func}(mod(n, {2*lcm(strobe_every,strobe_pause)}), {lcm(strobe_every,strobe_pause)})"

    return f'''lutrgb=r=negval:g=negval:b=negval:enable='{
        enforce_strobe_every(strobe_every)
    } * {
        enforce_strobe_pause(strobe_every, strobe_pause, should_invert_strobe_pause)
    }\''''

# For GIF management ;
# Without a separate palette for each GIF frame, noticeable quantization noise appears.
# The optimized thing to do would be to have two palettes : one for the normal frames, one for the inverted

def palette_filter():
    return "split[s0][s1];[s0]palettegen=stats_mode=single[p];[s1][p]paletteuse=new=1"
