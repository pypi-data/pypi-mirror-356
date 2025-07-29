from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Optional, TypeVar

import torch
from torch import nn
from torch.utils.hooks import RemovableHandle

# Type variables for generic types
T = TypeVar("T")
ModuleType = TypeVar("ModuleType", bound=nn.Module)  # pylint: disable=invalid-name
OUTPUT_KEY: str = "output"

# Type aliases for better readability
FilterFn = Callable[[str, nn.Module], bool]
HookFn = Callable[[nn.Module, tuple[torch.Tensor, ...], torch.Tensor], None]
RegisterHookFn = Callable[[str, nn.Module], RemovableHandle]
ForwardFn = Callable[[], T]


def all_layers_filter(_: str, __: nn.Module) -> bool:
    """Filter function to capture activations from all layers."""
    return True


def conv_layers_filter(_: str, module: nn.Module) -> bool:
    """Filter function to capture activations from Conv2d layers only."""
    return isinstance(module, nn.Conv2d)


def regex_name_filter(pattern: str) -> FilterFn:
    r"""Creates a filter function that matches module names using regex pattern.

    Args:
        pattern: Regex pattern to match module names.

    Returns:
        Filter function that matches names against the pattern.

    Example:
        # Filter for attention layers
        attn_filter = regex_name_filter(r".*\.attn\..*")

        # Filter for specific layer numbers
        layer_filter = regex_name_filter(r"layer[0-2]\..*")
    """
    compiled_pattern = re.compile(pattern)

    def _filter(name: str, module: nn.Module) -> bool:
        return bool(compiled_pattern.match(name))

    return _filter


def combined_filter(name_pattern: Optional[str] = None, module_types: Optional[tuple[type, ...]] = None) -> FilterFn:
    r"""Creates a combined filter function for both name patterns and module types.

    Args:
        name_pattern: Optional regex pattern to match module names.
        module_types: Optional tuple of module types to match.

    Returns:
        Filter function that applies both name and type filtering.

    Example:
        # Filter for Conv2d layers in specific blocks
        filter_fn = combined_filter(r"features\..*", (nn.Conv2d,))
    """
    compiled_pattern = re.compile(name_pattern) if name_pattern else None

    def _filter(name: str, module: nn.Module) -> bool:
        # Check name pattern if provided
        if compiled_pattern and not compiled_pattern.match(name):
            return False

        # Check module type if provided - simplified logic
        return not (module_types and not isinstance(module, module_types))

    return _filter


@dataclass
class HookCaptureConfig:
    """Configuration for model hook capture.

    Attributes:
        remove_compiled_prefix: Whether to remove '_orig_mod.' prefix from compiled models.
        raise_on_hook_error: Whether to raise exceptions on hook removal errors.
    """

    remove_compiled_prefix: bool = True
    raise_on_hook_error: bool = False


def model_hook_capture(  # pylint: disable=too-many-branches  # noqa: C901
    model: ModuleType,
    forward_fn: ForwardFn[T],
    register_hook_fn: RegisterHookFn,
    filter_fn: FilterFn = all_layers_filter,
    config: Optional[HookCaptureConfig] = None,
) -> T:
    """Captures and processes intermediate activations in a PyTorch model using hooks.

    Args:
        model: PyTorch model to hook into.
        forward_fn: Function that runs the model forward pass.
        filter_fn: Function to filter which modules to hook.
        register_hook_fn: Function to register hooks for modules.
        config: Optional configuration for hook capture behavior.

    Returns:
        Results from forward_fn execution.

    Raises:
        RuntimeError: If hook removal fails and raise_on_hook_error is True.
        ValueError: If model has no modules matching the filter criteria.

    Example:
        ```python
        def custom_filter(name, module):
            return isinstance(module, nn.Conv2d) and "layer1" in name

        def custom_hook_register(name, module):
            def hook_fn(mod, inputs, output):
                print(f"{name}: {output.shape}")
            return module.register_forward_hook(hook_fn)

        results = model_hook_capture(
            model=my_model,
            forward_fn=lambda: model(input_tensor),
            filter_fn=custom_filter,
            register_hook_fn=custom_hook_register,
        )
        ```
    """
    if config is None:
        config = HookCaptureConfig()

    if not isinstance(model, nn.Module):
        raise TypeError(f"Expected nn.Module, got {type(model).__name__}")

    # Get module name mapping, handling compiled models
    module_to_name: dict[nn.Module, str] = {}
    for name, module in model.named_modules():
        if config.remove_compiled_prefix:
            name = name.split("_orig_mod.")[-1]
        module_to_name[module] = name
    module_to_name[model] = OUTPUT_KEY

    # Filter modules and store in OrderedDict to maintain order
    captured_modules = OrderedDict()
    for module, name in module_to_name.items():
        if not filter_fn(name, module):
            continue
        captured_modules[name] = module

    if not captured_modules:
        raise ValueError("No modules matched the filter criteria. Check your filter_fn.")

    # Store hooks for cleanup
    hooks: list[RemovableHandle] = []

    try:
        # Register hooks for all captured modules
        for name, module in captured_modules.items():
            try:
                hook = register_hook_fn(name, module)
                if not isinstance(hook, RemovableHandle):
                    print(
                        f"Hook returned by register_hook_fn for module {name} is not a "
                        "RemovableHandle. Hook cleanup may fail."
                    )
                hooks.append(hook)
            except Exception as e:
                # log.error("Failed to register hook for module %s: %s", name, e)
                print(f"Failed to register hook for module {name}: {e}")
                # Clean up already registered hooks before re-raising
                _cleanup_hooks(hooks, raise_on_error=False)
                raise RuntimeError(f"Hook registration failed for module {name}") from e

        # Run the model
        try:
            results = forward_fn()
        except Exception as e:
            # log.error("Forward pass failed: %s", e)
            print(f"Forward pass failed: {e}")
            _cleanup_hooks(hooks, raise_on_error=False)
            raise

    finally:
        # Always clean up hooks
        _cleanup_hooks(hooks, raise_on_error=config.raise_on_hook_error)

    return results


def _cleanup_hooks(
    hooks: list[RemovableHandle],
    raise_on_error: bool = False,
) -> None:
    """Cleans up PyTorch hooks safely.

    Args:
        hooks: List of PyTorch removable handles to clean up.
        raise_on_error: Whether to raise exceptions on hook removal errors.

    Raises:
        RuntimeError: If hook removal fails and raise_on_error is True.
    """
    for hook in hooks:
        try:
            hook.remove()
        except Exception as e:  # pylint: disable=broad-except
            msg = f"Failed to remove hook: {e}"
            if raise_on_error:
                raise RuntimeError(msg) from e
            # log.warning(msg)
            print(f"warning: {msg}")
    hooks.clear()
