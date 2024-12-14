import os

def generate_playlist_basename(video_obj, height):
    return f'{video_obj.pk}_{height}p'

def generate_single_resolution_cmd(video_obj, index, resolution):
    base_name = f'{video_obj.video_files_abs_dir}/{generate_playlist_basename(video_obj, resolution['height'])}'
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
    if video_obj.video_upload:
        if os.path.isfile(video_obj.video_upload.path):
            os.remove(video_obj.video_upload.path)