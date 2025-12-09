from os.path import splitext
from ffmpy import FFmpeg
from argparse import ArgumentParser, BooleanOptionalAction

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

DEFAULT_OUTPUT = "default" # This is just a placeholder, not an actual filename.

DEFAULT_STROBE_EVERY = 2
DEFAULT_STROBE_PAUSE = 0

DEFAULT_RGB_SHIFT_INTENSITY = 5
DEFAULT_RGB_SHIFT_EVERY = 2

DEFAULT_ZOOM_FACTOR = 2
DEFAULT_ZOOM_CENTER_X = 0 # TODO : relative coordinates instead?
DEFAULT_ZOOM_CENTER_Y = 0
DEFAULT_ZOOM_ALPHA = 0.5
DEFAULT_ZOOM_PAUSE = 0

## FFMPEG uses this as its upper bound.

UINT32_MAX = 4294967295

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

    parser.add_argument("-n", "--strobe-every", type = int, nargs = "?", default = DEFAULT_STROBE_EVERY)

    parser.add_argument("-s", "--strobe-start-at", type = int, nargs = "?", default = 0)
    parser.add_argument("-e", "--strobe-end-at", type = int, nargs = "?", default = UINT32_MAX)

    parser.add_argument("-a", "--strobe-active", type=int, nargs = "?", default = DEFAULT_STROBE_PAUSE)
    parser.add_argument("-p", "--strobe-pause", type = int, nargs = "?", default = DEFAULT_STROBE_PAUSE)
    parser.add_argument("-ip", "--strobe-invert-pause", default = False, action = BooleanOptionalAction)

    parser.add_argument("-rgb", "--rgb-shift", default = False, action = BooleanOptionalAction)
    parser.add_argument("-rsi", "--rgb-shift-intensity", type = int, nargs = "?", default = DEFAULT_RGB_SHIFT_INTENSITY)
    parser.add_argument("-rsn", "--rgb-shift-every", type = int, nargs = "?", default = DEFAULT_RGB_SHIFT_EVERY)

    parser.add_argument("-rss", "--rgb-shift-start-at", type = int, nargs = "?", default = 0)
    parser.add_argument("-rse", "--rgb-shift-end-at", type = int, nargs = "?", default = UINT32_MAX)

    parser.add_argument("-z", "--zoom", default = False, action = BooleanOptionalAction)
    parser.add_argument("-zf", "--zoom-factor", type = int, nargs = "?", default = DEFAULT_ZOOM_FACTOR)
    parser.add_argument("-zx", "--zoom-center-x", type = int, nargs = "?", default = DEFAULT_ZOOM_CENTER_X)
    parser.add_argument("-zy", "--zoom-center-y", type = int, nargs = "?", default = DEFAULT_ZOOM_CENTER_Y)

    parser.add_argument("-zl", "--zoom-alpha", type = float, nargs = "?", default = DEFAULT_ZOOM_ALPHA)

    parser.add_argument("-zs", "--zoom-start-at", type = int, nargs = "?", default = 0)
    parser.add_argument("-ze", "--zoom-end-at", type = int, nargs = "?", default = UINT32_MAX)

    parser.add_argument("-za", "--zoom-active", type = int, nargs = "?", default = DEFAULT_ZOOM_PAUSE)
    parser.add_argument("-zp", "--zoom-pause", type = int, nargs = "?", default = DEFAULT_ZOOM_PAUSE)
    parser.add_argument("-zip", "--zoom-invert-pause", default = False, action = BooleanOptionalAction)

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
