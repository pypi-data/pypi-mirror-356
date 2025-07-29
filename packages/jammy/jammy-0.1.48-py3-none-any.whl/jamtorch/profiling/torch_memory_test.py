from __future__ import annotations

import shutil

import pytest
import torch

from jamtorch.profiling.torch_memory import maybe_enable_memory_snapshot


# Simple 2-layer MLP for testing
class TinyNet(torch.nn.Module):
    def __init__(self, in_features=4, hidden=8, out_features=2):
        super().__init__()
        self.net = torch.nn.Sequential(
            torch.nn.Linear(in_features, hidden),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden, out_features),
        )

    def forward(self, x):
        return self.net(x)


@pytest.mark.parametrize("enable_snapshot", [False, True])
def test_forward_backward(tmp_path, enable_snapshot):
    """Ensure forward+backward works with or without memory snapshotting."""
    # Clean out any previous runs
    snapshot_root = tmp_path / "snapshots"
    if snapshot_root.exists():
        shutil.rmtree(snapshot_root)

    # use CPU if no CUDA; snapshot will be noop on CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TinyNet().to(device)
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

    # enter profiling context
    with maybe_enable_memory_snapshot(
        enable_snapshot=enable_snapshot,
        local_path=str(snapshot_root),
        profile_freq=1,
        first_n_rank=5,
        start_step=0,
    ) as profiler:
        # one training step
        optimizer.zero_grad()
        x = torch.randn(5, 4, device=device)
        y = model(x)
        loss = y.pow(2).mean()
        loss.backward()
        optimizer.step()
        # if profiling is enabled, trigger an explicit snapshot step
        if profiler is not None:
            profiler.step()

    # if enabled, we should see at least one snapshot directory
    if enable_snapshot and torch.cuda.is_available():
        dirs = list(snapshot_root.glob("memory_snapshot/iteration_1*"))
        assert dirs, "No memory snapshot directory created"
    else:
        # no directories created
        assert not snapshot_root.exists() or not list(snapshot_root.iterdir())
