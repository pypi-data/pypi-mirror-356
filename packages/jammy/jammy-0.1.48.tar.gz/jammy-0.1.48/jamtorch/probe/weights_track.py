import re
from typing import Dict

import numpy as np
import pandas as pd

try:
    import plotly.express as px
except ImportError:
    px = None
import torch


def log_weight_plot(  # pylint: disable=too-many-locals
    model_cur_sd: Dict[str, torch.Tensor],
    model_prev_sd: Dict[str, torch.Tensor],
    step: int,
    html_fp="/tmp/weight_distribution_changes.html",
) -> str:
    """
    Generates and logs a plot of the weight distribution and changes between two model states.

    Args:
        model_cur_sd (Dict[str, torch.Tensor]): The current state dictionary of the model,
            containing parameter names and their corresponding tensors.
        model_prev_sd (Dict[str, torch.Tensor]): The previous state dictionary of the model,
            containing parameter names and their corresponding tensors.
        step (int): The current training step, used for labeling the plot.
        html_fp (str): The file path to save the HTML plot. Defaults to "/tmp/weight_distribution_changes.html".

    Returns:
        str: The path to the saved HTML plot.
    """
    # Initialize lists to store plot data
    layer_names = []
    std_devs = []
    l1_norms = []
    param_counts = []
    colors = []
    markers = []

    # Iterate over the parameters and compute necessary metrics
    for name, param in model_cur_sd.items():
        if name in model_prev_sd:
            prev_param = model_prev_sd[name]
            std_dev = param.std().item()
            l1_norm = torch.abs(param - prev_param).mean().item()
            param_count = param.numel()

            # Determine color based on the layer number using regex
            layer_match = re.match(r".*\.h\.(\d+)(?:\..*)?$", name)
            if layer_match:
                layer_num = int(layer_match.group(1))
                colors.append(layer_num)
            else:
                colors.append(-1)  # Non-layer parameters

            # Determine marker type based on the parameter's dimensionality
            if param.ndim == 1:
                markers.append("x")
            else:
                markers.append("circle")

            # Append data to the respective lists
            layer_names.append(name)
            std_devs.append(std_dev)
            l1_norms.append(np.log1p(l1_norm))  # log(1 + x) transformation
            param_counts.append(np.log(param_count))

    # Create a DataFrame for the plot
    df = pd.DataFrame(
        {
            "Layer Name": layer_names,
            "Standard Deviation": std_devs,
            "L1 Norm of Changes (log scale)": l1_norms,
            "Parameter Count (log)": param_counts,
            "Color": colors,
            "Marker": markers,
        }
    )

    # Determine the number of layers for color mapping
    max_layer_num = df[df["Color"] != -1]["Color"].max()

    # Create a color scale for the layers (yellow to red)
    color_scale = px.colors.sequential.YlOrRd
    color_discrete_map = {
        i: color_scale[int(i * (len(color_scale) - 1) / max_layer_num)]
        for i in range(int(max_layer_num) + 1)
    }
    color_discrete_map[-1] = "blue"  # Blue for non-layer parameters

    # Create Plotly figure
    fig = px.scatter(
        df,
        x="Standard Deviation",
        y="L1 Norm of Changes (log scale)",
        size="Parameter Count (log)",
        color="Color",
        hover_name="Layer Name",
        title=f"Model Weight Distribution and Changes, Step {step}",
        symbol="Marker",
        color_discrete_map=color_discrete_map,
        opacity=0.7,
    )

    # Save the plot as an HTML file
    fig.write_html(html_fp, auto_play=False)

    return html_fp
