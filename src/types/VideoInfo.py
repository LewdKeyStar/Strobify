from dataclasses import dataclass

from src.utils.ffprobe_utils import get_resolution, get_fps, get_duration

@dataclass
class VideoInfo:

    video_path: str

    def __post_init__(self):
        self.fps = get_fps(self.video_path)
        self.resolution = get_resolution(self.video_path)
        self.duration = get_duration(self.video_path)
