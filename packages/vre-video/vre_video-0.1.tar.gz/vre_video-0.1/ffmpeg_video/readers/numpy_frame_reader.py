"""numpy_frame_reader - module for NumPy-based functionality"""
from pathlib import Path
from natsort import natsorted
import numpy as np
from .frame_reader import FrameReader

class NumpyFrameReader(FrameReader):
    """Implements FrameReader using NumPy arrays, from memory or from disk (.npy/.npz files)"""
    def __init__(self, data: list[np.ndarray] | np.ndarray | str | Path, fps: int = 1):
        self.data = self._build_data(data)
        self._fps = fps

    @property
    def shape(self) -> tuple[int, int, int, int]:
        return self.data.shape

    @property
    def fps(self):
        return self._fps

    def get_one_frame(self, ix: int) -> np.ndarray:
        return self.data[ix]

    def _build_data(self, data: list[np.ndarray] | np.ndarray | str | Path) -> np.ndarray:
        if isinstance(data, np.ndarray):
            assert data.ndim == 4, f"Expected 4D NumPy array (N, H, W, C), got shape {data.shape}"
            assert data.dtype == np.uint8, f"Expected dtype uint8, got {data.dtype}"
            return data

        if isinstance(data, list):
            _shp = data[0].shape
            assert all(x.shape == _shp for x in data), f"Not all shapes match first image: {_shp}"
            assert all(x.dtype == np.uint8 for x in data), f"Not all data is uint8: {set(x.dtype for x in data)}"
            return np.array(data)

        if isinstance(data, (str, Path)):
            self.path = Path(data)
            assert self.path.exists() and self.path.is_dir(), f"Invalid path: '{self.path}'"

            files = natsorted([p for p in self.path.iterdir() if p.suffix in {".npy", ".npz"}], key=lambda p: p.name)
            suffixes = {f.suffix for f in files}
            assert len(suffixes) == 1, f"Directory must contain only one type of file (.npy or .npz), found: {suffixes}"

            if files[0].suffix == ".npy":
                data_lst: list[np.ndarray] = [np.load(f) for f in files]
            else:
                data_lst: list[np.ndarray] = [np.load(f)["arr_0"] for f in files]

            assert all(x.shape == data_lst[0].shape for x in data_lst), f"Shapes differ: expected {data_lst[0].shape}"
            assert all(x.dtype == np.uint8 for x in data_lst), f"Dtype mismatch: {[x.dtype for x in data_lst]}"
            return np.array(data_lst)

        raise TypeError(f"Data must be a list of np.ndarray, a 4D np.ndarray, or a directory path: Got {type(data)}.")

    def __getitem__(self, ix: int | list[int] | np.ndarray | slice) -> np.ndarray:
        return self.data[ix]
