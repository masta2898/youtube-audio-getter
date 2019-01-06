import random
import string
import logging
from typing import List
from datetime import timedelta

from moviepy.editor import *
from pytube import YouTube

from src.audio_getter import AudioGetter
from src.audio_file import AudioFile


class YoutubeAudioGetter(AudioGetter):
    def __init__(self):
        self.__path = "../media/"
        self.__part_len = 600

    def set_path(self, path):
        self.__path = path

    def get_path(self):
        return self.__path

    def set_part_len(self, part_len):
        self.__part_len = part_len

    def get_part_len(self):
        return self.__part_len

    def __download_video(self, url: str):
        logging.info(f"Downloading video from: {url}")
        video_name = self.__get_random_string(7)

        video = YouTube(url)
        video.streams.filter(only_audio=True).first().download(output_path=self.get_path(), filename=video_name)

        return int(video.length)-2, video.title, video_name

    def __cut_video(self, save_path: str, title: str, name: str, start: int, end: int):
        logging.info(f"Cutting video from: {save_path} from {start} to {end}")
        audio_name = self.__get_random_string(9)

        part_name = "{0}-{1}|{2}".format(timedelta(seconds=start), timedelta(seconds=end), title)
        file_name = "{0}{1}.{2}".format(save_path, name, "mp4")
        target_name = "{0}{1}.{2}".format(save_path, audio_name, "mp3")

        audio = AudioFileClip(file_name).subclip(start, end)
        audio.write_audiofile(target_name)

        return part_name, target_name


    def __get_random_string(self, len: int):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(len))

    def get_audio(self, url: str) -> List[AudioFile]:
        logging.info(f"Getting audio from {url}")
        audio_files = []
        start_part = 0

        part_len = self.get_part_len()
        path = self.get_path()

        video_len, video_title, video_name = self.__download_video(url)

        end_part = video_len if part_len >= video_len else part_len

        segment_nums = int((video_len / 60) // (part_len / 60) + 1)

        for segment_num in range(segment_nums):

            part_name, target_name = self.__cut_video(path, video_title, video_name, start_part, end_part)

            start_part = end_part

            end_part += part_len

            if end_part > video_len:
                end_part = video_len

            with open(target_name, "rb") as file:
                audio_files.append(AudioFile(part_name, file.read()))

            os.remove(target_name)

        logging.info(f"Removing old file {path} with {video_name}")
        os.remove("{0}{1}.{2}".format(path, video_name, "mp4"))
        return audio_files


if __name__ == "__main__":
    obj = YoutubeAudioGetter()

    data = obj.get_audio("https://www.youtube.com/watch?v=w62rEg6PSm8")
