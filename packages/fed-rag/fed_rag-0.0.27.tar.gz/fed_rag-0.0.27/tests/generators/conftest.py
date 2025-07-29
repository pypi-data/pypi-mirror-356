from typing import Any

import pytest
import torch
from peft import LoraConfig, PeftModel, get_peft_model
from tokenizers import Tokenizer, models
from transformers import (
    PretrainedConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

from fed_rag.base.generator import BaseGenerator
from fed_rag.base.tokenizer import BaseTokenizer


class _TestHFConfig(PretrainedConfig):
    model_type = "testmodel"

    def __init__(self, num_hidden: int = 42, **kwargs: Any):
        super().__init__(**kwargs)
        self.num_hidden = num_hidden


class _TestHFPretrainedModel(PreTrainedModel):
    config_class = _TestHFConfig

    def __init__(self, config: _TestHFConfig):
        super().__init__(config)
        self.config = config
        self.model = torch.nn.Linear(3, self.config.num_hidden)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        return self.model(input)


@pytest.fixture
def dummy_tokenizer() -> PreTrainedTokenizer:
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
    return PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        pad_token="[PAD]",
        cls_token="[CLS]",
        sep_token="[SEP]",
        mask_token="[MASK]",
    )


@pytest.fixture
def dummy_pretrained_model_and_tokenizer(
    dummy_tokenizer: PreTrainedTokenizer,
) -> tuple[PreTrainedModel, PreTrainedTokenizer]:
    return _TestHFPretrainedModel(_TestHFConfig()), dummy_tokenizer


@pytest.fixture
def dummy_peft_model_and_tokenizer(
    dummy_tokenizer: PreTrainedTokenizer,
) -> tuple[PeftModel, PreTrainedTokenizer]:
    class MLP(torch.nn.Module):
        """Taken from Peft's documentation, specifially 'Custom Models'.

        https://huggingface.co/docs/peft/main/en/developer_guides/custom_models
        """

        def __init__(self, num_units_hidden: int = 40):
            super().__init__()
            self.seq = torch.nn.Sequential(
                torch.nn.Linear(20, num_units_hidden),
                torch.nn.ReLU(),
                torch.nn.Linear(num_units_hidden, num_units_hidden),
                torch.nn.ReLU(),
                torch.nn.Linear(num_units_hidden, 2),
                torch.nn.LogSoftmax(dim=-1),
            )

        def forward(self, X: torch.Tensor) -> torch.Tensor:
            return self.seq(X)

    config = LoraConfig(
        target_modules=["seq.0", "seq.2"],
        r=4,
    )

    base_model = MLP()
    return get_peft_model(base_model, config), dummy_tokenizer


class MockTokenizer(BaseTokenizer):
    def encode(self, input: str, **kwargs: Any) -> list[int]:
        return [0, 1, 2]

    def decode(self, input_ids: list[int], **kwargs: Any) -> str:
        return "mock decoded sentence"

    @property
    def unwrapped(self) -> None:
        return None


@pytest.fixture()
def mock_tokenizer() -> BaseTokenizer:
    return MockTokenizer()


class MockGenerator(BaseGenerator):
    _model = torch.nn.Linear(2, 1)
    _tokenizer = MockTokenizer()
    _prompt_template = "{query} and {context}"

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return f"mock completion output from '{prompt}'."

    def generate(self, query: str, context: str, **kwargs: Any) -> str:
        return f"mock output from '{query}' and '{context}'."

    def compute_target_sequence_proba(self, prompt: str, target: str) -> float:
        return 0.42

    @property
    def model(self) -> torch.nn.Module:
        return self._model

    @model.setter
    def model(self, value: torch.nn.Module) -> None:
        self._model = value

    @property
    def tokenizer(self) -> MockTokenizer:
        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, value: BaseTokenizer) -> None:
        self._tokenizer = value

    @property
    def prompt_template(self) -> str:
        return self._prompt_template

    @prompt_template.setter
    def prompt_template(self, v: str) -> None:
        self._prompt_template = v


@pytest.fixture
def mock_generator() -> BaseGenerator:
    return MockGenerator()
