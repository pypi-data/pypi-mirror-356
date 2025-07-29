# ===----------------------------------------------------------------------=== #
#
# This file is Modular Inc proprietary.
#
# ===----------------------------------------------------------------------=== #
"""Op implementation for allreduce."""

from __future__ import annotations

from collections.abc import Iterable

from max.mlir.dialects import mo

from ..graph import Graph  # noqa
from ..type import _ChainType
from ..value import BufferValue, TensorValue


def sum(
    inputs: Iterable[TensorValue], signal_buffers: Iterable[BufferValue]
) -> list[TensorValue]:
    """Collective allreduce summation operation.

    This op is a collective op which takes in tensors from different devices and
    outputs tensors on different devices.
    In particular, this operation will gather the inputs across different
    devices and reduce them via a summation operation.
    The result is then broadcasted back to the same devices that the inputs
    came from.

    This version of the allreduce sum op uses device-to-device transfers and
    hence is expected to be much slower than the :obj:`ops.allreduce.sum` version.

    Args:
        inputs: The input tensors to reduce.
        signal_buffers: Device buffer values used for synchronization.

    Returns:
        An iterable outputs which all hold the reduction output.
    """
    # Convert `inputs` to list since we'll iterate over it twice.
    inputs = list(inputs)
    signal_buffers = list(signal_buffers)
    if len(inputs) != len(signal_buffers):
        msg = (
            f"expected number of inputs ({len(inputs)}) and number of "
            f"signal buffers ({len(signal_buffers)}) to match"
        )
        raise ValueError(msg)

    shape = None
    devices = []

    for input in inputs:
        if not shape:
            shape = input.shape
        if input.shape != shape:
            msg = (
                "allreduce.sum operation must have the same shape across all"
                " input tensors."
            )
            raise ValueError(msg)
        if not input.device:
            msg = (
                f"allreduce.sum operation input = {input} needs to have an"
                " explicit device."
            )
            raise ValueError(msg)
        if input.device in devices:
            msg = (
                "allreduce.sum operation must have unique devices across its"
                " input tensors."
            )
            raise ValueError(msg)
        devices.append(input.device)

    in_chain = Graph.current._current_chain
    *results, out_chain = Graph.current._add_op(
        mo.distributed_allreduce_sum,
        # Types for 2 outputs: chain, list of tensors
        [x.type.to_mlir() for x in inputs],
        _ChainType().to_mlir(),
        inputs,
        signal_buffers,
        in_chain,
    )

    Graph.current._update_chain(out_chain)

    return [res.tensor for res in results]
