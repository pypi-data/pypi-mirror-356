from typing import Container, Optional

import torch.distributed as dist
from torch import nn

if dist.is_available():
    from torch.distributed.distributed_c10d import _get_default_group
    from torch.distributed.utils import (
        _sync_module_states,
        _verify_param_shape_across_processes,
    )

__all__ = [
    "sync_model_states",
]


def sync_model_states(
    model: nn.Module,
    process_group: Optional[dist.ProcessGroup] = None,
    src: int = 0,
    params_and_buffers_to_ignore: Optional[Container[str]] = None,
    broadcast_buffers: bool = True,
):
    """
    Synchronizes the parameters and buffers of a model across different processes in a distributed setting.

    This function ensures that all processes in the specified process group have the same initial parameters and
    buffers from the source rank, typically rank 0. It is useful when different processes start with different model
    states and a synchronization is required to ensure consistency across all ranks.

    Args:
        model (nn.Module): The model whose parameters and buffers are to be synchronized.
        process_group (dist.ProcessGroup, optional): The process group for communication. If None,
            the default group is used. Defaults to None.
        src (int, optional): The source rank from which parameters and buffers will be broadcasted.
            Defaults to 0.
        params_and_buffers_to_ignore (Optional[Container[str]], optional): A container of parameter and buffer
            names to exclude from synchronization. Defaults to None, which means all parameters and buffers are
            included.
        broadcast_buffers (bool, optional): Whether to broadcast buffers or not. Defaults to True.

    Side Effects:
        This function modifies the state of the model in-place to synchronize it with the source rank's model state.

    Raises:
        RuntimeError: If the shapes of parameters across processes do not match, a runtime error will be raised.
    """
    if process_group is None:
        process_group = _get_default_group()
    if not params_and_buffers_to_ignore:
        params_and_buffers_to_ignore = set()

    # Build tuple of (module, parameter) for all parameters that require grads.
    modules_and_parameters = [
        (module, parameter)
        for module_name, module in model.named_modules()
        for parameter in [
            param
            # Note that we access module.named_parameters instead of
            # parameters(module). parameters(module) is only needed in the
            # single-process multi device case, where it accesses replicated
            # parameters through _former_parameters.
            for param_name, param in module.named_parameters(recurse=False)
            if param.requires_grad
            and f"{module_name}.{param_name}" not in params_and_buffers_to_ignore
        ]
    ]

    # Deduplicate any parameters that might be shared across child modules.
    memo = set()
    modules_and_parameters = [
        # "p not in memo" is the deduplication check.
        # "not memo.add(p)" is always True, and it's only there to cause "add(p)" if needed.
        (m, p)
        for m, p in modules_and_parameters
        if p not in memo and not memo.add(p)  # type: ignore[func-returns-value]
    ]

    # Build list of parameters.
    parameters = [parameter for _, parameter in modules_and_parameters]

    _verify_param_shape_across_processes(process_group, parameters)

    _sync_module_states(
        module=model,
        process_group=process_group,
        broadcast_bucket_size=int(250 * 1024 * 1024),
        src=src,
        params_and_buffers_to_ignore=params_and_buffers_to_ignore,
        broadcast_buffers=broadcast_buffers,
    )
