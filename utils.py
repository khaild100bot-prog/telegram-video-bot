
import re
import os
from uuid import uuid4
from yt_dlp import YoutubeDL

def is_video_url(url):
    pattern = re.compile(
        r'(https?://)?(www\.)?(tiktok\.com|instagram\.com|youtube\.com|youtu\.?be|facebook\.com|fb\.watch|twitter\.com|x\.com|reddit\.com)/.+'
    )
    return bool(pattern.match(url))

def download(url):
    unique_id = str(uuid4())
    output_dir = 'downloads'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    file_path = os.path.join(output_dir, f"{unique_id}.%(ext)s")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        actual_filename = ydl.prepare_filename(info)
        return actual_filename
