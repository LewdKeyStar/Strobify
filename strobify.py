from ffmpy import FFmpeg
from argparse import ArgumentParser

from src.ffprobe_utils import (
    get_resolution,
    get_fps
)

from src.feature_list import features
from src.filters import palette_filter

from src.parser_utils import register_feature

from src.name_utils import is_gif, to_output_name
from src.constants import DEFAULT_OUTPUT

def appropriate_filters(args, *, resolution, fps):

    all_filters = [
        *[
            feature_filter(
                args,
                # *[locals()[supp_arg] for supp_arg in feature_filter.supplemental_arguments]
                # ...but that doesn't work for some reason??????
                # It produces a KeyError for "resolution" or "fps".
                # Why????

                # So I have to do this stupid shit instead...
                # TODO : no, seriously, what the actual fuck
                *([resolution, fps] if feature_filter.name == "zoom" else [])
            )
            for feature_filter in features
         ],

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
