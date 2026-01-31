from src.impl.misc_filters import fade_in_filter_generic, fade_out_filter_generic
from src.utils.filter_utils import filter_separator

def alpha_filter(alpha):
    return (
        f"format=argb,colorchannelmixer=aa={alpha}"
    )

def fade_in_filter(
    fade_in_duration,

    fade_in_function,

    feature_start_at,
    feature_pause,
    feature_invert_pause,

    video_duration
):
    return fade_in_filter_generic(
        fade_in_duration = fade_in_duration,

        fade_in_function = fade_in_function,

        feature_start_at = feature_start_at,
        feature_pause = feature_pause,
        feature_invert_pause = feature_invert_pause,

        video_duration = video_duration
    )

def fade_out_filter(
    fade_out_duration,

    fade_out_function,

    feature_end_at,

    video_duration
):
    return fade_out_filter_generic(
        fade_out_duration = fade_out_duration,

        fade_out_function = fade_out_function,

        feature_end_at = feature_end_at,

        video_duration = video_duration
    )

def fade_cyclical_filter(
    fade_in_duration,
    fade_out_duration,

    fade_in_function,
    fade_out_function,

    fade_cyclical_peak,
    fade_cyclical_trough,

    fade_cyclical_sync,
    fade_cyclical_sync_in_percent,
    fade_cyclical_sync_out_percent,

    feature_start_at,
    feature_end_at,
    feature_pause,
    feature_active,
    feature_invert_pause,

    video_duration
):

    # Look.
    # It's either this, or we set them all to False and zero in the above calls.
    # Just go with it.

    return filter_separator(named_io=False).join([
        fade_in_filter_generic(
            fade_in_duration = fade_in_duration,
            fade_out_duration = fade_out_duration,
            fade_in_function = fade_in_function,
            fade_cyclical = True,
            fade_cyclical_peak = fade_cyclical_peak,
            fade_cyclical_trough = fade_cyclical_trough,
            fade_cyclical_sync = fade_cyclical_sync,
            fade_cyclical_sync_in_percent = fade_cyclical_sync_in_percent,
            fade_cyclical_sync_out_percent = fade_cyclical_sync_out_percent,
            feature_start_at = feature_start_at,
            feature_pause = feature_pause,
            feature_active = feature_active,
            feature_invert_pause = feature_invert_pause,
            video_duration = video_duration
        ),

        fade_out_filter_generic(
            fade_out_duration = fade_out_duration,
            fade_in_duration = fade_in_duration,
            fade_out_function = fade_out_function,
            fade_cyclical = True,
            fade_cyclical_peak = fade_cyclical_peak,
            fade_cyclical_trough = fade_cyclical_trough,
            fade_cyclical_sync = fade_cyclical_sync,
            fade_cyclical_sync_in_percent = fade_cyclical_sync_in_percent,
            fade_cyclical_sync_out_percent = fade_cyclical_sync_out_percent,
            feature_start_at = feature_start_at,
            feature_end_at = feature_end_at,
            feature_pause = feature_pause,
            feature_active = feature_active,
            feature_invert_pause = feature_invert_pause,
            video_duration = video_duration
        )
    ])

def crop_filter(
    crop_top,
    crop_bottom,
    crop_left,
    crop_right,

    crop_center_x,
    crop_center_y,
    crop_width,
    crop_height,

    crop_edge_fade,

    crop_center_mode,
    crop_relative_mode,

    resolution
):

    if (
        crop_center_mode
        and
        any(
            param < 0 for param in [
                crop_center_x,
                crop_center_y,
                crop_width,
                crop_height
            ]
        )
    ):
        raise ValueError(
            "Center-mode feature crop invoked without setting all of : "
            "crop center x, crop center y, crop width, crop height"
        )

    if(
        not crop_center_mode
        and
        any(
            param < 0 for param in [
                crop_top,
                crop_bottom,
                crop_left,
                crop_right
            ]
        )
    ):
        raise ValueError(
            "Corner-mode feature crop invoked without setting all of : "
            "crop top, crop bottom, crop left, crop right"
        )

    width, height = resolution.split("x")
    width, height = int(width), int(height)

    # The "center" and "corner" modes are equivalent in practice.

    if crop_center_mode:

        if crop_relative_mode:
            crop_center_x *= width
            crop_width *= width
            crop_center_y *= height
            crop_height *= height

        crop_top, crop_bottom, crop_left, crop_right = (
            crop_center_y - crop_height / 2,
            crop_center_y + crop_height / 2,
            crop_center_x - crop_width / 2,
            crop_center_x + crop_width / 2
        )

    else:

        if crop_relative_mode:

            crop_top *= height
            crop_bottom *= height
            crop_left *= width
            crop_right *= width

        crop_center_x = crop_left + (crop_right - crop_left) / 2
        crop_center_y = crop_top + (crop_bottom - crop_top) / 2

    # Now that that equivalency is assured, we can begin to work out fade conditions.

    # A pixel being in the fading area is determined through its distance to the center.

    def distance_center_x(x = 'X'):
        return f"(abs({x} - {crop_center_x}))"

    def distance_center_y(y = 'Y'):
        return f"(abs({y} - {crop_center_y}))"

    edge_lr_inner_bound = distance_center_x(crop_right)
    edge_tb_inner_bound = distance_center_y(crop_bottom)

    edge_lr_outer_bound = distance_center_x(crop_right + crop_edge_fade)
    edge_tb_outer_bound = distance_center_y(crop_bottom + crop_edge_fade)

    def in_tb_edge():
        return f"gt({distance_center_y()}, {edge_tb_inner_bound})"

    # For the left and right edges, we need to test inclusion with and without corners.
    # A corner is just a part of the lr edge that is also in the tb edge.

    def in_lr_edge(include_corners = False):
        return (
            f"gt({distance_center_x()}, {edge_lr_inner_bound})"
            +
            (
                ""
                if include_corners
                else f"*not({in_tb_edge()})"
            )
        )

    # Now that edges are dealt with, we have to handle corners.
    # Fade corners have to be cut diagonally in half, like :

    # - - - - - - - - -
    # |F \ _F A_D E_/ F|
    # |A |          | A|
    # |D |  normal  | D|
    # |E | _ _ _ _ _| E|
    # | /  F A D E   \ |
    # - - - - - - - - --

    # (I'm so good at drawing...)

    # In all four cases, it's about selecting above or below a diagonal
    # With x and y (lowercase) relative to a certain origin :

    # Top-left corner : origin (left-fade, top-fade)
    # Equation : x < y

    def in_tl_lr_corner_half():
        return (
            f"("
                f"lt(X, {crop_left})"
                f"*"
                f"lt(Y, {crop_top})"
                f"*"
                f"lt((X - {crop_left - crop_edge_fade}), (Y - {crop_top - crop_edge_fade}))"
            f")"
        )

    # Top-right corner : origin (right, top-fade)
    # Equation : x > edge - y

    def in_tr_lr_corner_half():
        return (
            f"("
                f"gt(X, {crop_right})"
                f"*"
                f"lt(Y, {crop_top})"
                f"*"
                f"gt((X - {crop_right}), {crop_edge_fade} - (Y - {crop_top - crop_edge_fade}))"
            f")"
        )

    # Bottom-left corner : origin (left-fade, bottom)
    # Equation : x < edge - y

    def in_bl_lr_corner_half():
        return (
            f"("
                f"lt(X, {crop_left})"
                f"*"
                f"gt(Y, {crop_bottom})"
                f"*"
                f"lt((X - {crop_left - crop_edge_fade}), {crop_edge_fade} - (Y - {crop_bottom}))"
            f")"
        )

    # Bottom-right corner : origin (right, bottom)
    # Equation : x > y

    def in_br_lr_corner_half():
        return (
            f"("
                f"gt(X, {crop_right})"
                f"*"
                f"gt(Y, {crop_bottom})"
                f"*"
                f"gt((X - {crop_right}), (Y - {crop_bottom}))"
            f")"
        )

    # So now we can know if a pixel is in the LR half of a fade corner.

    def in_lr_corner_halves():
        return (
            f"("
                f"{in_tb_edge()}"
                f"*"
                f"{in_lr_edge(include_corners = True)}"

                f"*"

                f"("
                    f"{in_tl_lr_corner_half()}"
                    f"+"
                    f"{in_tr_lr_corner_half()}"
                    f"+"
                    f"{in_bl_lr_corner_half()}"
                    f"+"
                    f"{in_br_lr_corner_half()}"
                f")"
            f")"
        )

    # Now that edges and corners are both handled, we define linear fade coefficients.
    # One for the LR edges and their halves of their corners,
    # One for the TB edges and their halves.

    # Note : +1 is if the fade is 1 pixel...is that really useful, though?
    # Is anyone ever going to do this?

    fade_coefficient_lr = (
        f"((abs({edge_lr_outer_bound} - {distance_center_x()})) / {crop_edge_fade + 1})"
    )

    fade_coefficient_tb = (
        f"((abs({edge_tb_outer_bound} - {distance_center_y()})) / {crop_edge_fade + 1})"
    )

    # Everything is ready.

    return (
        f"format=argb,"
        f"geq=r='p(X,Y)':"
        f"a='if("
            f"between(X, {crop_left - crop_edge_fade}, {crop_right + crop_edge_fade})*"
            f"between(Y, {crop_top - crop_edge_fade}, {crop_bottom + crop_edge_fade}),"

            f"if("
                f"between(X, {crop_left}, {crop_right})*"
                f"between(Y, {crop_top}, {crop_bottom}),"

                f"p(X,Y),"
                f'''{
                    '0' if crop_edge_fade == 0
                    else (
                        f'if('
                            f'{in_lr_edge()}+{in_lr_corner_halves()},'
                            f'{fade_coefficient_lr}*p(X,Y),'
                            f'if('
                                f'{in_tb_edge()}*not({in_lr_corner_halves()}),'
                                f'{fade_coefficient_tb}*p(X,Y),'
                                '0'
                            f')'
                        f')'
                    )
                }'''
            f")"
        f")'"
    )
