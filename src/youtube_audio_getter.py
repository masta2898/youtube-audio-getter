from typing import List
from datetime import timedelta

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
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
        video = YouTube(url)
        video.streams.filter(only_audio=True).first().download(output_path=self.get_path(), filename=video.title)
        return int(video.length), video.title

    def __cut_video(self, save_path: str, title: str, start: int, end: int):
        part_name = "{0}-{1}|{2}".format(timedelta(seconds=start), timedelta(seconds=end), title)
        file_name = "{0}{1}.{2}".format(save_path, title, "mp4")
        target_name = "{0}{1}.{2}".format(save_path, part_name, "mp4")

        ffmpeg_extract_subclip(file_name, start, end, targetname=target_name)

        return part_name, target_name

    def get_audio(self, url: str) -> List[AudioFile]:
        start_part = 0

        part_len = self.get_part_len()
        path = self.get_path()

        video_len, video_title = self.__download_video(url)
        end_part = video_len if part_len >= video_len else part_len
        segment_count = int((video_len / 60) // (part_len / 60) + 1)

        audio_files = []
        for segment_num in range(segment_count):
            part_name, target_name = self.__cut_video(path, video_title, start_part, end_part)
            start_part = end_part
            end_part += part_len
            if end_part > video_len:
                end_part = video_len - start_part

            with open(target_name, "rb") as file:
                audio_files.append(AudioFile(part_name, file.read()))

        return audio_files


if __name__ == "__main__":

    obj = YoutubeAudioGetter()

    data = obj.get_audio("https://www.youtube.com/watch?v=_l4XR--u5_g")



