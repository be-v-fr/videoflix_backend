import os
import subprocess
from .utils import generate_video_conversion_cmd, delete_source_video

RESOLUTIONS = (480, 720, 1080)

def convert_video_to_hls(video_obj):
    output_dir = os.path.join("media/videos", f"{video_obj.id}_{video_obj.title}")
    os.makedirs(output_dir, exist_ok=True)
    for resolution in RESOLUTIONS:
        convert_video_to_single_resolution_hls(video_obj, output_dir, resolution)
    delete_source_video(video_obj)

def convert_video_to_single_resolution_hls(video_obj, output_dir, resolution):
    target = os.path.join(output_dir, f"{video_obj.id}_{resolution}p")
    cmd = generate_video_conversion_cmd(
        source=video_obj.video_upload.path,
        target=target,
        resolution=resolution
    )
    subprocess.run(cmd, capture_output=True, check=True)