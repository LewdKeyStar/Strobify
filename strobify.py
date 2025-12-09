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

from src.parser_utils import register_feature
from src.feature_list import features

from src.name_utils import is_gif, to_output_name
from src.constants import DEFAULT_OUTPUT

def appropriate_filters(args, *, resolution, fps):
    all_filters = [
        invert_filter(
            args.strobe_start_at,
            args.strobe_end_at,

            args.strobe_every,

            args.strobe_pause,
            args.strobe_active,
            args.strobe_invert_pause
        ) if args.strobe else "",

        rgbshift_filter(
            args.rgb_shift_intensity,

            args.rgb_shift_start_at,
            args.rgb_shift_end_at,

            args.rgb_shift_every,

            args.rgb_shift_pause,
            args.rgb_shift_active,
            args.rgb_shift_invert_pause
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

            args.zoom_every,

            args.zoom_pause,
            args.zoom_active,
            args.zoom_invert_pause
        ) if args.zoom else "",

        palette_filter() if is_gif(args.input) else ""
    ]

    return ",".join([
        filter for filter in all_filters if filter != ""
    ])

def main():
    parser = ArgumentParser()

    parser.add_argument("input")
    parser.add_argument("-o", "--output", nargs = "?", default = DEFAULT_OUTPUT)

    for feature in features:
        register_feature(parser, feature)

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
