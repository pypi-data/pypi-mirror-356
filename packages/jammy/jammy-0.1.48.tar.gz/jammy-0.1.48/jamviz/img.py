import matplotlib.pyplot as plt
import numpy as np
import torch as th
from einops import rearrange
from PIL import Image
from torchvision.utils import make_grid

__all__ = [
    "show_batch_img",
    "save_batch_img",
    "show_imgs_traj",
]


def _reshape_viz_batch_img(img_data, shape=7):
    """
    Reshapes the visualization batch image.

    :param img_data: The input image data.
    :param shape: The shape of the output image grid. Can be an integer or a string in the format "x".
    :return: The reshaped image, number of rows, and number of columns.
    :raises RuntimeError: If the shape is not supported.
    """
    if isinstance(shape, int):
        nrow, ncol = shape, shape
    elif isinstance(shape, str):
        if "x" not in shape:
            nrow, ncol = int(shape), int(shape)
        else:
            shape = shape.split("x")
            nrow, ncol = int(shape[0]), int(shape[1])
    else:
        raise RuntimeError(f"shape {shape} not support")
    if isinstance(img_data, th.Tensor):
        assert img_data.shape[1] in [1, 3]
        grid_img = make_grid(img_data[: nrow * ncol].detach().cpu(), ncol)
        img = grid_img.permute(1, 2, 0)
    elif isinstance(img_data, np.ndarray):
        if img_data.shape[1] in [1, 3]:
            img = rearrange(
                img_data[: nrow * ncol], "(b t) c h w -> (b h) (t w) c", b=nrow
            )
        else:
            img = rearrange(
                img_data[: nrow * ncol], "(b t) h w c -> (b h) (t w) c", b=nrow
            )
    return img, nrow, ncol


def show_batch_img(img_data, shape=7, grid=3, is_n1p1=False, auto_n1p1=True):
    """
    Displays a batch of images.

    :param img_data: The batch of images to display.
    :param shape: The shape of the grid to display the images in. Default is 7.
    :param grid: The size of each image in the grid. Default is 3.
    :param is_n1p1: Whether the image data is in the range of -1 to 1. Default is False.
    :param auto_n1p1: Whether to automatically adjust the image data to the range of -1 to 1. Default is True.
    """
    if is_n1p1:
        img_data = (img_data + 1) / 2
    else:
        if auto_n1p1:
            if isinstance(img_data, th.Tensor):
                if img_data.min().item() < -0.5:
                    img_data = (img_data + 1) / 2
            elif isinstance(img_data, np.ndarray):
                if np.min(img_data) < -0.5:
                    img_data = (img_data + 1) / 2
    img, nrow, ncol = _reshape_viz_batch_img(img_data, shape)
    plt.figure(figsize=(ncol * grid, nrow * grid))
    plt.axis("off")
    plt.imshow(img)


def save_batch_img(fpath, img_data, shape=7):
    """
    Saves a batch of images to a file.

    :param fpath: The file path to save the images.
    :param img_data: The batch of images to save.
    :param shape: The shape of the images in the batch (default is 7).
    """
    img, _, _ = _reshape_viz_batch_img(img_data, shape)
    if isinstance(img, np.ndarray):
        img = th.from_numpy(img)
    ndarr = img.mul(255).add_(0.5).clamp_(0, 255).to("cpu", th.uint8).numpy()
    im = Image.fromarray(ndarr)
    im.save(fpath)


def show_imgs_traj(traj_batch_img, num_img, num_steps, grid=3, is_n1p1=False, auto_n1p1=True):
    """
    Displays a trajectory of images.

    :param traj_batch_img: The batch of trajectory images.
    :param num_img: The number of images to display per step.
    :param num_steps: The number of steps in the trajectory.
    :param grid: The number of images to display in each row and column.
    :param is_n1p1: Whether the image values are normalized between -1 and 1.
    :param auto_n1p1: Whether to automatically normalize the image values between -1 and 1.
    """
    idx = np.linspace(0, len(traj_batch_img) - 1, num_steps, dtype=int)
    imgs = []
    for cur_idx in idx:
        imgs.append(traj_batch_img[cur_idx][:num_img])
    imgs = th.cat(imgs)

    imgs = rearrange(imgs, "(n b) ... -> (b n) ...", b=num_img)
    show_batch_img(imgs, f"{num_img}x{num_steps}", grid, is_n1p1, auto_n1p1)
