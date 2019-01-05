from abc import ABCMeta, abstractmethod
from typing import List

from src.audio_file import AudioFile


class AudioGetter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_audio(self, url: str) -> List[AudioFile]:
        pass

