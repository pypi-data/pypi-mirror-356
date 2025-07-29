# FFmpeg Video

A python video reader that can read video frames using ffmpeg behind the scenes.

Install:
```
git clone https://gitlab.com/meehai/ffmpeg-video/
echo "$(pwd)/ffmpeg-video" >> ~/.bashrc
source ~/.bashrc
pip install -r ffmpeg-video/requirements.txt
```

Handle venv/conda/uv stuff on your own!

Usage:
```python
from ffmpeg_video import FFmpegVideo
video = FFmpegVideo("video.mp4")
frame = video[ix] # returns a numpy array
```

TODOs:
- A mid term plan is to get rid of `ffmpeg-python` package and just call `ffmpeg` ourselves.
- Make the generic video class receive `FrameReader` and `FrameWriter` and make `FFmpegVideo` inherit `FrameReader` so we can have different backends for reading/writing.
- More integration tests with actual videos

Potential future API:
```bash
from video_reader import Video
video = Video("video.mp4", backend="ffmpeg") # or read/write_backend ?
frame = video[ix]
```
