# ===----------------------------------------------------------------------=== #
# Copyright (c) 2025, Modular Inc. All rights reserved.
#
# Licensed under the Apache License v2.0 with LLVM Exceptions:
# https://llvm.org/LICENSE.txt
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===----------------------------------------------------------------------=== #
"""Rejection Sampler custom ops."""

from max import nn
from max.dtype import DType
from max.graph import DeviceRef, Dim, TensorValue, ops
from max.nn.kernels import topk_fused_sampling


class RejectionSampler(nn.Module):
    """A simple rejection sampler."""

    def __init__(
        self,
        device: DeviceRef,
        top_k: int = 1,
        top_p: float = 1,
        temperature: float = 1.0,
        seed: int = 0,
        eps: float = 1e-5,
    ):
        self.device = device
        self.top_k = top_k
        self.top_p = top_p
        self.temperature = temperature
        self.eps = eps
        self.seed = seed

    def __call__(
        self,
        draft_tokens: TensorValue,
        draft_logits_for_sampled_tokens: TensorValue,
        target_logits: TensorValue,
        target_logit_offsets: TensorValue,
    ) -> tuple[TensorValue, TensorValue]:
        # Get Proper Indices for Tokens
        broadcasted_range = ops.broadcast_to(
            ops.range(
                0,
                ops.shape_to_tensor([draft_tokens.shape[1]]).reshape(()),
                1,
                out_dim=Dim("num_steps"),
                device=self.device,
                dtype=DType.int64,
            ),
            shape=[Dim("batch_size"), Dim("num_steps")],
        )

        logit_offsets = ops.rebind(
            ops.unsqueeze(target_logit_offsets[:-1], axis=-1),
            shape=[Dim("batch_size"), 1],
        )
        sampled_token_offsets = ops.reshape(
            ops.rebind(
                (broadcasted_range + logit_offsets),
                shape=[Dim("batch_size"), Dim("num_steps")],
            ),
            shape=[Dim("batch_size") * Dim("num_steps"), 1],
        )

        target_logits_for_sampled_tokens = ops.reshape(
            ops.gather_nd(
                target_logits,
                ops.concat(
                    [
                        sampled_token_offsets,
                        ops.reshape(
                            draft_tokens,
                            shape=(Dim("batch_size") * Dim("num_steps"), 1),
                        ),
                    ],
                    axis=1,
                ),
            ),
            shape=[Dim("batch_size"), Dim("num_steps")],
        )

        # Apply Rejection Function Elementwise
        rejected_tokens = ops.rebind(
            ops.concat(
                [
                    draft_logits_for_sampled_tokens
                    > target_logits_for_sampled_tokens + self.eps,
                    ops.broadcast_to(
                        ops.constant(
                            True, dtype=DType.bool, device=self.device
                        ),
                        shape=[Dim("batch_size"), 1],
                    ),
                ],
                axis=1,
            ),
            shape=[Dim("batch_size"), Dim("total_num_steps")],
        )

        # Calculate first rejected_token idx
        first_rejected_token = ops.argmax(
            ops.broadcast_to(
                ops.range(
                    ops.shape_to_tensor([rejected_tokens.shape[1]])
                    .reshape(())
                    .cast(DType.int32),
                    ops.constant(0, dtype=DType.int32, device=DeviceRef.CPU()),
                    ops.constant(-1, dtype=DType.int32, device=DeviceRef.CPU()),
                    out_dim="total_num_steps",
                    device=self.device,
                ),
                shape=[rejected_tokens.shape[0], Dim("total_num_steps")],
            )
            * rejected_tokens,
            axis=-1,
        )

        # Retrieve Appropriate Logits from Target Logits
        rejected_offsets = ops.rebind(
            target_logit_offsets[:-1], shape=[Dim("batch_size")]
        ) + ops.squeeze(first_rejected_token, axis=1)

        sampled_target_tokens = topk_fused_sampling(
            logits=ops.gather(target_logits, rejected_offsets, axis=0),
            top_k=self.top_k,
            max_k=self.top_k,
            temperature=self.temperature,
            top_p=self.top_p,
            seed=self.seed,
        )

        return first_rejected_token, sampled_target_tokens
