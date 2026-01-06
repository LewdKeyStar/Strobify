from ffmpy import FFmpeg
from argparse import ArgumentParser

from src.types.VideoInfo import VideoInfo

from src.decl.feature_list import features, prioritized_features
from src.impl.misc_filters import palette_filter

from src.utils.parser_utils import register_feature
from src.utils.filter_utils import chain_filters

from src.utils.name_utils import is_gif, to_output_name
from src.constants import DEFAULT_OUTPUT

def appropriate_filters(args, video_info):

    all_filters = [

        *[
            feature_filter(
                args,
                video_info
            )
            for feature_filter in prioritized_features(args)
         ],

        palette_filter() if is_gif(args.output) else ""
    ]

    return chain_filters(all_filters)

def appropriate_filter_audio_components(args, video_info):

    all_audio_components = [

        feature_filter(
            args,
            video_info,
            seeking_audio_component = True
        )

        for feature_filter in prioritized_features(args)
    ]

    return chain_filters(all_audio_components)

def any_audio_filters_enabled(args):
    return any(feature.has_audio_component and feature.is_enabled(args) for feature in features)

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

    video_info = VideoInfo(args.input)

    ff = FFmpeg(
        global_options = "-y",
        inputs = {args.input: None},
        outputs = {args.output: (
            (
                [
                "-vf", appropriate_filters(
                    args,
                    video_info
                )]
            )
            +
            (
                [
                    "-af", appropriate_filter_audio_components(
                        args,
                        video_info
                    )
                ]
                if any_audio_filters_enabled(args)
                else []
            )
        )}
    )

    print(ff.cmd)

    ff.run()

if __name__ == '__main__':
    main()
