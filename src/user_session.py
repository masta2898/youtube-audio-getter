from typing import List

from src.audio_file import AudioFile
from src.audio_getter import AudioGetter


class UserSession:
    def __init__(self, user_id: int):
        self.__id = user_id
        self.__audio_getter: AudioGetter = None
        self.__part_len: int = 0

    def set_part_time(self, part_len):
        self.__part_len = part_len

    def get_part_time(self):
        return self.__part_len

    def set_audio_getter(self, audio_getter: AudioGetter):
        self.__audio_getter = audio_getter

    def get_audio(self, url) -> List[AudioFile]:
        audio_files: List[AudioFile] = ()
        if self.__audio_getter:
            audio_files = self.__audio_getter.get_audio(url, self.__part_len)
        return audio_files
