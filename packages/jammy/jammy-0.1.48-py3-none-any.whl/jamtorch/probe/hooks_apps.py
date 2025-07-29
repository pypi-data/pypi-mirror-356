from collections import OrderedDict
from dataclasses import asdict, dataclass
from typing import Any, Callable, List, Optional, Tuple, TypeVar

import pandas as pd
import torch
from torch import Tensor, nn
from torch.utils.hooks import RemovableHandle

DataclassType = TypeVar("DataclassType", bound=Any)  # pylint: disable=invalid-name
ProcessFn = Callable[[str, nn.Module, int, Tensor], DataclassType]


@dataclass
class TeorKStates:
    name: str
    shape: Tuple[int, ...]
    dtype: str
    magnitude: float
    max: float
    viz_type: Optional[str] = None


def terok_processor(
    name: str, module: nn.Module, idx: int, tensor: Tensor
) -> TeorKStates:
    del module, idx
    return TeorKStates(
        name=name,
        shape=tensor.shape,
        dtype=str(tensor.dtype).rsplit(".", maxsplit=1)[-1],
        magnitude=float(tensor.to(torch.float32).square().mean().sqrt()),
        max=float(tensor.to(torch.float32).abs().max()),
    )


class PerLayerSpec:
    def __init__(
        self,
        process_fn: ProcessFn = terok_processor,
    ):
        self.module2name = OrderedDict()
        self.unique_names = set()

        self.layer_specs = []
        self.process_fn = process_fn

    @property
    def results(self) -> List[DataclassType]:
        return self.layer_specs

    def unique_name(self, module, idx, num):
        name = self.module2name[module]

        # If there is more than one instance of the module, append the index to its name.
        # This helps in differentiating multiple instances of the same module.
        if num > 1:
            name += f":{idx}"

        # Check if the constructed name is already used by another module instance.
        # If it is, a unique suffix needs to be added to the name.
        if name in self.unique_names:
            # Start with a suffix of 2 (assuming the original without suffix is considered '1').
            suffix = 2
            # Increment the suffix until a unique name is found that isn't in the set of unique names.
            while f"{name}_{suffix}" in self.unique_names:
                suffix += 1
            # Once a unique suffix is found, append it to the name.
            name += f"_{suffix}"

        # Add the newly created unique name to the set of unique names to keep track.
        self.unique_names.add(name)

        # Return the unique name for the module.
        return name

    def module_hook(self, module, _, outputs):
        outputs = list(outputs) if isinstance(outputs, (tuple, list)) else [outputs]
        outputs = [out for out in outputs if isinstance(out, torch.Tensor)]
        for idx, value in enumerate(outputs):
            name = self.unique_name(module, idx, len(outputs))
            self.layer_specs.append(self.process_fn(name, module, idx, value))

    def register_hook(self, name: str, module: nn.Module) -> RemovableHandle:
        self.module2name[module] = name
        return module.register_forward_hook(self.module_hook)

    def reset(self):
        self.module2name.clear()
        self.unique_names.clear()
        self.layer_specs.clear()

    def reset_forward(self):
        self.layer_specs.clear()
        self.unique_names.clear()


def layer_sepc_to_df(layer_specs: List[DataclassType]) -> pd.DataFrame:
    return pd.DataFrame([asdict(spec) for spec in layer_specs])
