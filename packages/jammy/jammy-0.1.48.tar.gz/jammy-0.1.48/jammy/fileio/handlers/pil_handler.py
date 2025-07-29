# pylint: disable=import-outside-toplevel

from typing import IO, Optional, Tuple, Union

import numpy as np

from .base import BaseFileHandler

try:
    from PIL import Image
except ImportError:
    Image = None


class PILHandler(BaseFileHandler):
    str_like = False

    def load_from_fileobj(
        self,
        file: IO[bytes],
        fmt: str = "pil",
        size: Optional[Union[int, Tuple[int, int]]] = None,
        **kwargs,
    ):
        """
        Load an image from a file-like object and return it in a specified format.

        Args:
            file (IO[bytes]): A file-like object containing the image data.
            fmt (str): The format to convert the image into. Options are \
                'numpy', 'np', 'npy', 'type' (all return numpy arrays), \
                    'pil' (returns PIL Image), 'th', 'torch' (returns a torch tensor).
            size (Optional[Union[int, Tuple[int, int]]]): The new size of the image as a single integer \
                or a tuple of (width, height). If specified, the image is resized accordingly.
            **kwargs: Additional keyword arguments that can be passed to conversion functions.

        Returns:
            Image data in the format specified by `fmt`.

        Raises:
            IOError: If the image cannot be loaded or processed.
            ValueError: If the specified format is unsupported.
        """
        try:
            img = Image.open(file)
            img.load()  # Explicitly load the image data
            if size is not None:
                if isinstance(size, int):
                    size = (
                        size,
                        size,
                    )  # create a tuple if only one integer is provided
                img = img.resize(size, Image.ANTIALIAS)

            # Return the image in the requested format
            if fmt in ["numpy", "np", "npy"]:
                return np.array(img, **kwargs)
            if fmt == "pil":
                return img
            if fmt in ["th", "torch"]:
                import torch

                # Convert to tensor
                img_tensor = torch.from_numpy(np.array(img, **kwargs))
                # Convert image from HxWxC to CxHxW
                if img_tensor.ndim == 3:
                    img_tensor = img_tensor.permute(2, 0, 1)
                return img_tensor
            raise ValueError(
                "Unsupported format. Supported formats are 'numpy', 'np', 'npy', 'pil', 'th', and 'torch'."
            )
        except Exception as e:
            raise IOError(f"Unable to load image: {e}") from e

    def dump_to_fileobj(self, obj, file: IO[bytes], **kwargs):
        obj.save(file, **kwargs)

    def dump_to_str(self, obj, **kwargs):
        raise NotImplementedError
