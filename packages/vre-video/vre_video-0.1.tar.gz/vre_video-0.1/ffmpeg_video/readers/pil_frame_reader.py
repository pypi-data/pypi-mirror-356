"""pil_frame_reader - module for PIL-based functionality"""
from pathlib import Path
from natsort import natsorted
import numpy as np
from .frame_reader import FrameReader
from ..utils import image_read

class PILFrameReader(FrameReader):
    """implements FrameReader using Pillow to read frame by frame"""
    def __init__(self, path: str | Path, fps: int = 1):
        self.path = Path(path)
        self.frame_paths = natsorted(list(self.path.iterdir()), key=lambda p: p.name)
        self.data: list[np.ndarray] = [image_read(x) for x in self.frame_paths]
        _shp = self.data[0].shape
        assert all(x.shape == _shp for x in self.data), f"Not all shapes of all images are equal to first image: {_shp}"
        assert all(x.dtype == np.uint8 for x in self.data), f"Not all data is uint8: {set(x.dtype for x in self.data)}"
        self.data = np.array(self.data)
        self._fps = fps

    @property
    def shape(self) -> tuple[int, int, int, int]:
        return (len(self.data), *self.data[0].shape)

    @property
    def fps(self):
        return self._fps

    def get_one_frame(self, ix):
        return self.data[ix]

    def __getitem__(self, ix: int | list[int] | np.ndarray | slice) -> np.ndarray:
        return self.data[ix]
