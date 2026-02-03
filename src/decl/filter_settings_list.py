from src.decl.settings.enable_settings import enable_settings
from src.decl.settings.filter_bearing_video_settings import filter_bearing_video_settings
from src.decl.settings.filterless_video_settings import filterless_video_settings
from src.decl.settings.meta_settings import meta_settings

video_settings = filter_bearing_video_settings + filterless_video_settings
settings = meta_settings + enable_settings + video_settings

valid_setting_names = [setting.name for setting in settings]
valid_video_setting_filter_names = [setting.name for setting in filter_bearing_video_settings]
