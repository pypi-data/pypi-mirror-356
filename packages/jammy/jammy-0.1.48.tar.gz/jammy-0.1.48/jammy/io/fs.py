import contextlib
import glob
import gzip
import json
import os
import os.path as osp
import pickle
import platform
import shutil
import tarfile
from zipfile import ZIP_DEFLATED, ZipFile

import numpy as np
import scipy.io as sio
import six
import yaml
from filelock import FileLock

from jammy.image import imread, imwrite
from jammy.logging import get_logger
from jammy.utils.enum import JamEnum
from jammy.utils.registry import CallbackRegistry, RegistryGroup

from .common import get_ext

# pylint: disable=import-outside-toplevel, import-error

logger = get_logger()

__all__ = [
    "as_file_descriptor",
    "fs_verbose",
    "set_fs_verbose",
    "open",
    "open_txt",
    "open_h5",
    "open_gz",
    "load",
    "load_txt",
    "load_h5",
    "load_pkl",
    "load_pklgz",
    "load_npy",
    "load_npz",
    "load_mat",
    "load_pth",
    "load_yaml",
    "load_json",
    "load_img",
    "load_video",
    "dump",
    "dump_pkl",
    "dump_pklgz",
    "dump_npy",
    "dump_npz",
    "dump_mat",
    "dump_pth",
    "dump_json",
    "dump_img",
    "dump_video",
    "safe_dump",
    "compress",
    "compress_zip",
    "extract",
    "extract",
    "link",
    "mkdir",
    "lsdir",
    "remove",
    "locate_newest_file",
    "move",
    "copy",
    "replace",
    "io_function_registry",
    "latest_time",
]

sys_open = open  # pylint: disable=used-before-assignment


def as_file_descriptor(fd_or_fname, mode="r"):
    if isinstance(fd_or_fname, str):
        return sys_open(fd_or_fname, mode)  # pylint: disable=consider-using-with
    return fd_or_fname


def open_h5(file, mode, **kwargs):
    import h5py

    return h5py.File(file, mode, **kwargs)


def open_txt(file, mode, **kwargs):
    return sys_open(file, mode, **kwargs)  # pylint: disable=consider-using-with


def open_gz(file, mode):
    return gzip.open(file, mode)


def open_tar(file, mode="r"):
    return tarfile.open(file, mode)


def extract_zip(file, *args, **kwargs):
    with ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(*args, **kwargs)


def load_pkl(file, **kwargs):
    with as_file_descriptor(file, "rb") as f:
        try:
            return pickle.load(f, **kwargs)
        except UnicodeDecodeError:
            if "encoding" in kwargs:
                raise
            return pickle.load(f, encoding="latin1", **kwargs)


# pylint: disable=unused-argument
def load_pklgz(file, **kwargs):
    with open_gz(file, "rb") as f:
        return load_pkl(f)


def load_h5(file, **kwargs):
    return open_h5(file, "r", **kwargs)


def load_txt(file, **kwargs):
    with sys_open(file, "r", **kwargs) as f:
        return f.readlines()


def load_npy(file, **kwargs):
    return np.load(file, **kwargs)


def load_npz(file, **kwargs):
    return np.load(file, **kwargs)


def load_mat(file, **kwargs):
    return sio.loadmat(file, **kwargs)


def load_pth(file, **kwargs):
    import torch

    return torch.load(file, **kwargs)


def load_csv(file, **kwargs):
    import pandas as pd

    return pd.read_csv(file, **kwargs)


def load_json(file, **kwargs):
    with sys_open(file, "r") as fp:
        return json.load(fp)


def load_img(file, fmt="npy", size=None, **kwargs):
    img = imread(file, **kwargs)
    if fmt in ["th", "torch"]:
        from torchvision import transforms

        img = transforms.ToTensor()(img)
        if size is not None:
            img = transforms.Resize(size)(img)
    elif fmt in ["np", "npy"]:
        img = np.array(img)
    return img


def load_video(file, size=None, **kwargs):
    """
    Load a video from a file and return it as a numpy array of frames.

    Parameters:
        file (str): Path to the video file.
        size (tuple, optional): Desired size (width, height) to resize each frame.
            If None, frames are not resized.

    Returns:
        np.ndarray: Numpy array containing the video frames in the format \
            (frames, height, width, channels). The frames are returned in RGB format.

    Raises:
        ValueError: If the video file cannot be opened.

    Example:
        >>> video_frames = load_video('path/to/video.mp4', size=(320, 240))
        >>> print(video_frames.shape)
        (num_frames, 240, 320, 3)
    """
    import imageio

    reader = imageio.get_reader(file)
    frames = []

    try:
        for frame in reader:
            if size is not None:
                # Resize frame using imageio's built-in functionality
                frame = imageio.core.util.Array(frame).resize(size)
            frames.append(frame)
    except Exception as e:
        raise ValueError("Failed to load video: " + str(e)) from e
    finally:
        reader.close()

    return np.stack(frames)


def load_yaml(file, **kwargs):
    with sys_open(file, "r") as yamlfile:
        if "Loader" not in kwargs:
            kwargs["Loader"] = yaml.FullLoader
        return yaml.load(yamlfile, **kwargs)  # pylint: disable=no-value-for-parameter


def dump_pkl(file, obj, **kwargs):
    with as_file_descriptor(file, "wb") as f:
        return pickle.dump(obj, f, **kwargs)


def dump_pklgz(file, obj, **kwargs):
    with open_gz(file, "wb") as f:
        return pickle.dump(obj, f)


def dump_yaml(file, obj, **kwargs):
    with sys_open(file, "w") as f:
        return yaml.dump(obj, f)


def dump_json(file, obj, **kwargs):
    with sys_open(file, "w") as f:
        return json.dump(obj, f, **kwargs)


def dump_img(file, obj, **kwargs):
    imwrite(file, obj)


def dump_video(file: str, frames: np.ndarray, fps: int = 30, **kwargs):
    """
    Save a sequence of frames to a video file.

    Parameters:
        file (str): Path where the video file will be saved.
        frames (np.ndarray): Array of frames that make up the video. \
            Frames should be in the format (frames, height, width, channels).
        fps (int, optional): Frames per second of the output video (default: 30).

    Additional keyword arguments are passed to `imageio.get_writer()` \
            allowing customization of codec, bitrate, etc.

    Example:
        >>> frames = np.random.randint(0, 255, (60, 240, 320, 3), dtype=np.uint8)
        >>> dump_video('output_video.mp4', frames, fps=25)
    """
    import imageio

    assert isinstance(frames, np.ndarray), "only support np.array type now"
    with imageio.get_writer(file, fps=fps, **kwargs) as writer:
        for frame in frames:
            writer.append_data(frame)


def dump_npy(file, obj, **kwargs):
    return np.save(file, obj)


def dump_npz(file, obj, **kwargs):
    return np.savez(file, obj)


def dump_mat(file, obj, **kwargs):
    return sio.savemat(file, obj, **kwargs)


def dump_pth(file, obj, **kwargs):
    import torch

    return torch.save(obj, file)


def dump_csv(file, obj, **kwargs):
    import pandas as pd

    # Handle dictionary
    if isinstance(obj, dict):
        pd.DataFrame.from_dict(obj).to_csv(file, **kwargs)

    # Handle list
    elif isinstance(obj, list):
        # Assuming list of dicts for each row or simple list for single column
        if all(isinstance(i, dict) for i in obj):
            pd.DataFrame(obj).to_csv(file, **kwargs)
        else:
            pd.DataFrame(obj, columns=[kwargs.get("column_name", "value")]).to_csv(
                file, **kwargs
            )

    # Handle DataFrame directly
    elif isinstance(obj, pd.DataFrame):
        obj.to_csv(file, **kwargs)

    # Handle other types (e.g., numpy array)
    else:
        pd.DataFrame(obj).to_csv(file, **kwargs)


def compress_zip(  # pylint: disable=inconsistent-return-statements
    file, file_list, verbose=True, **kwargs
):
    from jammy.cli import yes_or_no

    with ZipFile(file, "w", ZIP_DEFLATED) as cur_zip:
        for l_file in file_list:
            try:
                cur_zip.write(l_file)
            except FileNotFoundError:
                is_continue = yes_or_no(f"Missing {l_file}, continue?")
                if is_continue:
                    pass
                else:
                    return None


class _IOFunctionRegistryGroup(RegistryGroup):
    __base_class__ = CallbackRegistry

    def dispatch(self, registry_name, file, *args, **kwargs):
        entry = get_ext(file)
        callback = self.lookup(
            registry_name, entry, fallback=True, default=_default_io_fallback
        )
        return callback(file, *args, **kwargs)


def _default_io_fallback(file, *args, **kwargs):
    raise ValueError('Unknown file extension: "{}".'.format(file))


io_function_registry = _IOFunctionRegistryGroup()
io_function_registry.register("open", ".txt", open_txt)
io_function_registry.register("open", ".h5", open_h5)
io_function_registry.register("open", ".gz", open_gz)
io_function_registry.register("open", "__fallback__", sys_open)

io_function_registry.register("load", ".pkl", load_pkl)
io_function_registry.register("load", ".pickle", load_pkl)
io_function_registry.register("load", ".pklgz", load_pklgz)
io_function_registry.register("load", ".txt", load_txt)
io_function_registry.register("load", ".h5", load_h5)
io_function_registry.register("load", ".npy", load_npy)
io_function_registry.register("load", ".npz", load_npz)
io_function_registry.register("load", ".mat", load_mat)
io_function_registry.register("load", ".cfg", load_pkl)
io_function_registry.register("load", ".yaml", load_yaml)
io_function_registry.register("load", ".yml", load_yaml)
io_function_registry.register("load", ".json", load_json)
io_function_registry.register("load", ".csv", load_csv)
io_function_registry.register("load", ".jpg", load_img)
io_function_registry.register("load", ".png", load_img)
io_function_registry.register("load", ".jpeg", load_img)

io_function_registry.register("dump", ".pkl", dump_pkl)
io_function_registry.register("dump", ".pickle", dump_pkl)
io_function_registry.register("dump", ".pklgz", dump_pklgz)
io_function_registry.register("dump", ".npy", dump_npy)
io_function_registry.register("dump", ".npz", dump_npz)
io_function_registry.register("dump", ".mat", dump_mat)
io_function_registry.register("dump", ".cfg", dump_pkl)
io_function_registry.register("dump", ".yaml", dump_yaml)
io_function_registry.register("dump", ".yml", dump_yaml)
io_function_registry.register("dump", ".json", dump_json)
io_function_registry.register("dump", ".csv", dump_csv)

for torch_type in [".pt", ".pth", ".ckpt"]:
    io_function_registry.register("load", torch_type, load_pth)
    io_function_registry.register("dump", torch_type, dump_pth)

for img_type in [".jpg", ".jpeg", ".png", ".bmp"]:
    io_function_registry.register("load", img_type, load_img)
    io_function_registry.register("dump", img_type, dump_img)

for video_type in [".mp4", ".avi", ".mov", ".webm", ".flv", ".wmv"]:
    io_function_registry.register("dump", video_type, dump_video)
    io_function_registry.register("load", video_type, load_video)

io_function_registry.register("extract", ".zip", extract_zip)
io_function_registry.register("compress", ".zip", compress_zip)


_FS_VERBOSE = False

# pylint: disable=global-statement
@contextlib.contextmanager
def fs_verbose(mode=True):
    global _FS_VERBOSE

    _FS_VERBOSE, mode = mode, _FS_VERBOSE
    yield
    _FS_VERBOSE = mode


def set_fs_verbose(mode=True):
    global _FS_VERBOSE
    _FS_VERBOSE = mode


def open(file, mode, **kwargs):  # pylint: disable=redefined-builtin
    if _FS_VERBOSE and isinstance(file, six.string_types):
        logger.info('Opening file: "{}", mode={}.'.format(file, mode))
    return io_function_registry.dispatch("open", file, mode, **kwargs)


def load(file, **kwargs):
    if _FS_VERBOSE and isinstance(file, six.string_types):
        logger.info('Loading data from file: "{}".'.format(file))
    return io_function_registry.dispatch("load", file, **kwargs)


def dump(file, obj, **kwargs):
    if _FS_VERBOSE and isinstance(file, six.string_types):
        logger.info('Dumping data to file: "{}".'.format(file))
    return io_function_registry.dispatch("dump", file, obj, **kwargs)


def compress(file, obj, **kwargs):
    if _FS_VERBOSE and isinstance(file, six.string_types):
        logger.info('compress data to file: "{}".'.format(file))
    return io_function_registry.dispatch("compress", file, obj, **kwargs)


def extract(file, **kwargs):
    if _FS_VERBOSE and isinstance(file, six.string_types):
        logger.info('extract data to file: "{}".'.format(file))
    return io_function_registry.dispatch("extract", file, **kwargs)


def safe_dump(fname, data, use_lock=True, use_temp=True, lock_timeout=10):
    temp_fname = "temp." + fname
    lock_fname = "lock." + fname

    def safe_dump_inner():
        if use_temp:
            dump(temp_fname, data)
            os.replace(temp_fname, fname)
            return True

        return dump(temp_fname, data)

    if use_lock:
        with FileLock(lock_fname, lock_timeout) as flock:
            if flock.is_locked:
                return safe_dump_inner()

            logger.warning("Cannot lock the file: {}.".format(fname))
            return False

    return safe_dump_inner()


def link(path_origin, *paths, use_relative_path=True):
    for item in paths:
        if os.path.exists(item):
            os.remove(item)
        if use_relative_path:
            src_path = os.path.relpath(path_origin, start=os.path.dirname(item))
        else:
            src_path = path_origin
        try:
            os.symlink(src_path, item)
        except FileExistsError:
            os.unlink(item)
            os.symlink(src_path, item)


def mkdir(path):
    return os.makedirs(path, exist_ok=True)


class LSDirectoryReturnType(JamEnum):
    BASE = "base"
    NAME = "name"
    REL = "rel"
    FULL = "full"
    REAL = "real"


def lsdir(dirname, pattern=None, return_type="full"):
    assert "*" in dirname or "?" in dirname or osp.isdir(dirname)

    return_type = LSDirectoryReturnType.from_string(return_type)
    if pattern is not None:
        files = glob.glob(osp.join(dirname, pattern), recursive=True)
    elif "*" in dirname:
        files = glob.glob(dirname)
    else:
        files = os.listdir(dirname)

    if return_type is LSDirectoryReturnType.BASE:
        return [osp.basename(f) for f in files]
    if return_type is LSDirectoryReturnType.NAME:
        return [osp.splitext(osp.basename(f))[0] for f in files]
    if return_type is LSDirectoryReturnType.REL:
        assert (
            "*" not in dirname and "?" not in dirname
        ), "Cannot use * or ? for relative paths."
        return [osp.relpath(f, dirname) for f in files]
    if return_type is LSDirectoryReturnType.FULL:
        return files
    if return_type is LSDirectoryReturnType.REAL:
        return [osp.realpath(osp.join(dirname, f)) for f in files]

    raise ValueError("Unknown lsdir return type: {}.".format(return_type))


def remove(file):
    if osp.exists(file):
        if osp.isdir(file):
            shutil.rmtree(file, ignore_errors=True)
        if osp.isfile(file):
            os.remove(file)


def copy(src, dst):
    if osp.exists(src):
        if osp.isdir(src):
            _copy = shutil.copytree
        if osp.isfile(src):
            _copy = shutil.copyfile

        _copy(src, dst)


def move(src, dst):
    if osp.exists(src):
        os.rename(src, dst)


def replace(src, dst):
    if osp.exists(src):
        if osp.exists(dst):
            remove(dst)
        os.replace(src, dst)


def locate_newest_file(dirname, pattern):
    files = lsdir(dirname, pattern, return_type="full")
    if len(files) == 0:
        return None
    return max(files, key=osp.getmtime)


def latest_time(fname):
    import datetime

    if platform.system() == "Windows":
        ftime = os.path.getctime(fname)
    else:
        stat = os.stat(fname)
        try:
            ftime = stat.st_birthtime
        except AttributeError:
            # probably on Linux.
            ftime = stat.st_mtime
    return datetime.datetime.fromtimestamp(ftime)
