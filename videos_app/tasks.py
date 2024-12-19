import os
import subprocess
import re
from .utils import generate_playlist_basename, generate_single_resolution_cmd, delete_source_video

RESOLUTIONS = [
    { "width": 640, "height": 360, "bitrate": 1000 },
    { "width": 853, "height": 480, "bitrate": 1500 },
    { "width": 1280, "height": 720, "bitrate": 3000 },
    { "width": 1920, "height": 1080, "bitrate": 5000 }
]

def set_video_duration(video_obj):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", video_obj.video_upload.path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise ValueError(f"ffprobe error: {result.stderr}")
        duration = float(result.stdout.strip())
        video_obj.duration_in_seconds = duration
        video_obj.save()
    except Exception as e:
        raise ValueError(f"Error when identifying the video duration: {e}")

def create_master_playlist(video_obj):
    """
    Combines multiple HLS playlist files into a single master playlist.

    :param playlists: List of dictionaries with 'file' (playlist path) and 'resolution' (e.g., "480p").
    :param output_file: Path to the output master playlist file.
    """
    master_playlist_lines = ["#EXTM3U", "#EXT-X-VERSION:3"]
    resolution_lookup = {f"{res['height']}p": res['bitrate'] * 1000 for res in RESOLUTIONS}
    for res in RESOLUTIONS:
        resolution = f'{res['height']}p'
        playlist_filename = f'{generate_playlist_basename(video_obj, res['height'])}.m3u8'
        bandwidth = resolution_lookup.get(resolution, 1000000)
        master_playlist_lines.append(
            f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}"
        )
        master_playlist_lines.append(playlist_filename)
    output_file = f'{video_obj.video_files_abs_dir}/{video_obj.pk}_master.m3u8'
    with open(output_file, "w") as f:
        f.write("\n".join(master_playlist_lines) + "\n")

def convert_video_to_hls(video_obj):
    os.makedirs(video_obj.video_files_abs_dir, exist_ok=True)
    for i, res in enumerate(RESOLUTIONS):
        cmd = ["ffmpeg", "-i", video_obj.video_upload.path]
        cmd.extend(generate_single_resolution_cmd(video_obj=video_obj, index=i, resolution=res))
        subprocess.run(cmd, capture_output=True, check=True)
    create_master_playlist(video_obj)
    delete_source_video(video_obj)