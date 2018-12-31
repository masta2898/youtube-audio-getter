from pytube import YouTube

class GetAudio:

    def __init__(self, cut_len=10):
        self.cut_len = cut_len

    def get_youtube_audio(self, link):
        video = YouTube(link)

        video.streams.filter(only_audio=True).first().download()
