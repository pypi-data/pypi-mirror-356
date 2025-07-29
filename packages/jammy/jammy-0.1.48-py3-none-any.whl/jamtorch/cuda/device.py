from __future__ import annotations

import torch

import jamtorch.prototype as jampt
from jammy.utils.gpu import gpu_by_weight
from jamtorch.logging import logger as log

__all__ = [
    "set_best_device",
]


def set_best_device(mem_prior=1.0):
    gpu_id = gpu_by_weight(mem_prior)[0]
    log.critical(f"select device: CUDA{gpu_id} ")
    torch.cuda.set_device(gpu_id)
    jampt.set_gpu_mode(True, gpu_id)
    return gpu_id
