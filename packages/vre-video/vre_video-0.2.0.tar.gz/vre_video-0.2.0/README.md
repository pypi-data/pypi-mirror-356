# FFmpeg Video

A python video reader that can read video frames using ffmpeg behind the scenes.

Install (pip):
```bash
pip install vre-video
```

Install (dev):
```bash
git clone https://gitlab.com/meehai/ffmpeg-video/
echo "$(pwd)/ffmpeg-video" >> ~/.bashrc
source ~/.bashrc
pip install -r ffmpeg-video/requirements.txt
```

Handle venv/conda/uv stuff on your own!

Usage:
```python
from vre_video import VREVideo
video = VREVideo("video.mp4")
frame = video[ix] # returns a numpy array
```

Supports 3 backends for both reading and writing: `numpy`, `Pillow` and `ffmpeg`. It will auto-detect based on input: if a directory is provided it'll try to guess (png/jpg/npz/npy etc.) assuming it's a dir of frames (1.npz, ..., N.npz). If it's a path with suffix (i.e. .mp4, .mkv etc.) it will use the ffmpeg-based variant. Same for writing.

### Support for youtube videos

Requires `youtube-dl` python package.

Usage:
```python
from vre_video import VREVideo
video = VREVideo("https://www.youtube.com/...")
frame = video[ix] # returns a numpy array
```
