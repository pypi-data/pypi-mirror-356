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

    @property
    def frame_shape(self):
        """The frame shape"""
        return self.shape[0]

    @abstractmethod
    def __getitem__(self, ix: int | list[int] | np.ndarray | slice) -> np.ndarray:
        """gets one or more frames"""

    def __len__(self):
        return self.shape[0]
