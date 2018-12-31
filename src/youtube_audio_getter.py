from typing import List

from pytube import YouTube

from src.audio_getter import AudioGetter
from src.audio_file import AudioFile


class YoutubeAudioGetter(AudioGetter):
    def get_audio(self, url: str, part_len: int = 0) -> List[AudioFile]:
        video = YouTube(url)

        video.streams.filter(only_audio=True).first().download()

        pass
