import functools
from contextlib import contextmanager

import torch.distributed as dist

__all__ = [
    "print0",
    "get_rank",
    "get_world_size",
    "is_rank0",
    "is_dist",
    "rank0_first",
    "rank0_only",
    "get_world_size",
    "barrier",
]


def print0(*args, **kwargs):
    if get_rank() == 0:
        print(*args, **kwargs)


def get_rank():
    return dist.get_rank() if dist.is_initialized() else 0


def get_world_size():
    return dist.get_world_size() if dist.is_initialized() else 1


def is_rank0():
    return not dist.is_initialized() or dist.get_rank() == 0


def is_dist():
    return dist.is_initialized()


def barrier():
    if is_dist():
        dist.barrier()


@contextmanager
def rank0_first():
    if not is_rank0():
        barrier()
    yield
    if dist.is_initialized() and is_rank0():
        barrier()


def rank0_only(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):  # pylint: disable=inconsistent-return-statements
        if is_rank0():
            return func(*args, **kwargs)
        return

    return new_func
