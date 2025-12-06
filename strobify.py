from os.path import splitext
from ffmpy import FFmpeg
from argparse import ArgumentParser, BooleanOptionalAction

from src.filters import (
    invert_filter,
    rgbshift_filter,
    palette_filter
)

DEFAULT_OUTPUT = "default" # This is just a placeholder, not an actual filename.
DEFAULT_STROBE_EVERY = 2
DEFAULT_STROBE_PAUSE = 0
DEFAULT_RGB_SHIFT_INTENSITY = 5
DEFAULT_RGB_SHIFT_EVERY = 2

## FFMPEG uses this as its upper bound.

UINT32_MAX = 4294967295

def to_output_name(args):
    input_name, input_ext = splitext(args.input)
    return input_name+f'''_strobe_every_{
        args.every
    }{
        f'_start_from_{args.start_strobe_at}' if args.start_strobe_at > 0 else ''
    }{
        f'_end_at_{args.end_strobe_at}' if args.end_strobe_at < UINT32_MAX else ''
    }{
        f'_pause_{args.pause}' if args.pause > 0 else ''
    }{
        "_inverted" if args.pause > 0 and args.invert_pause else ''
    }{
        (
            f'_rgb_{args.rgb_shift_intensity}px'
            f'_every_{args.rgb_shift_every}'
        ) if args.rgb_shift else ''
    }'''+input_ext

def appropriate_filters(args):
    all_filters = [
        invert_filter(args.start_strobe_at, args.end_strobe_at, args.every, args.pause, args.invert_pause),
        rgbshift_filter(args.rgb_shift_intensity, args.rgb_shift_every) if args.rgb_shift else "",
        palette_filter() if splitext(args.input)[1].lower() == ".gif" else ""
    ]

    return ",".join([
        filter for filter in all_filters if filter != ""
    ])

def main():
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    parser.add_argument("-n", "--every", type = int, nargs = "?", default = DEFAULT_STROBE_EVERY)

    parser.add_argument("-s", "--start-strobe-at", type = int, nargs = "?", default = 0)
    parser.add_argument("-e", "--end-strobe-at", type = int, nargs = "?", default = UINT32_MAX)

    parser.add_argument("-p", "--pause", type = int, nargs = "?", default = DEFAULT_STROBE_PAUSE)
    parser.add_argument("-ip", "--invert-pause", default = False, action = BooleanOptionalAction)

    parser.add_argument("-rgb", "--rgb-shift", default = False, action = BooleanOptionalAction)
    parser.add_argument("-rsi", "--rgb-shift-intensity", type = int, nargs = "?", default = DEFAULT_RGB_SHIFT_INTENSITY)
    parser.add_argument("-rse", "--rgb-shift-every", type = int, nargs = "?", default = DEFAULT_RGB_SHIFT_EVERY)

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
            "-vf", appropriate_filters(args)
        ]}
    )

    print(ff.cmd)

    ff.run()

if __name__ == '__main__':
    main()
