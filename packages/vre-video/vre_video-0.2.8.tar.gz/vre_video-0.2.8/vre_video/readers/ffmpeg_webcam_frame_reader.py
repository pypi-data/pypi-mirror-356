"""ffmpeg_webcam_frame_reader - module for ffmopeg-based webcam functionality"""
from pathlib import Path
import subprocess
import numpy as np
from .frame_reader import FrameReader
from ..utils import logger

class FFmpegWebcamFrameReader(FrameReader):
    """Implements FrameReader using ffmpeg for webcams from /dev/videoX"""
    def __init__(self, data: str | Path, resolution: tuple[int, int]=(480, 640), fps: int=30):
        assert isinstance(data, (str, Path)), type(data)
        super().__init__()
        self.data = data
        self._fps = fps
        self.resolution = (self.height, self.width) = resolution
        self.process: subprocess.Popen = self._start_ffmpeg(data)

    @property
    def shape(self) -> tuple[int, int, int, int]:
        return (1, self.height, self.width, 3)

    @property
    def fps(self):
        return self._fps

    @property
    def path(self) -> str:
        return str(self.data)

    def _start_ffmpeg(self, data: str | Path) -> subprocess.Popen:
        cmd = [
            "ffmpeg",
            "-f", "v4l2",
            "-framerate", f"{self.fps}",
            "-video_size", f"{self.width}x{self.height}",
            "-i", str(data),
            "-pix_fmt", "rgb24",
            "-f", "rawvideo",
            "-"
        ]
        logger.debug(f"Running '{' '.join(cmd)}'")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        return proc

    def __getitem__(self, ix: int | list[int] | np.ndarray | slice) -> np.ndarray:
        raw_frame = self.process.stdout.read(self.width * self.height * 3)
        if not raw_frame:
            return np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((self.height, self.width, 3))
        if isinstance(ix, list):
            assert len(ix) == 1, f"cannot have batches in webcam, got: {ix}"
            frame = frame[None]
        return frame
