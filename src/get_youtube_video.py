import sys
from pytube import YouTube

class getVideo():
    pass

yt = YouTube('http://youtube.com/watch?v=9bZkp7q19f0')
print(yt.video_id)