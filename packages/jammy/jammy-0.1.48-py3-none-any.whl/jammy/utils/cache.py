#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : cache.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 01/19/2018
#
# Qinsheng Zhang modified based on Jacinle.
# Distributed under terms of the MIT license.

import collections
import functools
import os.path as osp
import threading
from typing import Callable

from jammy.logging import get_logger

from .meta import synchronized

logger = get_logger()

__all__ = ["cached_property", "cached_result", "fs_cached_result"]


def cached_property(fget):
    """A decorator that converts a function into a cached property. Similar to ``@property``, but the function result is cached. This function has threading lock support."""

    mutex = collections.defaultdict(threading.Lock)
    cache = dict()

    def impl(self):
        nonlocal impl
        id_ = id(self)
        with mutex[id_]:
            if id_ not in cache:
                cache[id_] = fget(self)
                return cache[id_]
            else:
                return cache[id_]

    return property(impl)


def cached_result(func):
    """A decorator that caches the result of a function. Note that this decorator does not support any arguments to the function."""

    def impl():
        nonlocal impl
        ret = func()
        impl = lambda: ret
        return ret

    @synchronized()
    @functools.wraps(func)
    def f():
        return impl()

    return f


def fs_cached_result(
    filename: str, force_update: bool = False, verbose: bool = False
) -> Callable[[Callable], Callable]:
    """A decorator that caches the result of a function into a file. Note that this decorator does not take care of any arguments to the function.

    Args:
        filename: the filename to store the result.
        force_update: if True, the result will be updated even if the file exists.
        verbose: if True, the filenames will be printed to the console.

    Returns:
        a decorator function.
    """
    import jammy.io as io

    def wrapper(func):
        @synchronized()
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            if not force_update and osp.exists(filename):
                if verbose:
                    logger.info('Using cached results from "{}".'.format(filename))
                cached_value = io.load(filename)
                if cached_value is not None:
                    return cached_value

            computed_value = func(*args, **kwargs)
            if verbose:
                logger.info('Writing result cache to "{}".'.format(filename))
            io.dump(filename, computed_value)
            return computed_value

        return wrapped_func

    return wrapper
