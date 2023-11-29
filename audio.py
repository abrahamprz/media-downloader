import re
import yt_dlp

def get_youtube_link():
    while True:
        link = input("Please enter a YouTube link: ")
        if re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', link):
            return [link]
        else:
            print("Invalid YouTube link. Please try again.")

if __name__ == '__main__':
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(get_youtube_link())
        