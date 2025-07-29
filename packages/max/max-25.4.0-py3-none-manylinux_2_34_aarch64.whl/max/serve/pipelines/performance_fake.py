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

import dataclasses
import json
import logging
import random
import threading
from collections.abc import Iterable, Sequence
from os import environ
from time import sleep, time
from typing import Literal, Optional, Union

import numpy as np
from max.pipelines.core import (
    TextGenerationResponse,
    TextGenerationStatus,
    TextResponse,
    TokenGenerator,
    TokenGeneratorRequest,
)
from max.pipelines.lib.tokenizer import PreTrainedPipelineTokenizer
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast


@dataclasses.dataclass
class PerformanceFakingContext:
    # simulation attributes
    prompt_len: int
    context_len: int
    active_length: int
    max_tokens: int

    # correctness attributes
    prompt: Union[str, Sequence[int]]
    encoded_prompt: np.ndarray

    # Scheduler_V2 use them to determine if a context has been chunked.
    start_idx: int = 0
    active_idx: int = 0
    cache_seq_id: int = -1

    # Used by frontend to make Usage objects
    current_length: int = 0

    def assign_to_cache(self, cache_seq_id: int) -> None:
        """Assigns the context to a cache slot."""
        self.cache_seq_id = cache_seq_id

    def unassign_from_cache(self) -> None:
        """Unassigns the context from a cache slot."""
        self.cache_seq_id = -1

    @property
    def is_assigned_to_cache(self) -> bool:
        """Returns True if input is assigned to a cache slot, False otherwise."""
        return self.cache_seq_id != -1

    @property
    def next_tokens(self) -> np.ndarray:
        """Returns the next tokens to be generated."""
        return np.array([], dtype=np.int32)


@dataclasses.dataclass
class BatchInfo:
    """Information about a batch of requests passed to the pipeline"""

    past_seq_lens: list[int]
    """Coordinated list of past sequence lengths (i.e. context lengths)"""

    seq_lens: list[int]
    """Coordinated list of sequence lengths, i.e. prompt_len or 1"""

    num_steps: int
    """Number of steps to do in the pipeline"""


class PerformanceFakingPipelineTokenizer(
    PreTrainedPipelineTokenizer[PerformanceFakingContext]
):
    def __init__(
        self, delegate: Union[PreTrainedTokenizer, PreTrainedTokenizerFast]
    ) -> None:
        super().__init__(delegate)
        self.logger = logging.getLogger(self.__class__.__name__)
        # amount of time spent in the tokenizer
        self.tokenizer_secs = 0.0

    async def new_context(
        self, request: TokenGeneratorRequest
    ) -> PerformanceFakingContext:
        prompt: Union[str, Sequence[int]]
        if request.prompt is not None:
            prompt = request.prompt
        elif request.messages is not None:
            prompt = self.apply_chat_template(request.messages)
        else:
            raise ValueError(f"{request} does not provide messages or prompt.")
        encoded_prompt = await self.encode(prompt)
        prompt_length = len(encoded_prompt)
        num_tokens = request.sampling_params.max_new_tokens or prompt_length
        return PerformanceFakingContext(
            prompt_length,
            0,
            prompt_length,
            num_tokens,
            prompt,
            np.array(encoded_prompt),
        )

    async def encode(
        self, prompt: Union[str, Sequence[int]], add_special_tokens: bool = True
    ) -> np.ndarray:
        start = time()
        if isinstance(prompt, str):
            encoded = await super().encode(
                prompt, add_special_tokens=add_special_tokens
            )
        else:
            encoded = np.array(list(prompt))
        self.tokenizer_secs += time() - start
        return encoded

    async def decode(
        self, context: PerformanceFakingContext, encoded: np.ndarray, **kwargs
    ) -> str:
        # Not actually an np.ndarray!
        return encoded  # type: ignore

    def __del__(self) -> None:
        self.logger.info(
            "PerformanceFake: tokenized for"
            f" {self.tokenizer_secs:.4f} sec total"
        )


class PerformanceFakingTokenGenerator(TokenGenerator[PerformanceFakingContext]):
    def __init__(
        self,
        ce_baseline: float,
        ce_rate: float,
        ce_padding: bool,
        tg_baseline: float,
        tg_rate_no_context: float,
        tg_rate_per_context_token: float,
        tg_padding: bool,
        busy_wait: bool,
        failure_percentage: Optional[int] = None,
    ) -> None:
        """Parameterize a performance fake

        Args:
            ce_baseline: The minimum amount of time context encoding can take
            ce_rate: The context encoding time per prompt token
            ce_padding: Whether or not prompts are padding to equal length
            tg_baseline: The minimum amount of time token generation can take
            tg_rate_no_context: The token generation time per request with no context
            tg_rate_per_context_token: The additional token generation time per context token
            tg_padding: Whether or not contexts are padded to the same length
            busy_wait: Whether to wait on the fake GPU as a busy-loop, vs sleep
        """
        super().__init__()
        self.ce_baseline = ce_baseline
        self.ce_rate = ce_rate
        self.ce_padding = ce_padding
        self.tg_baseline = tg_baseline
        self.tg_rate_no_context = tg_rate_no_context
        self.tg_rate_per_context_token = tg_rate_per_context_token
        self.tg_padding = tg_padding
        self.busy_wait = busy_wait
        self.failure_predicate = None
        if failure_percentage:

            def sim_failure_lambda(sim_failure: int) -> bool:
                return random.randint(0, 100) < min(sim_failure, 100)

            self.failure_predicate = lambda: sim_failure_lambda(
                failure_percentage
            )

        self.batch_info_output_fname: Optional[str] = environ.get(
            "MAX_BATCH_INFO_FILENAME"
        )

        self.logger: logging.Logger = logging.getLogger(__name__)

        # lock to prevent concurrent usage of the fake GPU
        self.wait_lock = threading.Lock()
        # amount of time waited in the fake GPU
        self.wait_secs = 0.0
        # number of times waited in the fake GPU
        self.wait_count = 0
        # timestamp of the end of the last GPU wait
        self.last_wait_end: Optional[float] = None
        # amount of time spent in between waiting
        self.non_wait_secs: float = 0
        # record of batches
        self.batch_infos: list[BatchInfo] = []

    def next_token(
        self, batch: dict[str, PerformanceFakingContext], num_steps: int = 1
    ) -> dict[str, TextGenerationResponse]:
        if self.batch_info_output_fname is not None:
            self._record_batch_info(batch.values(), num_steps)

        response = {}
        for step in range(num_steps):
            context_lengths = [x.context_len for x in batch.values()]
            if sum(context_lengths) == 0:
                self.logger.debug(
                    f"PerformanceFake: CE with batch_size = {len(batch)}"
                )
                # context encoding mode
                wait_time = self._ce_time_ms(
                    [x.prompt_len for x in batch.values()]
                )
                for _, ctx in batch.items():
                    if self.failure_predicate and self.failure_predicate():
                        raise Exception(
                            "performance fake simulated failure in CE"
                        )
                    ctx.context_len += ctx.prompt_len
                    ctx.active_length = 1
            else:
                # token generation mode
                self.logger.debug(
                    f"PerformanceFake: TG with batch_size = {len(batch)}"
                )
                wait_time = self._tg_time_ms(
                    [x.context_len for x in batch.values()]
                )
                for _, ctx in batch.items():
                    if self.failure_predicate and self.failure_predicate():
                        raise Exception(
                            "performance fake simulated failure in TG"
                        )
                    ctx.context_len += 1

            # actually wait here
            self._wait(wait_time)

            for request_id, context in batch.items():
                if request_id not in response:
                    response[request_id] = TextGenerationResponse(
                        [], TextGenerationStatus.ACTIVE
                    )

                if (
                    context.context_len - context.prompt_len
                    >= context.max_tokens
                ):
                    response[request_id].update_status(
                        TextGenerationStatus.MAXIMUM_LENGTH
                    )
                    break

                response[request_id].append_token(
                    TextResponse(
                        next_token=context.prompt[
                            -((context.context_len + 1) % context.prompt_len)
                        ]
                    )
                )

        return response

    def release(self, context: PerformanceFakingContext) -> None:
        pass

    def _wait(self, wait_time_ms: float) -> None:
        self.logger.debug(f"PerformanceFake: waiting {wait_time_ms} ms")
        self.wait_secs += wait_time_ms * 0.001
        self.wait_count += 1
        with self.wait_lock:
            start = time()
            if self.last_wait_end is not None:
                self.logger.debug(
                    "PerformanceFake: waiting after"
                    f" {start - self.last_wait_end:.4f} sec"
                )
                self.non_wait_secs += start - self.last_wait_end
            if self.busy_wait:
                while (time() - start) * 1000 < wait_time_ms:
                    pass
            else:
                sleep(wait_time_ms * 0.001)
            self.last_wait_end = time()

    def _ce_time_ms(self, prompt_sizes: Sequence[int]) -> float:
        if self.ce_padding:
            N = len(prompt_sizes) * max(prompt_sizes)
        else:
            N = sum(prompt_sizes)
        return max(self.ce_rate * N, self.ce_baseline)

    def _tg_time_ms(self, context_sizes: Sequence[int]) -> float:
        if self.tg_padding:
            N = len(context_sizes) * max(context_sizes)
        else:
            N = sum(context_sizes)

        return (
            max(self.tg_baseline, self.tg_rate_no_context * len(context_sizes))
            + N * self.tg_rate_per_context_token
        )

    def _record_batch_info(
        self, contexts: Iterable[PerformanceFakingContext], num_steps: int
    ) -> None:
        self.batch_infos.append(
            BatchInfo(
                past_seq_lens=[x.context_len for x in contexts],
                seq_lens=[x.active_length for x in contexts],
                num_steps=num_steps,
            )
        )

    def __del__(self) -> None:
        # print the total wait time for benchmarking/debugging purposes
        self.logger.info(
            f"PerformanceFake: waited {self.wait_count} times for"
            f" {self.wait_secs:.4f} sec total"
        )
        self.logger.info(
            "PerformanceFake: not waiting for"
            f" {self.non_wait_secs:.4f} sec total"
        )
        if self.batch_info_output_fname is not None:
            output = {
                "batch_data": [dataclasses.asdict(x) for x in self.batch_infos]
            }
            with open(self.batch_info_output_fname, "w") as f:
                json.dump(output, f, indent=2)
                f.flush()  # Refer to MAXSERV-893


def get_performance_fake(
    mode: Literal["no-op", "speed-of-light", "vllm"],
    failure_percentage: Optional[int] = None,
) -> PerformanceFakingTokenGenerator:
    """Construct a performance fake for the given performance mode."""
    if mode == "no-op":
        return PerformanceFakingTokenGenerator(
            ce_baseline=0,
            ce_rate=0,
            ce_padding=False,
            tg_baseline=0,
            tg_rate_no_context=0,
            tg_rate_per_context_token=0,
            tg_padding=False,
            busy_wait=False,
            failure_percentage=failure_percentage,
        )
    elif mode == "speed-of-light":
        # current defaults are speed-of-light on A100-80GB
        return PerformanceFakingTokenGenerator(
            ce_baseline=6.85,
            ce_rate=54043.08 / 1024 / 1024,
            ce_padding=False,
            tg_baseline=6.85,
            tg_rate_no_context=12.67 / 256,
            tg_rate_per_context_token=(21.11 / 256 - 12.67 / 256) / 512,
            tg_padding=False,
            busy_wait=False,
            failure_percentage=failure_percentage,
        )
    elif mode == "vllm":
        # this is for A100-80GB
        return PerformanceFakingTokenGenerator(
            ce_baseline=11.95,
            ce_rate=19487 / 1024 / 256,
            ce_padding=False,
            tg_baseline=11.95,
            tg_rate_no_context=33.66 / 256,
            tg_rate_per_context_token=(59.79 - 33.66) / 256 / 1024,
            tg_padding=False,
            busy_wait=False,
            failure_percentage=failure_percentage,
        )
    else:
        raise ValueError(f"Unexpected mode: {mode}")
