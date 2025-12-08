from ffmpy import FFprobe
from tempfile import TemporaryFile

def ffprobe_get(input, parameters):
    fprobe_command = FFprobe(
        global_options = [
            "-hide_banner",
            "-v", "error"
        ],
        inputs = {input: [
            "-select_streams", "v:0",
            "-show_entries", f"stream={parameters}",
            "-of", "csv=s=x:p=0"
        ]}
    )

    # This stupid workaround is required because ffmpy returs None from an ffprobe call.
    # Supposedly this should only happen if the output was redirected to a devnull-type sink
    # (Or not redirected at all),
    # But in practice, even when redirecting a file, it still returns None.
    # We really need a better bindings lib for FFMPEG.

    with TemporaryFile(mode = "w+t") as tmpfile:
        fprobe_command.run(stdout = tmpfile)
        tmpfile.seek(0)
        result = tmpfile.read().strip()

    return result

def get_resolution(input):
    return ffprobe_get(input, "width, height")

def get_fps(input):
    fps_fraction = ffprobe_get(input, "r_frame_rate")
    num, den = fps_fraction.split("/")

    return int(num) / int(den)
