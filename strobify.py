from os.path import splitext
from ffmpy import FFmpeg
from argparse import ArgumentParser, BooleanOptionalAction

from src.filters import (
    invert_filter,
    palette_filter
)

DEFAULT_OUTPUT = "default" # This is just a placeholder, not an actual filename.
DEFAULT_STROBE_EVERY = 2
DEFAULT_STROBE_PAUSE = 0

def to_output_name(args):
    input_name, input_ext = splitext(args.input)
    return input_name+f'''_strobe_every_{
        args.every
    }{
        f'_pause_{args.pause}' if args.pause > 0 else ''
    }{
        "_inverted" if args.pause > 0 and args.invert_pause else ''
    }'''+input_ext

def appropriate_filters(args):
    return ",".join([
        invert_filter(args.every, args.pause, args.invert_pause),
        palette_filter() if splitext(args.input)[1].lower() == ".gif" else ""
    ])

def main():
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    parser.add_argument("-n", "--every", type = int, nargs = "?", default = DEFAULT_STROBE_EVERY)

    parser.add_argument("-p", "--pause", type = int, nargs = "?", default = DEFAULT_STROBE_PAUSE)
    parser.add_argument("-i", "--invert-pause", default = False, action = BooleanOptionalAction)

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
