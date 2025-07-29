# pylint: disable=redefined-outer-name
"""Tests for TensorSparseSample class.

This module contains comprehensive tests for the TensorSparseSample class,
covering initialization, updates, and various sampling strategies.
"""

import pytest
import torch
from torch import Tensor

from .distribution_sample import TensorSparseSample, get_tensor_stat_info


def test_get_stat_info():
    """Tests the get_stat_info function."""
    tensor = torch.randn(1000)
    stat_info = get_tensor_stat_info(tensor, "Random")
    print(stat_info)


# Test fixtures
@pytest.fixture
def small_1d_tensor() -> Tensor:
    """Creates a small 1D tensor for basic tests."""
    return torch.arange(10, dtype=torch.float32)


@pytest.fixture
def large_1d_tensor() -> Tensor:
    """Creates a larger 1D tensor for testing sampling strategies."""
    return torch.arange(1000, dtype=torch.float32)


@pytest.fixture
def tensor_2d() -> Tensor:
    """Creates a 2D tensor for testing multi-dimensional cases."""
    return torch.arange(100, dtype=torch.float32).reshape(10, 10)


@pytest.fixture
def tensor_3d() -> Tensor:
    """Creates a 3D tensor for testing multi-dimensional cases."""
    return torch.arange(120, dtype=torch.float32).reshape(4, 5, 6)


@pytest.fixture
def basic_sparse_sample(small_1d_tensor: Tensor) -> TensorSparseSample:
    """Creates a basic TensorSparseSample instance."""
    return TensorSparseSample.from_tensor(small_1d_tensor, sample_size=5)


class TestTensorSparseSampleInitialization:
    """Tests for TensorSparseSample initialization."""

    def test_basic_initialization(self):
        """Tests basic initialization with valid inputs."""
        indices = torch.tensor([0, 1, 2])
        sample = TensorSparseSample(indices=indices)
        assert torch.equal(sample.indices, indices)
        assert sample.values is None
        assert sample.ntensor == 0

    def test_initialization_with_values(self):
        """Tests initialization with both indices and values."""
        indices = torch.tensor([0, 1, 2])
        values = torch.tensor([[1.0, 2.0, 3.0]])  # Shape: (1, 3)
        sample = TensorSparseSample(indices=indices, values=values, ntensor=1)
        assert torch.equal(sample.indices, indices)
        assert torch.equal(sample.values, values)
        assert sample.ntensor == 1

    def test_wrong_number_of_values(self):
        """Tests initialization with wrong number of values."""
        indices = torch.tensor([0, 1, 2])
        values = torch.tensor([[1.0, 2.0]])  # Wrong number of values
        with pytest.raises(ValueError, match="Number of values .* must match"):
            TensorSparseSample(indices=indices, values=values)

    def test_wrong_shape_values(self):
        """Tests initialization with wrong shape values (1D instead of 2D)."""
        indices = torch.tensor([0, 1, 2])
        values = torch.tensor([1.0, 2.0, 3.0])  # 1D instead of 2D
        with pytest.raises(ValueError, match="values must be a 2D tensor"):
            TensorSparseSample(indices=indices, values=values)

    def test_wrong_type_values(self):
        """Tests initialization with wrong type values."""
        indices = torch.tensor([0, 1, 2])
        values = [1.0, 2.0, 3.0]  # List instead of tensor
        with pytest.raises(TypeError, match="values must be a torch.Tensor"):
            TensorSparseSample(indices=indices, values=values)

    def test_wrong_type_indices(self):
        """Tests initialization with wrong type indices."""
        indices = [0, 1, 2]  # List instead of tensor
        with pytest.raises(TypeError, match="indices must be a torch.Tensor"):
            TensorSparseSample(indices=indices)


class TestTensorSparseSampleUpdate:
    """Tests for update functionality."""

    def test_single_update(self, small_1d_tensor: Tensor):
        """Tests single update behavior."""
        sample = TensorSparseSample.from_tensor(small_1d_tensor, sample_size=3)
        assert sample.ntensor == 1
        assert sample.values.shape == (1, 3)
        assert torch.equal(sample.values[0], small_1d_tensor[sample.indices])

    def test_multiple_updates(self, small_1d_tensor: Tensor):
        """Tests multiple update behavior."""
        sample = TensorSparseSample.from_tensor(small_1d_tensor, sample_size=3)

        # Second update
        new_tensor = small_1d_tensor + 10
        sample.update(new_tensor)
        assert sample.ntensor == 2
        assert sample.values.shape == (2, 3)
        assert torch.equal(sample.values[1], new_tensor[sample.indices])

        # Third update
        newer_tensor = small_1d_tensor + 20
        sample.update(newer_tensor)
        assert sample.ntensor == 3
        assert sample.values.shape == (3, 3)
        assert torch.equal(sample.values[2], newer_tensor[sample.indices])

    def test_update_different_dim_tensor(self, basic_sparse_sample: TensorSparseSample):
        """Tests update with tensor of different dimensions."""
        tensor_2d = torch.randn(10, 10)
        with pytest.raises(ValueError):
            basic_sparse_sample.update(tensor_2d)

    def test_update_value_consistency(self, small_1d_tensor: Tensor):
        """Tests that values are consistent across updates."""
        sample = TensorSparseSample.from_tensor(small_1d_tensor, sample_size=3)
        values_history = [sample.values[0].clone()]

        for i in range(3):
            new_tensor = small_1d_tensor + (i + 1) * 10
            sample.update(new_tensor)
            values_history.append(sample.values[i + 1].clone())

        # Check each update matches expected values
        for i, values in enumerate(values_history):
            expected_tensor = small_1d_tensor + i * 10
            assert torch.allclose(values, expected_tensor[sample.indices])


class TestSamplingStrategies:
    """Tests for different sampling strategies."""

    @pytest.mark.parametrize("strategy", ["random", "uniform", "edges"])
    def test_sampling_strategies(self, large_1d_tensor: Tensor, strategy: str):
        """Tests different sampling strategies."""
        sample_size = 10
        sample = TensorSparseSample.from_tensor(
            large_1d_tensor, sample_size=sample_size, strategy=strategy
        )

        assert len(sample) == sample_size
        assert sample.values.shape == (1, sample_size)
        assert torch.all(sample.indices < len(large_1d_tensor))

    def test_edges_strategy_distribution(self, large_1d_tensor: Tensor):
        """Tests that edges strategy samples from start, middle, and end."""
        sample = TensorSparseSample.from_tensor(
            large_1d_tensor, sample_size=9, strategy="edges"
        )

        indices = sample.indices.cpu().numpy()
        n = len(large_1d_tensor)

        # Check if we have samples from each third
        assert any(idx < n / 3 for idx in indices)  # Start
        assert any(n / 3 <= idx < 2 * n / 3 for idx in indices)  # Middle
        assert any(idx >= 2 * n / 3 for idx in indices)  # End

    def test_uniform_strategy_spacing(self, large_1d_tensor: Tensor):
        """Tests that uniform strategy has consistent spacing."""
        sample = TensorSparseSample.from_tensor(
            large_1d_tensor, sample_size=5, strategy="uniform"
        )

        diffs = sample.indices[1:] - sample.indices[:-1]
        assert torch.allclose(diffs, diffs[0] * torch.ones_like(diffs))


class TestMultiDimensionalTensors:
    """Tests for handling multi-dimensional tensors."""

    @pytest.mark.parametrize("tensor_fixture", ["tensor_2d", "tensor_3d"])
    def test_multi_dim_sampling(self, tensor_fixture: str, request):
        """Tests sampling from multi-dimensional tensors."""
        tensor = request.getfixturevalue(tensor_fixture)
        sample = TensorSparseSample.from_tensor(tensor, sample_size=5)

        # Check indices shape
        assert sample.indices.shape[0] == 5  # number of samples
        assert sample.indices.shape[1] == tensor.dim()  # number of dimensions
        assert sample.values.shape == (1, 5)  # (ntensor, n_samples)

        # Verify values match
        values = []
        for idx in sample.indices:
            values.append(tensor[tuple(idx.tolist())])
        expected_values = torch.stack(values)
        assert torch.equal(sample.values[0], expected_values)

    def test_multi_dim_updates(self, tensor_2d: Tensor):
        """Tests updates with multi-dimensional tensors."""
        sample = TensorSparseSample.from_tensor(tensor_2d, sample_size=5)
        new_tensor = tensor_2d + 10

        sample.update(new_tensor)
        assert sample.ntensor == 2
        assert sample.values.shape == (2, 5)

        # Verify new values match
        values = []
        for idx in sample.indices:
            values.append(new_tensor[tuple(idx.tolist())])
        expected_values = torch.stack(values)
        assert torch.equal(sample.values[1], expected_values)


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_strategy(self, small_1d_tensor: Tensor):
        """Tests error handling for invalid sampling strategy."""
        with pytest.raises(ValueError, match="Unknown sampling strategy"):
            TensorSparseSample.from_tensor(small_1d_tensor, strategy="invalid_strategy")

    def test_sample_size_too_large(self, small_1d_tensor: Tensor):
        """Tests error handling for too large sample size."""
        with pytest.raises(ValueError, match="sample_size .* cannot be larger"):
            TensorSparseSample.from_tensor(
                small_1d_tensor, sample_size=len(small_1d_tensor) + 1
            )

    def test_out_of_bounds_indices(self, small_1d_tensor: Tensor):
        """Tests error handling for out-of-bounds indices."""
        invalid_indices = torch.tensor([len(small_1d_tensor) + 1])
        with pytest.raises(ValueError, match="Index out of bounds"):
            TensorSparseSample.from_tensor(small_1d_tensor, indices=invalid_indices)


if __name__ == "__main__":
    pytest.main([__file__])
