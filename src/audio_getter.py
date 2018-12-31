from abc import ABCMeta
from typing import List

from src.audio_file import AudioFile


class AudioGetter:
    metaclass = ABCMeta

    def get_audio(self, url: str, part_len: int = 0) -> List[AudioFile]:
        pass
