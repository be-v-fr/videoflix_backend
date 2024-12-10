import os

def generate_video_conversion_cmd(source, target, resolution):
    return [
            'ffmpeg', 
            '-i', source, 
            '-c:v', 'libx264', 
            '-crf', '23', 
            '-preset', 'fast', 
            '-c:a', 'aac', 
            '-ar', '44100', 
            '-ac', '2', 
            '-s', f'hd{resolution}', 
            '-f', 'hls', 
            '-hls_time', '10', 
            '-hls_list_size', '0', 
            '-hls_segment_filename', f'{target}_%03d.ts', 
            f'{target}.m3u8'
    ]

def delete_source_video(video_obj):
    if video_obj.video_upload:
        if os.path.isfile(video_obj.video_upload.path):
            os.remove(video_obj.video_upload.path)