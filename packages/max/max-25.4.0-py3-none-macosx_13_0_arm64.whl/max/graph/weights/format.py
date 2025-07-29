# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #
"""Utilities for tracking weight formats."""

from enum import Enum
from pathlib import Path


class WeightsFormat(str, Enum):
    gguf = "gguf"
    safetensors = "safetensors"
    pytorch = "pytorch"


def weights_format(weight_paths: list[Path]) -> WeightsFormat:
    """Retrieve the format of the weights files in the provided paths.

    Args:
        weight_paths:
          A list of file paths, containing the weights for a single model.

    Returns:
        A `WeightsFormat` enum, representing whether the weights are in
        `gguf`, `safetensors` or `pytorch` format.

    Raises:
        ValueError: If weights type cannot be inferred from the paths.

    """
    if not weight_paths:
        raise ValueError(
            "no weight_paths provided cannot infer weights format."
        )

    if all(weight_path.suffix == ".gguf" for weight_path in weight_paths):
        return WeightsFormat.gguf
    elif all(
        weight_path.suffix == ".safetensors" for weight_path in weight_paths
    ):
        return WeightsFormat.safetensors
    elif all(weight_path.suffix == ".bin" for weight_path in weight_paths):
        return WeightsFormat.pytorch
    else:
        raise ValueError(f"weights type cannot be inferred from {weight_paths}")
