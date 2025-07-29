from typing import Any

import pytest
import torch
from pydantic import PrivateAttr

from fed_rag import RAGConfig, RAGSystem
from fed_rag.base.generator import BaseGenerator
from fed_rag.base.retriever import BaseRetriever
from fed_rag.base.tokenizer import BaseTokenizer
from fed_rag.knowledge_stores.in_memory import InMemoryKnowledgeStore


class MockRetriever(BaseRetriever):
    _encoder: torch.nn.Module = PrivateAttr(default=torch.nn.Linear(3, 3))

    def encode_context(self, context: str, **kwargs: Any) -> torch.Tensor:
        return self._encoder.forward(torch.ones(3))

    def encode_query(self, query: str, **kwargs: Any) -> torch.Tensor:
        return self._encoder.forward(torch.zeros(3))

    @property
    def encoder(self) -> torch.nn.Module:
        return self._encoder

    @property
    def query_encoder(self) -> torch.nn.Module | None:
        return None

    @property
    def context_encoder(self) -> torch.nn.Module | None:
        return None


@pytest.fixture
def mock_retriever() -> MockRetriever:
    return MockRetriever()


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


@pytest.fixture
def mock_rag_system(
    mock_generator: BaseGenerator,
    mock_retriever: BaseRetriever,
) -> RAGSystem:
    knowledge_store = InMemoryKnowledgeStore()
    rag_config = RAGConfig(
        top_k=2,
    )
    return RAGSystem(
        generator=mock_generator,
        retriever=mock_retriever,
        knowledge_store=knowledge_store,
        rag_config=rag_config,
    )
