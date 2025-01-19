import os
import subprocess
    
def generate_calc_duration_cmd(video_obj):
    """
    Returns a command to calculate a video's duration using FFProbe.
    """
    return [
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", video_obj.video_upload.path
    ]
    
def calc_duration(video_obj):
    """
    Calculates a video's duration by running FFProbe and returning the program's output.
    """
    return subprocess.run(
        generate_calc_duration_cmd(video_obj),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def generate_playlist_basename(video_obj, height):
    """
    Returns a playlist basename designating the video instance and the vertical resolution.
    """
    return f"{video_obj.pk}_{height}p"

def generate_single_resolution_cmd(video_obj, index, resolution):
    """
    Returns a command to convert a video upload to a single selected resolution and bitrate.
    """
    base_name = f"{video_obj.video_files_abs_dir}/{generate_playlist_basename(video_obj, resolution['height'])}"
    segment_filename = base_name + '_%03d.ts'
    playlist_filename = base_name + '.m3u8'
    return [
        f"-filter:v:{index}", f"scale=w={resolution['width']}:h={resolution['height']}",
        "-c:a", "aac", "-ar", "48000", "-b:a", "128",
        f"-c:v:{index}", "libx264", f"-b:v:{index}", f"{resolution['bitrate']}k", "-preset", "fast",
        "-keyint_min", "48", "-g", "48", "-sc_threshold", "0",
        "-hls_time", "4", "-hls_playlist_type", "vod",
        "-hls_segment_filename", segment_filename, playlist_filename,
    ]

def delete_source_video(video_obj):
    """
    Deletes the source video upload associated with a video instance.
    """
    if video_obj.video_upload:
        if os.path.isfile(video_obj.video_upload.path):
            os.remove(video_obj.video_upload.path)