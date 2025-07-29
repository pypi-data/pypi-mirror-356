"""utils"""
from pathlib import Path
from urllib.request import urlretrieve
import os
import numpy as np
from PIL import Image
from tqdm import tqdm
from loggez import make_logger

logger = make_logger("VRE_VIDEO")

def image_write(file: np.ndarray, path: str):
    """PIL image writer"""
    assert file.min() >= 0 and file.max() <= 255
    img = Image.fromarray(file.astype(np.uint8), "RGB")
    img.save(path)

def image_read(path: str) -> np.ndarray:
    """PIL image reader"""
    # TODO: for grayscale, this returns a RGB image too
    img_pil = Image.open(path)
    img_np = np.array(img_pil, dtype=np.uint8)
    # grayscale -> 3 gray channels repeated.
    if img_pil.mode == "L":
        return np.repeat(img_np[..., None], 3, axis=-1)
    # RGB or RGBA
    return img_np[..., 0:3]

def fetch(url: str, dst: str):
    """fetches data and stores locally with pbar"""
    assert not Path(dst).exists(), f"'{dst}' exists (or is a dir). Remove first or provide destination file path + name"
    class DownloadProgressBar(tqdm):
        """requests + tqdm"""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs, disable=os.getenv("VRE_VIDEO_PBAR", "1") == "0")

        def update_to(self, b=1, bsize=1, tsize=None):
            """Callback from tqdm"""
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)

    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=Path(dst).name) as t:
        try:
            urlretrieve(url, filename=dst, reporthook=t.update_to)
        except Exception as e:
            logger.info(f"Failed to download '{url}' to '{dst}'")
            raise e
