"""Library for monitoring PyTorch network statistics.

This module provides utilities for monitoring various statistics of PyTorch networks,
including weights, gradients, and activations. It helps identify potential issues
like vanishing/exploding gradients and unusual distributions.
"""

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np
import torch
from torch import Tensor


@dataclass
class TensorQuartileInfo:
    """Stores quartile information of a tensor distribution.

    Attributes:
        quartile_95: The 95th percentile value.
        quartile_75: The 75th percentile value (upper quartile).
        quartile_25: The 25th percentile value (lower quartile).
        quartile_5: The 5th percentile value.
    """

    quartile_95: float
    quartile_75: float
    quartile_25: float
    quartile_5: float

    def __repr__(self) -> str:
        """Returns a formatted string representation of quartile information."""
        return (
            f"TensorQuartileInfo(\n"
            f"    q95: {self.quartile_95:8.3g},\n"
            f"    q75: {self.quartile_75:8.3g},\n"
            f"    q25: {self.quartile_25:8.3g},\n"
            f"    q05: {self.quartile_5:8.3g}\n"
            f")"
        )

    @classmethod
    def from_tensor(cls, tensor: Tensor) -> "TensorQuartileInfo":
        """Creates TensorQuartileInfo from a tensor.

        Args:
            tensor: Input tensor of any shape, will be flattened for analysis.

        Returns:
            TensorQuartileInfo containing the quartile statistics of the input tensor.
        """
        flat_tensor = tensor.detach().float().flatten()
        percentiles = torch.tensor([5, 25, 75, 95], dtype=torch.float32)
        q05, q25, q75, q95 = torch.quantile(flat_tensor, percentiles / 100)

        return cls(
            quartile_95=q95.item(),
            quartile_75=q75.item(),
            quartile_25=q25.item(),
            quartile_5=q05.item(),
        )


@dataclass
class TensorOutlierInfo:
    """Stores outlier information using multiple detection methods.

    Attributes:
        iqr_outlier_ratio_high: Ratio of high outliers using IQR method.
        iqr_outlier_ratio_low: Ratio of low outliers using IQR method.
        modified_z_score_outlier_ratio_high: Ratio of high outliers using modified Z-score.
        modified_z_score_outlier_ratio_low: Ratio of low outliers using modified Z-score.
        mad_outlier_ratio_high: Ratio of high outliers using MAD method.
        mad_outlier_ratio_low: Ratio of low outliers using MAD method.
    """

    iqr_outlier_ratio_high: float
    iqr_outlier_ratio_low: float
    modified_z_score_outlier_ratio_high: float
    modified_z_score_outlier_ratio_low: float
    mad_outlier_ratio_high: float
    mad_outlier_ratio_low: float

    def __repr__(self) -> str:
        """Returns a formatted string representation of outlier information."""
        return (
            f"TensorOutlierInfo(\n"
            f"    IQR High:      {self.iqr_outlier_ratio_high:8.3%}\n"
            f"    IQR Low:       {self.iqr_outlier_ratio_low:8.3%}\n"
            f"    Mod Z High:    {self.modified_z_score_outlier_ratio_high:8.3%}\n"
            f"    Mod Z Low:     {self.modified_z_score_outlier_ratio_low:8.3%}\n"
            f"    MAD High:      {self.mad_outlier_ratio_high:8.3%}\n"
            f"    MAD Low:       {self.mad_outlier_ratio_low:8.3%}\n"
            f")"
        )

    @classmethod
    def from_tensor(cls, tensor: Tensor) -> "TensorOutlierInfo":
        """Creates TensorOutlierInfo from a tensor using multiple outlier detection methods.

        Args:
            tensor: Input tensor of any shape, will be flattened for analysis.

        Returns:
            TensorOutlierInfo containing outlier statistics using various methods.
        """
        flat_tensor = tensor.detach().float().flatten().numpy()

        # IQR method
        q75, q25 = np.percentile(flat_tensor, [75, 25])
        iqr = q75 - q25
        iqr_high = q75 + 1.5 * iqr
        iqr_low = q25 - 1.5 * iqr

        # Modified Z-score method
        median = np.median(flat_tensor)
        mad = np.median(np.abs(flat_tensor - median))
        modified_z = 0.6745 * (flat_tensor - median) / mad
        z_threshold = 3.5

        # MAD method
        mad_high = median + 3 * mad
        mad_low = median - 3 * mad

        return cls(
            iqr_outlier_ratio_high=np.mean(flat_tensor > iqr_high),
            iqr_outlier_ratio_low=np.mean(flat_tensor < iqr_low),
            modified_z_score_outlier_ratio_high=np.mean(modified_z > z_threshold),
            modified_z_score_outlier_ratio_low=np.mean(modified_z < -z_threshold),
            mad_outlier_ratio_high=np.mean(flat_tensor > mad_high),
            mad_outlier_ratio_low=np.mean(flat_tensor < mad_low),
        )


@dataclass
class TensorStatInfo:  # pylint: disable=too-many-instance-attributes
    """Comprehensive statistical information about a tensor.

    Attributes:
        num_samples: Number of elements in the tensor.
        m1: First moment (mean).
        m2: Second moment.
        median: Median value.
        std: Standard deviation.
        min: Minimum value.
        max: Maximum value.
        quartile_info: Quartile statistics.
        outlier_info: Outlier statistics.
    """

    num_samples: int
    m1: float
    m2: float
    median: float
    std: float
    min: float
    max: float
    quartile_info: TensorQuartileInfo
    outlier_info: TensorOutlierInfo

    def __repr__(self) -> str:
        """Returns a formatted string representation of all statistics."""
        return (
            f"StatInfo(\n"
            f"    num_samples: {self.num_samples}\n"
            f"    mean:        {self.m1:8.3g}\n"
            f"    std:         {self.std:8.3g}\n"
            f"    median:      {self.median:8.3g}\n"
            f"    min:         {self.min:8.3g}\n"
            f"    max:         {self.max:8.3g}\n"
            f"    quartile_info:\n"
            f"{self._indent(self.quartile_info.__repr__())}\n"
            f"    outlier_info:\n"
            f"{self._indent(self.outlier_info.__repr__())}\n"
            f")"
        )

    @staticmethod
    def _indent(text: str, spaces: int = 8) -> str:
        """Indents each line of the text by specified number of spaces."""
        return "\n".join(" " * spaces + line for line in text.split("\n"))

    @classmethod
    def from_tensor(cls, tensor: Tensor) -> "TensorStatInfo":
        """Creates StatInfo from a tensor.

        Args:
            tensor: Input tensor of any shape, will be flattened for analysis.

        Returns:
            StatInfo containing comprehensive statistics of the input tensor.
        """
        flat_tensor = tensor.detach().float().flatten()

        return cls(
            num_samples=flat_tensor.numel(),
            m1=torch.mean(flat_tensor).item(),
            m2=torch.mean(flat_tensor**2).item(),
            median=torch.median(flat_tensor).item(),
            std=torch.std(flat_tensor).item(),
            min=torch.min(flat_tensor).item(),
            max=torch.max(flat_tensor).item(),
            quartile_info=TensorQuartileInfo.from_tensor(flat_tensor),
            outlier_info=TensorOutlierInfo.from_tensor(flat_tensor),
        )


@dataclass
class TensorSparseSample:
    """Stores sparse samples from multiple tensors using indices and values.

    This class enables efficient storage and updates of specific tensor elements,
    useful for monitoring large tensors without storing the entire tensor.
    It can track values from multiple tensor updates, stacking them for analysis.

    Attributes:
        indices: Tensor of indices for the sampled elements. Shape: (n_samples, n_dims)
            For 1D tensors, shape is (n_samples,).
        values: Optional tensor of values at the specified indices.
            Shape is (ntensor, n_samples) where ntensor is number of updates.
        ntensor: Number of tensors processed (number of updates made).
    """

    indices: Tensor
    values: Optional[Tensor] = None
    ntensor: int = 0

    def __post_init__(self):
        """Validates the inputs after initialization.

        Raises:
            TypeError: If indices or values are not tensors.
            ValueError: If values shape doesn't match indices or has wrong dimensions.
        """
        if not isinstance(self.indices, Tensor):
            raise TypeError("indices must be a torch.Tensor")

        if self.values is not None:
            if not isinstance(self.values, Tensor):
                raise TypeError("values must be a torch.Tensor")

            # Check values is 2D
            if self.values.dim() != 2:
                raise ValueError(
                    "values must be a 2D tensor with shape (ntensor, n_samples)"
                )

            # Check number of samples matches
            if self.values.shape[1] != self.indices.shape[0]:
                raise ValueError(
                    f"Number of values ({self.values.shape[1]}) must match "
                    f"number of indices ({self.indices.shape[0]})"
                )

            # Update ntensor based on values if provided
            self.ntensor = self.values.shape[0]

    def update(self, tensor: Tensor) -> None:
        """Updates values from the input tensor at stored indices.

        This method extracts values at the stored indices and stacks them with
        previous updates. Each update adds a new row to the values tensor.

        Args:
            tensor: Input tensor to sample values from. Its shape must be compatible
                with the stored indices.

        Raises:
            ValueError: If tensor shape is incompatible with stored indices.
            RuntimeError: If indices are out of bounds for the input tensor.
        """
        if not isinstance(tensor, Tensor):
            raise TypeError("tensor must be a torch.Tensor")

        # Handle different dimensional cases
        if self.indices.dim() == 1:
            if tensor.dim() != 1:
                raise ValueError(
                    f"Expected 1D tensor for 1D indices, got shape {tensor.shape}"
                )
            new_values = tensor[self.indices]
        else:
            # For multi-dimensional tensors
            try:
                new_values = tensor[tuple(self.indices.t())]
            except IndexError as e:
                raise RuntimeError(
                    f"Index out of bounds. Tensor shape: {tensor.shape}, "
                    f"Max index: {self.indices.max().item()}"
                ) from e

        new_values = new_values.detach().clone()

        # Stack with previous values or initialize
        if self.values is None:
            self.values = new_values.unsqueeze(0)
        else:
            self.values = torch.cat([self.values, new_values.unsqueeze(0)])

        self.ntensor += 1

    @classmethod
    def from_tensor(
        cls,
        tensor: Tensor,
        indices: Optional[Tensor] = None,
        sample_size: Optional[int] = None,
        strategy: str = "random",
    ) -> "TensorSparseSample":
        """Creates a TensorSparseSample from a tensor.

        Args:
            tensor: Input tensor to sample from.
            indices: Optional specific indices to sample. If None, indices will be
                generated according to the strategy.
            sample_size: Number of samples to take if indices is None.
                Defaults to min(sqrt(tensor.numel()), 100) if None.
            strategy: Sampling strategy when generating indices. Options:
                - 'random': Random sampling (default)
                - 'uniform': Uniform sampling across the tensor
                - 'edges': Sample from edges and center of the tensor

        Returns:
            A new TensorSparseSample instance containing the sampled indices and values.

        Raises:
            ValueError: If strategy is invalid or sampling parameters are inconsistent.
        """
        if not isinstance(tensor, Tensor):
            raise TypeError("tensor must be a torch.Tensor")

        # Generate indices if not provided
        if indices is None:
            # Determine sample size if not specified
            if sample_size is None:
                sample_size = min(int(math.sqrt(tensor.numel())), 100)

            indices = cls._generate_indices(tensor, sample_size, strategy)
        else:
            if not isinstance(indices, Tensor):
                raise TypeError("indices must be a torch.Tensor")

            # Validate indices
            if indices.max() >= tensor.numel():
                raise ValueError("Index out of bounds for tensor")

        # Create instance and update values
        instance = cls(indices=indices, ntensor=0)
        instance.update(tensor)
        return instance

    @staticmethod
    def _generate_indices(  # pylint: disable=too-many-locals
        tensor: Tensor, sample_size: int, strategy: str = "random"
    ) -> Tensor:
        """Generates indices for sampling based on the specified strategy.

        Args:
            tensor: Input tensor to generate indices for.
            sample_size: Number of samples to generate.
            strategy: Sampling strategy ('random', 'uniform', or 'edges').

        Returns:
            Tensor containing the generated indices.

        Raises:
            ValueError: If strategy is invalid or sample_size is too large.
        """
        if sample_size > tensor.numel():
            raise ValueError(
                f"sample_size ({sample_size}) cannot be larger than "
                f"number of elements ({tensor.numel()})"
            )

        # Generate linear indices first
        if strategy == "random":
            linear_indices = torch.randperm(tensor.numel())[:sample_size]

        elif strategy == "uniform":
            stride = tensor.numel() // sample_size
            linear_indices = torch.arange(0, tensor.numel(), stride)[:sample_size]

        elif strategy == "edges":
            # Take samples from start, middle, and end of tensor
            third = sample_size // 3
            remainder = sample_size % 3

            start_indices = torch.arange(third)
            middle_start = (tensor.numel() // 2) - (third // 2)
            middle_indices = torch.arange(middle_start, middle_start + third)
            end_start = tensor.numel() - third - remainder
            end_indices = torch.arange(end_start, tensor.numel())

            linear_indices = torch.cat([start_indices, middle_indices, end_indices])

        else:
            raise ValueError(
                f"Unknown sampling strategy: {strategy}. "
                "Valid options are: 'random', 'uniform', 'edges'"
            )

        # For multi-dimensional tensors, convert linear indices to multi-dimensional indices
        if tensor.dim() > 1:
            multi_indices = []
            shape = tensor.shape
            for idx in linear_indices:
                # Convert linear index to multi-dimensional indices
                curr_idx = idx.item()
                multi_idx = []
                for dim_size in shape[::-1]:
                    multi_idx.append(curr_idx % dim_size)
                    curr_idx //= dim_size
                multi_indices.append(multi_idx[::-1])  # Reverse to get correct order
            return torch.tensor(multi_indices)

        return linear_indices

    def __len__(self) -> int:
        """Returns the number of samples."""
        return self.indices.shape[0]

    def __repr__(self) -> str:
        """Returns a string representation of the sparse sample."""
        return (
            f"TensorSparseSample(\n"
            f"    num_samples: {len(self)}\n"
            f"    indices shape: {tuple(self.indices.shape)}\n"
            f"    values: {'Not set' if self.values is None else f'shape {tuple(self.values.shape)}'}\n"
            f"    ntensor: {self.ntensor}\n"
            ")"
        )


def get_tensor_stat_info(tensor: Tensor, name: Optional[str] = None) -> TensorStatInfo:
    """Returns comprehensive statistical information about a tensor.

    Args:
        tensor: Input tensor of any shape.
        name: Optional name to identify the tensor.

    Returns:
        StatInfo containing comprehensive statistics of the input tensor.
    """
    if name is not None:
        print(f"Statistics for {name} tensor:")
    return TensorStatInfo.from_tensor(tensor)
