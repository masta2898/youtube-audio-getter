from abc import ABCMeta
from typing import List

from src.audio_file import AudioFile


class AudioGetter:
    metaclass = ABCMeta

    def get_audio(self, url: str) -> List[AudioFile]:
        pass
