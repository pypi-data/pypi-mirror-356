"""ffmpeg_frame_writer - Module that implements frame writing using ffmpeg"""
from pathlib import Path
import os
from tqdm import trange
import ffmpeg

from .frame_writer import FrameWriter

class FFmpegFrameWriter(FrameWriter):
    """FFmpegFrameWriter implementation that writes to disk a video using ffmpeg process"""
    def __init__(self):
        super().__init__()
        self.write_process = None

    def write(self, video: "VREVideo", out_path: Path, start_frame: int = 0, end_frame: int | None = None):
        out_path = Path(out_path)
        assert self.write_process is None, self.write_process
        assert out_path.suffix == ".mp4", out_path
        assert isinstance(start_frame, int) and start_frame >= 0, start_frame

        self.write_process = (
            ffmpeg
            .input("pipe:0", format="rawvideo", pix_fmt="rgb24", s=f"{video.shape[2]}x{video.shape[1]}", r=video.fps)
            .output(str(out_path), pix_fmt="yuv420p", vcodec="libx264")
            .overwrite_output()
            .run_async(pipe_stdin=True, pipe_stderr=-3, pipe_stdout=-3) # -3 = subprocess.DEVNULL
        )

        assert not out_path.exists(), out_path
        out_path.parent.mkdir(exist_ok=True, parents=True)
        start_frame = start_frame or 0
        end_frame = end_frame or len(video)
        assert start_frame >= 0 and end_frame <= len(video), (start_frame, end_frame)

        try:
            for i in trange(start_frame, end_frame, disable=os.getenv("VRE_VIDEO_PBAR", "1") == "0",
                            desc=f"[FFmpegFrameWriter] {out_path}"):
                self.write_process.stdin.write(video[i].tobytes())
        finally:
            self.write_process.stdin.close()
            self.write_process.wait()
            self.write_process = None
