# pylint: disable=import-outside-toplevel,import-error,redefined-builtin,too-many-arguments
from typing import IO

import numpy as np

from .base import BaseFileHandler

try:
    import imageio
except ImportError:
    imageio = None


class ImageioVideoHandler(BaseFileHandler):
    str_like = False

    def load_from_fileobj(
        self, file: IO[bytes], format: str = "mp4", mode: str = "rgb", **kwargs
    ):
        """
        Load video from a file-like object using imageio with specified format and color mode.

        Parameters:
            file (IO[bytes]): A file-like object containing video data.
            format (str): Format of the video file (default 'mp4').
            mode (str): Color mode of the video, 'rgb' or 'gray' (default 'rgb').

        Returns:
            tuple: A tuple containing an array of video frames and metadata about the video.
        """
        file.seek(0)
        video_reader = imageio.get_reader(file, format, **kwargs)

        video_frames = []
        for frame in video_reader:
            if mode == "gray":
                import cv2  # Convert frame to grayscale if mode is gray

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                frame = np.expand_dims(
                    frame, axis=2
                )  # Keep frame dimensions consistent
            video_frames.append(frame)

        return np.array(video_frames), video_reader.get_meta_data()

    def dump_to_fileobj(
        self,
        obj: np.ndarray,
        file: IO[bytes],
        format: str = "mp4",  # pylint: disable=redefined-builtin
        fps: int = 30,
        quality: int = 5,
        **kwargs,
    ):
        """
        Save an array of video frames to a file-like object using imageio.

        Parameters:
            obj (np.ndarray): An array of frames to be saved as video.
            file (IO[bytes]): A file-like object to which the video data will be written.
            format (str): Format of the video file (default 'mp4').
            fps (int): Frames per second of the output video (default 30).

        """
        # with imageio.get_writer(file, format=format, fps=fps, **kwargs) as writer:
        #     for frame in obj:
        #         writer.append_data(frame)
        h, w = obj.shape[1:-1]
        kwargs = {
            "fps": fps,
            "quality": quality,
            "macro_block_size": 1,
            "ffmpeg_params": ["-s", f"{w}x{h}"],
            "output_params": ["-f", "mp4"],
        }
        imageio.mimsave(file, obj, format, **kwargs)

    def dump_to_str(self, obj, **kwargs):
        raise NotImplementedError
