import pytest
import torch

from jamtorch.nn.gpt import GPT, GPTConfig

from .hooks_apps import PerLayerSpec, layer_sepc_to_df, terok_processor
from .hooks_core import all_layers_filter, model_hook_capture


def test_forward():
    gpt_config = GPTConfig()
    gpt_model = GPT(gpt_config).cuda()
    per_layer_spec = PerLayerSpec(process_fn=terok_processor)

    def _fn():
        return gpt_model(torch.randint(0, gpt_config.vocab_size, (2, 128)).cuda())

    _ = model_hook_capture(
        gpt_model,
        _fn,
        per_layer_spec.register_hook,
        all_layers_filter,
        None,
    )

    layer_spec = per_layer_spec.results
    print(layer_sepc_to_df(layer_spec))


if __name__ == "__main__":
    pytest.main([__file__])
