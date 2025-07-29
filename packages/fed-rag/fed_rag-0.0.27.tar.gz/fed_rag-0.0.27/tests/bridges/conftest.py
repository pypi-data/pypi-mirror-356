from typing import Any

import numpy as np
import pytest
import torch
from pydantic import PrivateAttr
from torch.utils.data import DataLoader, Dataset

from fed_rag.base.generator import BaseGenerator
from fed_rag.base.knowledge_store import BaseAsyncKnowledgeStore
from fed_rag.base.retriever import BaseRetriever
from fed_rag.base.tokenizer import BaseTokenizer
from fed_rag.core.rag_system import AsyncRAGSystem, RAGSystem
from fed_rag.data_structures import KnowledgeNode, RAGConfig
from fed_rag.knowledge_stores.in_memory import InMemoryKnowledgeStore


class _TestDataset(Dataset):
    def __init__(self, size: int) -> None:
        self.features = np.random.rand(size, 2)
        self.labels = np.random.choice(2, size=size)

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int) -> tuple[np.ndarray, Any]:
        return self.features[index], self.labels[index]


@pytest.fixture()
def train_dataloader() -> DataLoader:
    dataset = _TestDataset(size=10)
    return DataLoader(dataset, batch_size=2, shuffle=True)


@pytest.fixture()
def val_dataloader() -> DataLoader:
    dataset = _TestDataset(size=4)
    return DataLoader(dataset, batch_size=2, shuffle=True)


class MockRetriever(BaseRetriever):
    _encoder: torch.nn.Module = PrivateAttr(default=torch.nn.Linear(3, 3))

    def encode_context(self, context: str, **kwargs: Any) -> torch.Tensor:
        return self._encoder.forward(torch.ones(3))

    def encode_query(self, query: str, **kwargs: Any) -> torch.Tensor:
        return self._encoder.forward(torch.zeros(3))

    @property
    def encoder(self) -> torch.nn.Module:
        return self._encoder

    @encoder.setter
    def encoder(self, value: torch.nn.Module) -> None:
        self._encoder = value

    @property
    def query_encoder(self) -> torch.nn.Module | None:
        return None

    @property
    def context_encoder(self) -> torch.nn.Module | None:
        return None


@pytest.fixture
def mock_retriever() -> MockRetriever:
    return MockRetriever()


class MockDualRetriever(BaseRetriever):
    _query_encoder: torch.nn.Module = PrivateAttr(
        default=torch.nn.Linear(2, 1)
    )
    _context_encoder: torch.nn.Module = PrivateAttr(
        default=torch.nn.Linear(2, 1)
    )

    def encode_context(self, context: str, **kwargs: Any) -> torch.Tensor:
        return self._encoder.forward(torch.ones(2))

    def encode_query(self, query: str, **kwargs: Any) -> torch.Tensor:
        return self._encoder.forward(torch.zeros(2))

    @property
    def encoder(self) -> torch.nn.Module | None:
        return None

    @property
    def query_encoder(self) -> torch.nn.Module | None:
        return self._query_encoder

    @query_encoder.setter
    def query_encoder(self, value: torch.nn.Module) -> None:
        self._query_encoder = value

    @property
    def context_encoder(self) -> torch.nn.Module | None:
        return self._context_encoder

    @context_encoder.setter
    def context_encoder(self, value: torch.nn.Module) -> None:
        self._context_encoder = value


@pytest.fixture
def mock_dual_retriever() -> MockDualRetriever:
    return MockDualRetriever()


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


@pytest.fixture
def another_mock_rag_system(
    mock_generator: BaseGenerator,
    mock_retriever: BaseRetriever,
) -> RAGSystem:
    knowledge_store = InMemoryKnowledgeStore()
    rag_config = RAGConfig(
        top_k=1,
    )
    return RAGSystem(
        generator=mock_generator,
        retriever=mock_retriever,
        knowledge_store=knowledge_store,
        rag_config=rag_config,
    )


class DummyAsyncKnowledgeStore(BaseAsyncKnowledgeStore):
    nodes: list[KnowledgeNode] = []

    async def load_node(self, node: KnowledgeNode) -> None:
        self.nodes.append(node)

    async def retrieve(
        self, query_emb: list[float], top_k: int
    ) -> list[tuple[float, KnowledgeNode]]:
        return []

    async def batch_retrieve(
        self, query_embs: list[list[float]], top_k: int
    ) -> list[list[tuple[float, KnowledgeNode]]]:
        return [[]]

    async def delete_node(self, node_id: str) -> bool:
        return True

    async def clear(self) -> None:
        self.nodes.clear()

    async def count(self) -> int:
        return len(self.nodes)

    async def persist(self) -> None:
        pass

    async def load(self) -> None:
        pass


@pytest.fixture
def mock_async_rag_system(
    mock_generator: BaseGenerator,
    mock_retriever: BaseRetriever,
) -> AsyncRAGSystem:
    knowledge_store = DummyAsyncKnowledgeStore()
    rag_config = RAGConfig(
        top_k=2,
    )
    return AsyncRAGSystem(
        generator=mock_generator,
        retriever=mock_retriever,
        knowledge_store=knowledge_store,
        rag_config=rag_config,
    )
