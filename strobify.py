from os.path import splitext
from ffmpy import FFmpeg
from argparse import ArgumentParser

from src.ffprobe_utils import (
    get_resolution,
    get_fps
)

from src.filters import (
    invert_filter,
    rgbshift_filter,
    zoom_filter,
    palette_filter
)

from src.parser_utils import (
    register_feature
)

from src.constants import *

def to_output_name(args):
    input_name, input_ext = splitext(args.input)
    return input_name+f'''_strobe_every_{
        args.strobe_every
    }{
        f'_start_from_{args.strobe_start_at}' if args.strobe_start_at > 0 else ''
    }{
        f'_end_at_{args.strobe_end_at}' if args.strobe_end_at < UINT32_MAX else ''
    }{
        f'_pause_{args.strobe_pause}' if args.strobe_pause > 0 else ''
    }{
        f'_active_{args.strobe_active}' if args.strobe_pause > 0 and args.strobe_active > 0 else ''
    }{
        "_inverted" if args.strobe_pause > 0 and args.strobe_invert_pause else ''
    }{
        (
            f'_rgb_{args.rgb_shift_intensity}px'
            f'_every_{args.rgb_shift_every}'
            + (f'_start_from_{args.rgb_shift_start_at}' if args.rgb_shift_start_at > 0 else '')
            + (f'_end_at_{args.rgb_shift_end_at}' if args.rgb_shift_end_at < UINT32_MAX else '')
        ) if args.rgb_shift else ''
    }{
        (
            f'_zoom_{args.zoom_factor}x'
            f'_into_({args.zoom_center_x},{args.zoom_center_y})'
            + (f'_start_from_{args.zoom_start_at}' if args.zoom_start_at > 0 else '')
            + (f'_end_at_{args.zoom_end_at}' if args.zoom_end_at < UINT32_MAX else '')
            + (f'_pause_{args.zoom_pause}' if args.zoom_pause > 0 else '')
            + (f'_active_{args.zoom_active}' if args.zoom_pause > 0 and args.zoom_active > 0 else '')
            + (f'_inverted' if args.zoom_invert_pause else '')
            + f'_alpha_{args.zoom_alpha}'
        ) if args.zoom else ''
    }'''+input_ext

def appropriate_filters(args, *, resolution, fps):
    all_filters = [
        invert_filter(
            args.strobe_start_at,
            args.strobe_end_at,
            args.strobe_every,
            args.strobe_pause,
            args.strobe_active,
            args.strobe_invert_pause
        ),

        rgbshift_filter(
            args.rgb_shift_start_at,
            args.rgb_shift_end_at,
            args.rgb_shift_intensity,
            args.rgb_shift_every
        ) if args.rgb_shift else "",

        zoom_filter(
            resolution,
            fps,

            args.zoom_factor,
            args.zoom_center_x,
            args.zoom_center_y,
            args.zoom_alpha,

            args.zoom_start_at,
            args.zoom_end_at,

            args.zoom_pause,
            args.zoom_active,
            args.zoom_invert_pause
        ),

        palette_filter() if splitext(args.input)[1].lower() == ".gif" else ""
    ]

    return ",".join([
        filter for filter in all_filters if filter != ""
    ])

def main():
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    register_feature(
        "strobe",

        parser = parser,

        default_values = {
            "every": DEFAULT_STROBE_EVERY,
            "pause": DEFAULT_STROBE_PAUSE
        },

        # TODO : this is done for ease on the options,
        # but in practice it also means there is an option called "-" !
        # I'm not sure how valid that is
        shorthand_prefix = "",
        enable_default = True
    )

    register_feature(
        "rgb_shift",

        ["intensity"],
        {"intensity": {"default": DEFAULT_RGB_SHIFT_INTENSITY}},

        parser = parser,

        default_values = {
            "every": DEFAULT_RGB_SHIFT_EVERY,
            "pause": DEFAULT_RGB_SHIFT_PAUSE
        }
    )

    register_feature(
        "zoom",

        ["factor", "center_x", "center_y", "alpha"],
        {
            "factor": {"default": DEFAULT_ZOOM_FACTOR},

            "center_x": {
                "shorthand": "x",
                "default": DEFAULT_ZOOM_CENTER_X
            },

            "center_y": {
                "shorthand": "y",
                "default": DEFAULT_ZOOM_CENTER_Y
            },

            "alpha": {
                "shorthand": "l",
                "type": float,
                "default": DEFAULT_ZOOM_ALPHA
            }
        },

        parser = parser,

        default_values = {
            "every": DEFAULT_ZOOM_EVERY,
            "pause": DEFAULT_ZOOM_PAUSE
        }
    )

    args = parser.parse_args()

    # This has to be done because there is no way to pass a default value generator
    # To ArgumentParser ; only constant values.

    args.output = \
        to_output_name(args) \
        if args.output == DEFAULT_OUTPUT \
        else args.output

    ff = FFmpeg(
        global_options = "-y",
        inputs = {args.input: None},
        outputs = {args.output: [
            "-c:a", "copy", # this cannot be done for video, so transcoding WILL occur
            # because there is no way for ffmpeg to reference the input codec in the filter chain...
            "-vf", appropriate_filters(
                args,
                resolution = get_resolution(args.input),
                fps = get_fps(args.input)
            )
        ]}
    )

    print(ff.cmd)

    ff.run()

if __name__ == '__main__':
    main()
