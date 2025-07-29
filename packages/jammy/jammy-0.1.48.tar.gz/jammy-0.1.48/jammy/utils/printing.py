from __future__ import annotations

import collections
import contextlib
import io
import os
import sys
import threading
from dataclasses import asdict, is_dataclass
from typing import Any, ClassVar, Optional

import numpy as np

from .registry import LockRegistry

__all__ = [
    "PrintToStringContext",
    "SupressPrintCTX",
    "bubbletext",
    "indent_text",
    "kvformat",
    "kvprint",
    "print2format",
    "print_to",
    "print_to_string",
    "stformat",
    "stprint",
]

_DEFAULT_FLOAT_FORMAT = "{:.6f}"


def indent_text(text: str, level: int = 1, indent_format: Optional[str] = None, tabsize: Optional[int] = None) -> str:
    # Replace asserts with ValueError
    if indent_format is not None and tabsize is not None:
        raise ValueError("Cannot provide both indent format and tabsize.")

    if tabsize is not None:
        indent_format = " " * tabsize
    elif indent_format is None:
        indent_format = "  "

    final_indent = indent_format * level
    return final_indent + text.replace("\n", "\n" + final_indent)


def format_printable_data(data: Any, float_format: str = _DEFAULT_FLOAT_FORMAT) -> str:
    t = type(data)
    if t is np.ndarray:
        return f"ndarray{data.shape}, dtype={data.dtype}"
    # Handle torch.tensor
    if "Tensor" in str(t):
        return f"tensor{tuple(data.shape)}, dtype={data.dtype}"
    elif t is float:
        return float_format.format(data)
    else:
        return str(data)


def _process_data_recursive(  # noqa: C901
    data: Any,
    indent: int,
    key: Optional[str],
    max_depth: int,
    indent_format: str,
    end_format: str,
    float_format: str,
    file: Optional[io.TextIOBase],
) -> None:
    """Helper function to process data recursively for stprint."""
    if file is None:
        file = sys.stdout

    def _indent_print(msg: str, indent: int, prefix: Optional[str] = None) -> None:
        print(indent_format * indent, end="", file=file)
        if prefix is not None:
            print(prefix, end="", file=file)
        print(msg, end=end_format, file=file)

    t = type(data)

    if max_depth == 0:
        if t in (tuple, list):
            _indent_print(f"({t.__name__} of length {len(data)}) ...", indent, prefix=key)
        elif is_dataclass(data):
            _indent_print(f"(dataclass {data.__class__.__name__}) ...", indent, prefix=key)
        elif t in (dict, collections.OrderedDict, collections.defaultdict):
            _indent_print(f"(dict of length {len(data)}) ...", indent, prefix=key)
        return

    if t is tuple:
        _indent_print("tuple[", indent, prefix=key)
        for v in data:
            _process_data_recursive(v, indent + 1, None, max_depth - 1, indent_format, end_format, float_format, file)
        _indent_print("]", indent)
    elif t is list:
        _indent_print("list[", indent, prefix=key)
        for v in data:
            _process_data_recursive(v, indent + 1, None, max_depth - 1, indent_format, end_format, float_format, file)
        _indent_print("]", indent)
    elif is_dataclass(data):
        typename = f"dataclass {data.__class__.__name__}"
        data_dict = asdict(data)
        _indent_print(typename + "{", indent, prefix=key)
        for k in sorted(data_dict.keys()):
            v = data_dict[k]
            _process_data_recursive(
                v, indent + 1, f"{k}: ", max_depth - 1, indent_format, end_format, float_format, file
            )
        _indent_print("}", indent)
    elif t in (dict, collections.OrderedDict, collections.defaultdict):
        typename = {
            dict: "dict",
            collections.OrderedDict: "ordered_dict",
            collections.defaultdict: "default_dict",
        }[t]
        _indent_print(typename + "{", indent, prefix=key)
        for k in sorted(data.keys()):
            v = data[k]
            _process_data_recursive(
                v, indent + 1, f"{k}: ", max_depth - 1, indent_format, end_format, float_format, file
            )
        _indent_print("}", indent)
    else:
        _indent_print(format_printable_data(data, float_format=float_format), indent, prefix=key)


def stprint(
    data: Any,
    key: Optional[str] = None,
    indent: int = 0,
    file: Optional[io.TextIOBase] = None,
    indent_format: str = "  ",
    end_format: str = "\n",
    float_format: str = _DEFAULT_FLOAT_FORMAT,
    need_lock: bool = True,
    max_depth: int = 100,
) -> None:
    """
    Structure print.

    Example:
        >>> data = dict(a=np.zeros(shape=(10, 10)), b=3)
        >>> stprint(data)
        dict{
            a: ndarray(10, 10), dtype=float64
            b: 3
        }
    """
    if file is None:
        file = sys.stdout

    with stprint.locks.synchronized(file, need_lock):
        _process_data_recursive(data, indent, key, max_depth, indent_format, end_format, float_format, file)


stprint.locks = LockRegistry()


def stformat(data: Any, key: Optional[str] = None, indent: int = 0, max_depth: int = 100, **kwargs) -> str:
    return print2format(stprint)(data, key=key, indent=indent, need_lock=False, max_depth=max_depth, **kwargs)


def kvprint(
    data: dict,
    indent: int = 0,
    sep: str = " : ",
    end: str = "\n",
    max_key_len: Optional[int] = None,
    file: Optional[io.TextIOBase] = None,
    float_format: str = _DEFAULT_FLOAT_FORMAT,
    need_lock: bool = True,
) -> None:
    if len(data) == 0:
        return

    with kvprint.locks.synchronized(file, need_lock):
        keys = sorted(data.keys())
        lens = list(map(len, keys))
        # Replace if-else with ternary operator
        max_len = max_key_len if max_key_len is not None else max(lens)

        for k in keys:
            print("  " * indent, end="")
            print(
                k + " " * max(max_len - len(k), 0),
                format_printable_data(data[k], float_format=float_format),
                sep=sep,
                end=end,
                file=file,
                flush=True,
            )


kvprint.locks = LockRegistry()


def kvformat(data: dict, indent: int = 0, sep: str = " : ", end: str = "\n", max_key_len: Optional[int] = None) -> str:
    return print2format(kvprint)(data, indent=indent, sep=sep, end=end, max_key_len=max_key_len, need_lock=False)


class PrintToStringContext:
    __global_locks = LockRegistry()
    VALID_TARGETS: ClassVar[set[str]] = {"STDOUT", "STDERR"}

    def __init__(self, target: str = "STDOUT", stream: Optional[io.StringIO] = None, need_lock: bool = True):
        # Replace assert with ValueError
        if target not in self.VALID_TARGETS:
            raise ValueError(f"Target must be one of {self.VALID_TARGETS}")

        self._target = target
        self._need_lock = need_lock
        self._stream = stream if stream is not None else io.StringIO()
        self._stream_lock = threading.Lock()
        self._backup = None
        self._value = None

    def _swap(self, rhs: io.StringIO) -> io.StringIO:
        if self._target == "STDOUT":
            sys.stdout, rhs = rhs, sys.stdout
        else:
            sys.stderr, rhs = rhs, sys.stderr
        return rhs

    def __enter__(self) -> PrintToStringContext:
        if self._need_lock:
            self.__global_locks[self._target].acquire()
        self._backup = self._swap(self._stream)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._stream = self._swap(self._backup)
        if self._need_lock:
            self.__global_locks[self._target].release()

    def _ensure_value(self) -> None:
        if self._value is None:
            self._value = self._stream.getvalue()
            self._stream.close()

    def get(self) -> str:
        self._ensure_value()
        return self._value


def print_to_string(target: str = "STDOUT") -> PrintToStringContext:
    return PrintToStringContext(target, need_lock=True)


@contextlib.contextmanager
def print_to(print_func, target: str = "STDOUT", rstrip: bool = True):
    with PrintToStringContext(target, need_lock=True) as ctx:
        yield
    out_str = ctx.get()
    if rstrip:
        out_str = out_str.rstrip()
    print_func(out_str)


def print2format(print_func):
    def format_func(*args, **kwargs):
        f = io.StringIO()
        print_func(*args, file=f, **kwargs)
        value = f.getvalue()
        f.close()
        return value

    return format_func


def bubbletext(text: str, font: str = "cybermedium") -> str:
    """
    Uses pyfiglet to create bubble text.
    Args:
        font (str): default=cybermedium, other fonts include: cybersmall and
            cyberlarge.
    References:
        http://www.figlet.org/
    """
    try:
        import pyfiglet
    except ImportError:
        from jammy.logging import get_logger

        logger = get_logger()
        logger.debug("Missing pyfiglet when use bubbletext")
        return text
    else:
        bubble_text = pyfiglet.figlet_format(text, font=font)
        return bubble_text


class SupressPrintCTX:
    def __init__(self, stdout: bool = False, stderr: bool = False):
        self._stdout = stdout
        self._stderr = stderr
        self._stdout_backup = None
        self._stderr_backup = None

    def __enter__(self) -> None:
        if self._stdout:
            self._stdout_backup = sys.stdout
            sys.stdout = open(os.devnull, "w")
        if self._stderr:
            self._stderr_backup = sys.stderr
            sys.stderr = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._stdout:
            sys.stdout.close()
            sys.stdout = self._stdout_backup
        if self._stderr:
            sys.stderr.close()
            sys.stderr = self._stderr_backup
