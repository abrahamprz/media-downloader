from yt_dlp import YoutubeDL # https://github.com/yt-dlp/yt-dlp#embedding-yt-dlp
import pexpect
import re
import os

NUMBERS_PATTERN = re.compile('[^0-9]|_')

def my_hook(d):
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        print("Done downloading {}".format(file_tuple[1]))  # print()
    if d['status'] == 'downloading':
        download_progress = str(d['_percent_str']).replace('%', '').strip()
        download_progress = re.sub(NUMBERS_PATTERN, '', download_progress)[3:]
        download_progress = float(download_progress) / 100
        print(f'progress: {download_progress}')
    return None

YOUTUBE_REGEX = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
FACEBOOK_REGEX = r'^https?:\/\/www\.facebook\.com.*\/(video(s)?|watch|story)(\.php?|\/).+$'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MP4_YTDLP_OPTIONS = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                     'outtmpl': 'media/video/%(title)s',
                     'progress_hooks': [my_hook],
                     'quiet': True,
                     'progress': True,
}
MP3_YTDLP_OPTIONS = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': 'media/audio/%(title)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}


def downloader(url, format):
    ydl_opts = MP4_YTDLP_OPTIONS if format == 'mp4' else MP3_YTDLP_OPTIONS
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        mediainfo = ydl.extract_info(url=url, download=False)
        filename = str(ydl.prepare_filename(mediainfo))
    if format == 'mp4':
        pexpect.run("{BASH_COMMAND} {FILE} {SIZE_LIMIT} \'{FFMPEG_ARGS}\'".format(
            BASH_COMMAND='sh split-video.sh',
            FILE=filename,
            SIZE_LIMIT='25000000',
            FFMPEG_ARGS='-c:v libx264 -crf 23 -c:a copy -vf scale=960:-1'))


def urlValidation(url):
    if len(url) != 0:
        if re.match(YOUTUBE_REGEX, url) or re.match(FACEBOOK_REGEX, url):
            return True
        else:
            return False
    return None


def process_url(url, format):
    if urlValidation(url):
        if format == 'mp4':
            print('MP4 FORMAT')
            print(BASE_DIR)
            downloader(url=url, format='mp4')
        elif format == 'mp3':
            print('MP3 FORMAT')
            print(BASE_DIR)
            downloader(url=url, format='mp3')
        else:
            print("INVALID FORMAT")
    else:
        print("ERROR WITH URL")


if __name__ == "__main__":
    url = input("Enter the URL: ").strip()
    format = input("Enter the format (mp4/mp3): ").strip()
    process_url(url, format)
