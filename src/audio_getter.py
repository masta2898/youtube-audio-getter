import random
import string

from abc import ABCMeta
from typing import List

from src.audio_file import AudioFile


class AudioGetter:
    metaclass = ABCMeta

    def get_audio(self, url: str) -> List[AudioFile]:
        pass

    def get_random_string(self, len: int):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(len))
