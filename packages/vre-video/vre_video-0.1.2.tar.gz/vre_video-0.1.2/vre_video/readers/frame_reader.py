"""frame_reader module. Other readers will implement these methods."""
from abc import ABC, abstractmethod
import numpy as np

class FrameReader(ABC):
    """FrameReader - defines the interface of a reader"""
    @property
    @abstractmethod
    def shape(self) -> tuple[int, int, int, int]:
        """Returns the (N, H, W, 3) tuple of the video"""

    @property
    @abstractmethod
    def fps(self) -> float:
        """The frame rate of the video"""

    @abstractmethod
    def get_one_frame(self, ix: int) -> np.ndarray:
        """Gets one frame from the video"""

    @property
    def frame_shape(self):
        """The frame shape"""
        return self.shape[0]

    def __getitem__(self, ix: int | list[int] | np.ndarray | slice) -> np.ndarray:
        if isinstance(ix, np.ndarray):
            return self[ix.tolist()]
        if isinstance(ix, list):
            return np.array([self[_ix] for _ix in ix])
        if isinstance(ix, slice):
            return np.array([self[_ix] for _ix in range(ix.start, ix.stop)])
        return self.get_one_frame(ix)

    def __len__(self):
        return self.shape[0]
