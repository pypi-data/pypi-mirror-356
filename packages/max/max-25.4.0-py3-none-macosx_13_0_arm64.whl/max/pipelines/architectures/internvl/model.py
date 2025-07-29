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

from __future__ import annotations

import logging
import time
from collections.abc import Sequence
from typing import cast

import numpy as np
from max.driver import Device, Tensor
from max.dtype import DType
from max.engine import InferenceSession, Model
from max.graph import DeviceRef, Graph, TensorType, TensorValue, Type
from max.graph.weights import (
    SafetensorWeights,
    WeightData,
    Weights,
    WeightsAdapter,
)
from max.nn import ReturnLogits, Signals
from max.nn.kv_cache import (
    KVCacheInputs,
    KVCacheManager,
    KVCacheParams,
    estimate_kv_cache_size,
    load_kv_manager,
)
from max.pipelines.core import TextAndVisionContext
from max.pipelines.lib import (
    KVCacheConfig,
    KVCacheMixin,
    ModelInputs,
    ModelOutputs,
    PipelineConfig,
    PipelineModel,
    SupportedEncoding,
)
from transformers import AutoConfig

from .internvl import InternVLLanguageModel, InternVLVisionModel
from .model_config import InternVLConfig
from .weight_adapters import convert_internvl_language_model_state_dict

logger = logging.getLogger("max.pipelines")


class InternVLInputs(ModelInputs):
    """A class representing inputs for the InternVL model."""

    input_ids: Tensor
    """Tensor containing the input token IDs."""

    input_row_offsets: Tensor
    """Tensor containing the offsets for each row in the ragged input sequence."""

    signal_buffers: list[Tensor]
    """Device buffers used for synchronization in communication collectives."""

    # Vision inputs
    pixel_values: Tensor | None = None
    """Pixel values for vision inputs."""

    return_n_logits: Tensor
    """Number of logits to return, used by speculative decoding for example."""

    def __init__(
        self,
        input_ids: Tensor,
        input_row_offsets: Tensor,
        signal_buffers: list[Tensor],
        return_n_logits: Tensor,
        pixel_values: Tensor | None = None,
        kv_cache_inputs: KVCacheInputs | None = None,
    ) -> None:
        self.input_ids = input_ids
        self.input_row_offsets = input_row_offsets
        self.signal_buffers = signal_buffers
        self.return_n_logits = return_n_logits
        self.pixel_values = pixel_values
        self.kv_cache_inputs = kv_cache_inputs

    @property
    def has_vision_inputs(self) -> bool:
        """Check if this input contains vision data."""
        return self.pixel_values is not None


class InternVLModel(PipelineModel[TextAndVisionContext], KVCacheMixin):
    """An InternVL pipeline model for multimodal text generation."""

    vision_model: Model
    """The compiled vision model for processing images."""

    language_model: Model
    """The compiled language model for text generation."""

    _input_row_offsets_prealloc: Tensor
    """Pre-allocated tensor for input row offsets in multi-step execution."""

    def __init__(
        self,
        pipeline_config: PipelineConfig,
        session: InferenceSession,
        huggingface_config: AutoConfig,
        encoding: SupportedEncoding,
        devices: list[Device],
        kv_cache_config: KVCacheConfig,
        weights: Weights,
        adapter: WeightsAdapter | None = None,
        return_logits: ReturnLogits = ReturnLogits.LAST_TOKEN,
    ) -> None:
        super().__init__(
            pipeline_config,
            session,
            huggingface_config,
            encoding,
            devices,
            kv_cache_config,
            weights,
            adapter,
            return_logits,
        )

        self.vision_model, self.language_model = self.load_model(session)

        # Initialize signal buffers for distributed communication.
        # InternVL is natively distributed, so we always need these.
        self.signal_buffers = [
            Tensor.zeros(
                shape=(Signals.NUM_BYTES,), dtype=DType.uint8, device=dev
            )
            for dev in self.devices
        ]

    @staticmethod
    def calculate_max_seq_len(
        pipeline_config: PipelineConfig, huggingface_config: AutoConfig
    ) -> int:
        """Calculates the maximum sequence length for the InternVL model."""
        max_seq_len = pipeline_config.max_length
        if max_seq_len:
            return max_seq_len

        # Get `max_position_embeddings` from the `llm_config`.
        return huggingface_config.llm_config.max_position_embeddings

    @classmethod
    def get_kv_params(
        cls,
        huggingface_config: AutoConfig,
        n_devices: int,
        kv_cache_config: KVCacheConfig,
        cache_dtype: DType,
    ) -> KVCacheParams:
        """Gets the parameters required to configure the KV cache for InternVL."""
        return InternVLConfig.get_kv_params(
            huggingface_config, n_devices, kv_cache_config, cache_dtype
        )

    @classmethod
    def get_num_layers(cls, huggingface_config: AutoConfig) -> int:
        """Gets the number of hidden layers from the HuggingFace configuration."""
        return InternVLConfig.get_num_layers(huggingface_config)

    @classmethod
    def estimate_kv_cache_size(
        cls,
        pipeline_config: PipelineConfig,
        available_cache_memory: int,
        devices: list[Device],
        huggingface_config: AutoConfig,
        kv_cache_config: KVCacheConfig,
        cache_dtype: DType,
    ) -> int:
        """Estimates the size of the KV cache required for the InternVL model in bytes."""
        return estimate_kv_cache_size(
            params=InternVLConfig.get_kv_params(
                huggingface_config=huggingface_config,
                n_devices=len(devices),
                kv_cache_config=kv_cache_config,
                cache_dtype=cache_dtype,
            ),
            max_batch_size=pipeline_config.max_batch_size,
            max_seq_len=cls.calculate_max_seq_len(
                pipeline_config, huggingface_config=huggingface_config
            ),
            num_layers=InternVLConfig.get_num_layers(
                huggingface_config=huggingface_config
            ),
            available_cache_memory=available_cache_memory,
            devices=devices,
        )

    def _get_state_dict(
        self,
        weights: Weights,
        adapter: WeightsAdapter,
    ) -> dict[str, WeightData]:
        """Get processed state dict for language model loading.

        Args:
            weights: Raw InternVL checkpoint weights
            adapter: Weight adapter for name mapping (required)

        Returns:
            Processed state dict ready for DistributedLlama3.load_state_dict()
        """
        return adapter(
            dict(weights.items()),
            huggingface_config=self.huggingface_config,
            pipeline_config=self.pipeline_config,
        )

    def load_model(self, session: InferenceSession) -> tuple[Model, Model]:
        """Loads the compiled InternVL models into the MAX Engine session.

        Returns:
            A tuple of (vision_model, language_model).
        """
        # Pre-allocation for multi-step execution
        assert self.pipeline_config.max_batch_size, (
            "Expected max_batch_size to be set"
        )
        self._input_row_offsets_prealloc = Tensor.from_numpy(
            np.arange(self.pipeline_config.max_batch_size + 1, dtype=np.uint32)
        ).to(self.devices[0])

        # Validate SafetensorWeights requirement
        if not isinstance(self.weights, SafetensorWeights):
            raise ValueError(
                "InternVL currently only supports safetensors weights"
            )

        # Get processed state dict for language model.
        state_dict = self._get_state_dict(
            self.weights, convert_internvl_language_model_state_dict
        )

        # Generate InternVL config from HuggingFace config
        internvl_config = InternVLConfig.generate(
            pipeline_config=self.pipeline_config,
            huggingface_config=self.huggingface_config,
            state_dict=state_dict,
            dtype=self.dtype,
            n_devices=len(self.devices),
            logits_postprocessor=None,
            cache_dtype=self.encoding.cache_dtype,
            kv_cache_config=self.kv_cache_config,
            return_logits=self.return_logits,
        )

        # Build and compile vision model
        logger.info("Building and compiling vision model...")
        before = time.perf_counter()
        vision_graph = self._build_vision_graph(internvl_config)
        vision_model = session.load(
            vision_graph, weights_registry=self.weights.allocated_weights
        )
        after = time.perf_counter()
        logger.info(
            f"Building and compiling vision model took {after - before:.6f} seconds"
        )

        # Build and compile language model
        logger.info("Building and compiling language model...")
        before = time.perf_counter()
        language_graph = self._build_language_graph(internvl_config, state_dict)
        language_model = session.load(
            language_graph, weights_registry=self.state_dict
        )
        after = time.perf_counter()
        logger.info(
            f"Building and compiling language model took {after - before:.6f} seconds"
        )

        return vision_model, language_model

    def _build_vision_graph(self, config: InternVLConfig) -> Graph:
        """Build the vision model graph for processing images."""
        # Define input types for the vision model
        pixel_values_type = TensorType(
            DType.float32,
            shape=["batch_size", "height", "width", "num_channels"],
            # Expect the input image on device 0.
            device=DeviceRef.GPU(),
        )

        # Initialize graph with input types
        with Graph("internvl_vision", input_types=[pixel_values_type]) as graph:
            # Build vision model architecture.
            vision_model = InternVLVisionModel(config)

            # Unpack inputs.
            (pixel_values,) = graph.inputs

            # Execute vision model: pixel_values -> image_embeddings.
            image_embeddings = vision_model(
                [
                    # Transfer pixel values to each device.
                    pixel_values.tensor.to(DeviceRef.from_device(dev))
                    for dev in self.devices
                ]
            )

            # Set graph outputs.
            graph.output(*image_embeddings)

            return graph

    def _language_graph_input_types(self) -> tuple[Type, ...]:
        # Generate DeviceRef.
        device_ref = DeviceRef.from_device(self.devices[0])

        return_n_logits_type = TensorType(
            DType.int64, shape=["return_n_logits"], device=DeviceRef.CPU()
        )

        kv_inputs = self.kv_manager.input_symbols()

        # Construct Graph Inputs
        tokens_type = TensorType(
            DType.int64, shape=["total_seq_len"], device=device_ref
        )
        input_row_offsets_type = TensorType(
            DType.uint32, shape=["input_row_offsets_len"], device=device_ref
        )

        # Flatten kv types for each device
        flattened_kv_types = [
            kv_type for sublist in kv_inputs for kv_type in sublist
        ]

        signals = Signals(
            devices=(DeviceRef(d.label, d.id) for d in self.devices)
        )

        return (
            tokens_type,
            input_row_offsets_type,
            return_n_logits_type,
            *signals.input_types(),
            *flattened_kv_types,
        )

    def _unflatten_kv_inputs(
        self, kv_inputs_flat: Sequence[TensorValue]
    ) -> list[tuple[TensorValue, ...]]:
        kv_params = InternVLConfig.get_kv_params(
            huggingface_config=self.huggingface_config,
            n_devices=len(self.devices),
            kv_cache_config=self.kv_cache_config,
            cache_dtype=self.encoding.cache_dtype,
        )
        n_devices = kv_params.n_devices
        fetch_types = self.kv_manager.input_symbols()[0]
        len_of_kv_tuple_per_dev = len(list(fetch_types))
        kv_caches_per_dev = [
            tuple(
                kv_inputs_flat[
                    i * len_of_kv_tuple_per_dev : (i + 1)
                    * len_of_kv_tuple_per_dev
                ]
            )
            for i in range(n_devices)
        ]
        return kv_caches_per_dev

    def _build_language_graph(
        self, config: InternVLConfig, state_dict: dict[str, WeightData]
    ) -> Graph:
        """Build the language model graph for text generation with image embeddings."""
        # Initialize graph with input types.
        with Graph(
            "internvl_language", input_types=self._language_graph_input_types()
        ) as graph:
            # Build language model architecture.
            language_model = InternVLLanguageModel(config.llm_config)
            language_model.load_state_dict(
                state_dict=state_dict,
                override_quantization_encoding=True,
                weight_alignment=1,
            )
            self.state_dict = language_model.state_dict()

            # Unpack inputs
            tokens, input_row_offsets, return_n_logits, *variadic_args = (
                graph.inputs
            )

            # Multi-GPU passes a signal buffer per device: unmarshal these.
            signal_buffers = [
                v.buffer for v in variadic_args[: len(self.devices)]
            ]

            # Unmarshal the remaining arguments, which are for KV cache.
            kv_cache = [v.tensor for v in variadic_args[len(self.devices) :]]

            # Execute language model: text + image embeddings -> logits
            outputs = language_model(
                tokens=tokens.tensor,
                signal_buffers=[buf.buffer for buf in signal_buffers],
                kv_cache_inputs_per_dev=self._unflatten_kv_inputs(kv_cache),
                return_n_logits=return_n_logits.tensor,
                input_row_offsets=input_row_offsets.tensor,
            )

            graph.output(*outputs)

            return graph

    def _prepare_vision_inputs(
        self, context_batch: Sequence[TextAndVisionContext]
    ) -> Tensor | None:
        """Batches up pixel_values for vision processing."""
        images = []
        for context in context_batch:
            if (
                context.pixel_values is not None
                and len(context.pixel_values) > 0
            ):
                # InternVL expects images in CHW format
                # context.pixel_values is a list of numpy arrays, take the first one
                image = context.pixel_values[0]  # Shape: [patches, C, H, W]

                # Add batch dimension: [1, patches, C, H, W]
                image = np.expand_dims(image, axis=0)
                images.append(image)

        if not images:
            return None

        # Convert the list into a single NumPy array with shape
        # (batch_size, patches, C, H, W).
        final_images = np.concatenate(images, axis=0)

        return Tensor.from_numpy(final_images).to(self.devices[0])

    def execute(self, model_inputs: ModelInputs) -> ModelOutputs:
        """Executes the InternVL model with the prepared inputs."""
        assert model_inputs.kv_cache_inputs is not None, (
            "InternVL requires KV cache inputs"
        )

        model_inputs = cast(InternVLInputs, model_inputs)

        # Process vision inputs if present
        image_embeddings: Tensor
        if model_inputs.has_vision_inputs:
            assert model_inputs.pixel_values is not None

            # Execute vision model: pixel_values -> image_embeddings.
            vision_outputs = self.vision_model.execute(
                model_inputs.pixel_values
            )
            assert isinstance(vision_outputs[0], Tensor)
            image_embeddings = vision_outputs[0]
        else:
            # Initialize image embeddings as empty tensor for text-only mode
            image_embeddings = Tensor.zeros(
                shape=[0, self.huggingface_config.llm_config.hidden_size],
                dtype=self.dtype,
            ).to(self.devices[0])

        # Prepare KV cache inputs as list of tensors
        assert model_inputs.kv_cache_inputs
        kv_cache_inputs_list = list(model_inputs.kv_cache_inputs)

        # Execute language model with text and image embeddings
        language_outputs = self.language_model.execute(
            model_inputs.input_ids,
            model_inputs.input_row_offsets,
            model_inputs.return_n_logits,
            *model_inputs.signal_buffers,
            *kv_cache_inputs_list,
        )

        # Return model outputs based on what the language model returns
        if len(language_outputs) == 3:
            return ModelOutputs(
                next_token_logits=cast(Tensor, language_outputs[0]),
                logits=cast(Tensor, language_outputs[1]),
                logit_offsets=cast(Tensor, language_outputs[2]),
            )
        else:
            return ModelOutputs(
                next_token_logits=cast(Tensor, language_outputs[0]),
                logits=cast(Tensor, language_outputs[0]),
            )

    def prepare_initial_token_inputs(
        self,
        context_batch: Sequence[TextAndVisionContext],
        kv_cache_inputs: KVCacheInputs | None = None,
        return_n_logits: int = 1,
    ) -> ModelInputs:
        """Prepares the initial inputs for the first execution pass of the InternVL model."""

        # First marshal out the pixel values, since we'll overwrite them.
        pixel_values = self._prepare_vision_inputs(context_batch)

        # Input row offset type: ["input_row_offsets_len"], UInt32
        input_row_offsets = Tensor.from_numpy(
            np.cumsum(
                [0] + [ctx.active_length for ctx in context_batch],
                dtype=np.uint32,
            )
        ).to(self.devices[0])

        # Input Ids: ["total_seq_len"], Int64
        # Create a ragged token vector of length: sum(len(t) for t in tokens).
        tokens = np.concatenate([ctx.next_tokens for ctx in context_batch])
        input_ids = Tensor.from_numpy(tokens).to(self.devices[0])

        # Unset the context's pixel values so that subsequent next_token
        # calls reusing the same context won't run the vision encoder.
        for ctx in context_batch:
            ctx.pixel_values = tuple()

        return InternVLInputs(
            input_ids=input_ids,
            input_row_offsets=input_row_offsets,
            signal_buffers=self.signal_buffers,
            return_n_logits=Tensor.from_numpy(
                np.array([return_n_logits], dtype=np.int64)
            ),
            pixel_values=pixel_values,
            kv_cache_inputs=kv_cache_inputs,
        )

    def prepare_next_token_inputs(
        self, next_tokens: Tensor, prev_model_inputs: ModelInputs
    ) -> ModelInputs:
        """Prepares the inputs for subsequent execution steps in a multi-step generation."""
        assert isinstance(prev_model_inputs, InternVLInputs)
        prev_inputs = prev_model_inputs

        # Use pre-allocated row offsets for next token
        next_row_offsets = self._input_row_offsets_prealloc[
            : prev_inputs.input_row_offsets.shape[0]
        ]

        return InternVLInputs(
            input_ids=next_tokens,
            input_row_offsets=next_row_offsets,
            signal_buffers=self.signal_buffers,
            return_n_logits=prev_model_inputs.return_n_logits,
            # Set vision model inputs to None after the first step
            pixel_values=None,
            kv_cache_inputs=prev_inputs.kv_cache_inputs,
        )

    def load_kv_manager(
        self, session: InferenceSession, available_cache_memory: int | None
    ) -> KVCacheManager:
        """Loads and initializes the KVCacheManager for the InternVL model."""
        return load_kv_manager(
            params=InternVLConfig.get_kv_params(
                huggingface_config=self.huggingface_config,
                n_devices=len(self.devices),
                kv_cache_config=self.kv_cache_config,
                cache_dtype=self.encoding.cache_dtype,
            ),
            max_batch_size=self.pipeline_config.max_batch_size,
            max_seq_len=self.calculate_max_seq_len(
                self.pipeline_config, huggingface_config=self.huggingface_config
            ),
            num_layers=InternVLConfig.get_num_layers(
                huggingface_config=self.huggingface_config
            ),
            devices=self.devices,
            available_cache_memory=available_cache_memory,
            page_size=self.kv_cache_config.kv_cache_page_size,
            session=session,
        )
