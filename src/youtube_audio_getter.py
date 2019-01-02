from typing import List
from datetime import timedelta

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube

from src.audio_getter import AudioGetter
from src.audio_file import AudioFile


class YoutubeAudioGetter(AudioGetter):

    def get_audio(self, url: str, part_len: int = 600) -> List[AudioFile]:

        dto = []

        video = YouTube(url)
        path = "../media/"

        video.streams.filter(only_audio=True).first().download(output_path=path, filename=video.title)
        video_len = int(video.length)
        start_part = 0

        if part_len >= video_len:
            end_part = video_len
        else:
            end_part = part_len

        segment_nums = int((video_len / 60) // (part_len / 60) + 1)

        for segment_num in range(segment_nums):

            out_name = "{0}|{1}-{2}|{3}".format(segment_num, timedelta(seconds=start_part), timedelta(seconds=end_part), video.title)

            filename = "{0}{1}.{2}".format(path, video.title, "mp4")
            targetname = "{0}{1}.{2}".format(path, out_name, "mp4")

            ffmpeg_extract_subclip(filename, start_part, end_part, targetname=targetname)

            start_part = end_part

            if end_part + part_len > video_len:
                end_part = video_len - start_part
            else:
                end_part += part_len

            dto.append(AudioFile(out_name, open(targetname, "rb")))

        return dto


if __name__ == "__main__":

    obj = YoutubeAudioGetter()

    data = obj.get_audio("https://www.youtube.com/watch?v=hAYnqfpO4K0")

    print(data[0].get_data())



