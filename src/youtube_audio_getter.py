from typing import List

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube

from src.audio_getter import AudioGetter
from src.audio_file import AudioFile


class YoutubeAudioGetter(AudioGetter):



    def get_audio(self, url: str, part_len: int = 600) -> List[AudioFile]:
        video = YouTube(url)

        video.streams.filter(only_audio=True).first().download()
        video_len = int(video.length)
        start_part = 0
        end_patr = 600

        segment_nums = int((video_len / 60) // (part_len / 60) + 1)
        print(segment_nums)

        for segment_num in range(segment_nums):
            print("что-то происходит")

            ffmpeg_extract_subclip(video.title + ".mp4", start_part, end_patr, targetname=str(segment_num) + "q.mp4")

            start_part = end_patr

            if end_patr + part_len > video_len:
                end_patr = video_len - start_part
            else:
                end_patr += part_len



if __name__ == "__main__":

    obj = YoutubeAudioGetter()

    obj.get_audio("https://www.youtube.com/watch?v=Bkn57dWdBsI")



