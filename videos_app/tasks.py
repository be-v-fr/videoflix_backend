import os
import subprocess
from .utils import add_suffix_to_filename

def convert_video_quality(source, resolution_in_p):
    target = add_suffix_to_filename(source, f'_{resolution_in_p}p')
    cmd = f'touch {target}'
    cmd = f'ffmpeg -i "{source}" -s hd{resolution_in_p} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    subprocess.run(cmd, capture_output=True)