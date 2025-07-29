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

"""Standardized response object for Pipeline Inference."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np


class LogProbabilities:
    """Log probabilities for an individual output token.

    Attributes:
        token_log_probabilities (list[float]): Probabilities of each token.
        top_log_probabilities (list[dict[int, float]]): Top tokens and their corresponding probabilities.

    """

    def __init__(
        self,
        token_log_probabilities: list[float],
        top_log_probabilities: list[dict[int, float]],
    ) -> None:
        self.token_log_probabilities = token_log_probabilities
        self.top_log_probabilities = top_log_probabilities

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LogProbabilities):
            return False

        if len(self.token_log_probabilities) != len(
            other.token_log_probabilities
        ):
            return False

        if not all(
            a == b
            for a, b in zip(
                self.token_log_probabilities, other.token_log_probabilities
            )
        ):
            return False

        if len(self.top_log_probabilities) != len(other.top_log_probabilities):
            return False

        if not all(
            a == b
            for a, b in zip(
                self.top_log_probabilities, other.top_log_probabilities
            )
        ):
            return False

        return True


class TextResponse:
    """A base class for model response, specifically for Text model variants.

    Attributes:
        next_token (int | str): Encoded predicted next token.
        log_probabilities (LogProbabilities | None): Log probabilities of each output token.

    """

    def __init__(
        self,
        next_token: int | str,
        log_probabilities: LogProbabilities | None = None,
    ) -> None:
        self.next_token = next_token
        self.log_probabilities = log_probabilities

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, TextResponse):
            return False

        return (
            self.next_token == value.next_token
            and self.log_probabilities == value.log_probabilities
        )


@dataclass
class EmbeddingsResponse:
    """Container for the response from embeddings pipeline."""

    embeddings: np.ndarray


class TextGenerationStatus(str, Enum):
    ACTIVE = "active"
    END_OF_SEQUENCE = "end_of_sequence"
    MAXIMUM_LENGTH = "maximum_length"

    @property
    def is_done(self) -> bool:
        return self is not TextGenerationStatus.ACTIVE


class TextGenerationResponse:
    def __init__(
        self, tokens: list[TextResponse], final_status: TextGenerationStatus
    ) -> None:
        self._tokens = tokens
        self._final_status = final_status

    @property
    def is_done(self) -> bool:
        return self._final_status.is_done

    @property
    def tokens(self) -> list[TextResponse]:
        return self._tokens

    @property
    def final_status(self) -> TextGenerationStatus:
        return self._final_status

    def append_token(self, token: TextResponse) -> None:
        self._tokens.append(token)

    def update_status(self, status: TextGenerationStatus) -> None:
        self._final_status = status


class AudioGenerationResponse:
    def __init__(
        self,
        final_status: TextGenerationStatus,
        audio: np.ndarray | None = None,
    ) -> None:
        self._audio = audio
        self._final_status = final_status

    @property
    def is_done(self) -> bool:
        return self._final_status.is_done

    @property
    def has_audio_data(self) -> bool:
        return self._audio is not None

    @property
    def audio_data(self) -> np.ndarray:
        assert self._audio is not None
        return self._audio

    @property
    def final_status(self) -> TextGenerationStatus:
        return self._final_status
