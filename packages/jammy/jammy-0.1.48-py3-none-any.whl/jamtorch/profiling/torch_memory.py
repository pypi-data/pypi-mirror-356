from __future__ import annotations

import os
import time
from contextlib import contextmanager

import torch

from jammy.fileio import io as easy_io
from jamtorch.distributed import get_rank
from jamtorch.logging import logger as log

MEMORY_SNAPSHOT_MAX_ENTRIES = 1024


class MemoryProfiler:
    """Helper to record and dump CUDA memory snapshots at specified intervals."""

    def __init__(
        self,
        start_step: int,
        freq: int,
        snapshot_dir: str,
        first_n_rank: int,
    ) -> None:
        """
        Args:
            start_step: the initial global step counter.
            freq: how often (in steps) to record a snapshot.
            snapshot_dir: local or S3 base directory to save snapshots.
            first_n_rank: only ranks < first_n_rank will dump.
        """
        torch.cuda.memory._record_memory_history(max_entries=MEMORY_SNAPSHOT_MAX_ENTRIES)
        self.step_num = start_step
        self.freq = freq
        self.snapshot_dir = snapshot_dir
        self.first_n_rank = first_n_rank
        self.rank = get_rank()

    def step(self, exit_ctx: bool = False) -> None:
        """Maybe dump a snapshot on this step or at exit due to OOM."""
        self.step_num += 1
        if not exit_ctx and (self.step_num % self.freq != 0):
            return

        curr_step = self.step_num if not exit_ctx else self.step_num - 1
        suffix = "" if not exit_ctx else "_exit"
        dir_name = f"iteration_{curr_step}{suffix}"
        target_dir = os.path.join(self.snapshot_dir, dir_name)

        if not self.snapshot_dir.startswith("s3://"):
            os.makedirs(target_dir, exist_ok=True)

        log.info(f"Dumping memory snapshot at step {curr_step}")
        start = time.monotonic()
        if self.first_n_rank < 0 or self.rank < self.first_n_rank:
            path = os.path.join(target_dir, f"rank{self.rank}_memory_snapshot.pickle")
            easy_io.dump(torch.cuda.memory._snapshot(), path)
        log.info(f"Finished dumping in {time.monotonic() - start:.2f}s")


@contextmanager
def maybe_enable_memory_snapshot(
    enable_snapshot: bool,
    local_path: str,
    profile_freq: int,
    first_n_rank: int,
    start_step: int = 0,
):
    """
    Context manager for CUDA memory snapshotting.

    Args:
        enable_snapshot: master switch to turn profiling on/off.
        local_path: local root for snapshots.
        profile_freq: dump every `profile_freq` steps.
        first_n_rank: only ranks < this will actually dump; set <0 to allow all.
        start_step: initial global step counter.
    Yields:
        MemoryProfiler instance if enabled, else None.
    """
    if not enable_snapshot:
        yield None
        return

    # determine base directory
    snapshot_dir = os.path.join(local_path, "memory_snapshot")
    if get_rank() == 0:
        os.makedirs(snapshot_dir, exist_ok=True)

    log.info(f"Memory profiler active. Snapshot dir: {snapshot_dir}")
    profiler = MemoryProfiler(start_step, profile_freq, snapshot_dir, first_n_rank)
    try:
        yield profiler
    except torch.cuda.OutOfMemoryError:
        # capture at OOM
        profiler.step(exit_ctx=True)
        raise
