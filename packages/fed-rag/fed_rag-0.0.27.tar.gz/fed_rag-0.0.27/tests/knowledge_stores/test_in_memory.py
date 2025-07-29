import tempfile
from pathlib import Path

import pytest
import torch

from fed_rag.base.knowledge_store import BaseKnowledgeStore
from fed_rag.data_structures.knowledge_node import KnowledgeNode
from fed_rag.exceptions import KnowledgeStoreNotFoundError
from fed_rag.knowledge_stores.in_memory import InMemoryKnowledgeStore


@pytest.fixture
def text_nodes() -> list[KnowledgeNode]:
    return [
        KnowledgeNode(
            embedding=[1.0, 0.0, 1.0],
            node_type="text",
            text_content="node 1",
            metadata={"key1": "value1"},
        ),
        KnowledgeNode(
            embedding=[1.0, 0.0, 0.0],
            node_type="text",
            text_content="node 2",
            metadata={"key2": "value2"},
        ),
        KnowledgeNode(
            embedding=[1.0, 1.0, 0.0],
            node_type="text",
            text_content="node 3",
            metadata={"key3": "value3"},
        ),
    ]


def test_in_memory_knowledge_store_class() -> None:
    names_of_base_classes = [
        b.__name__ for b in InMemoryKnowledgeStore.__mro__
    ]
    assert BaseKnowledgeStore.__name__ in names_of_base_classes


def test_in_memory_knowledge_store_init() -> None:
    knowledge_store = InMemoryKnowledgeStore()

    assert knowledge_store.count == 0


def test_from_nodes(text_nodes: list[KnowledgeNode]) -> None:
    knowledge_store = InMemoryKnowledgeStore.from_nodes(nodes=text_nodes)

    assert knowledge_store.count == 3
    assert all(n.node_id in knowledge_store._data for n in text_nodes)


def test_delete_node(text_nodes: list[KnowledgeNode]) -> None:
    knowledge_store = InMemoryKnowledgeStore.from_nodes(nodes=text_nodes)

    assert knowledge_store.count == 3

    res = knowledge_store.delete_node(text_nodes[0].node_id)

    assert res is True
    assert knowledge_store.count == 2
    assert text_nodes[0].node_id not in knowledge_store._data


def test_delete_node_returns_false(text_nodes: list[KnowledgeNode]) -> None:
    knowledge_store = InMemoryKnowledgeStore.from_nodes(nodes=text_nodes)

    assert knowledge_store.count == 3

    res = knowledge_store.delete_node("non_included_id")

    assert res is False
    assert knowledge_store.count == 3
    assert all(n.node_id in knowledge_store._data for n in text_nodes)


def test_load_node(text_nodes: list[KnowledgeNode]) -> None:
    knowledge_store = InMemoryKnowledgeStore()
    assert knowledge_store.count == 0

    knowledge_store.load_node(text_nodes[-1])

    assert knowledge_store.count == 1
    assert text_nodes[-1].node_id in knowledge_store._data


def test_load_nodes(text_nodes: list[KnowledgeNode]) -> None:
    knowledge_store = InMemoryKnowledgeStore()
    assert knowledge_store.count == 0

    knowledge_store.load_nodes(text_nodes)

    assert knowledge_store.count == 3
    assert all(n.node_id in knowledge_store._data for n in text_nodes)


@pytest.mark.parametrize(
    ("query_emb", "top_k", "expected_node_ix"),
    [([1.0, 1.0, 1.0], 2, [0, 2]), ([0.5, 0.0, 0.0], 1, [1])],
    ids=[str([1.0, 1.0, 1.0]), str([0.5, 0.0, 0.0])],
)
def test_load_and_offload_nodes(
    query_emb: list[float],
    top_k: int,
    expected_node_ix: list[int],
    text_nodes: list[KnowledgeNode],
) -> None:
    knowledge_store = InMemoryKnowledgeStore()
    assert knowledge_store.count == 0

    knowledge_store.load_nodes(text_nodes)
    # act
    res = knowledge_store.retrieve(query_emb, top_k=top_k)
    # assert
    assert [el[1] for el in res] == [text_nodes[ix] for ix in expected_node_ix]
    # print(isinstance(knowledge_store._data_storage, torch.Tensor))
    knowledge_store.delete_node(text_nodes[0].node_id)
    assert knowledge_store.count == 2
    res = knowledge_store.retrieve(query_emb, top_k=top_k)
    node = KnowledgeNode(
        embedding=[1.0, 1.0, 0.0],
        node_type="text",
        text_content="node 4",
        metadata={"key4": "value4"},
    )
    knowledge_store.load_nodes([node])
    assert not isinstance(knowledge_store._data_storage, torch.Tensor)


def test_clear(text_nodes: list[KnowledgeNode]) -> None:
    knowledge_store = InMemoryKnowledgeStore.from_nodes(nodes=text_nodes)
    assert knowledge_store.count == 3

    knowledge_store.clear()

    assert knowledge_store.count == 0
    assert all(n.node_id not in knowledge_store._data for n in text_nodes)


@pytest.mark.parametrize(
    ("query_emb", "top_k", "expected_node_ix"),
    [([1.0, 1.0, 1.0], 2, [0, 2]), ([0.5, 0.0, 0.0], 1, [1])],
    ids=[str([1.0, 1.0, 1.0]), str([0.5, 0.0, 0.0])],
)
def test_retrieve(
    query_emb: list[float],
    top_k: int,
    expected_node_ix: list[int],
    text_nodes: list[KnowledgeNode],
) -> None:
    # arrange
    knowledge_store = InMemoryKnowledgeStore.from_nodes(nodes=text_nodes)

    # act
    res = knowledge_store.retrieve(query_emb, top_k=top_k)

    # assert
    assert [el[1] for el in res] == [text_nodes[ix] for ix in expected_node_ix]


def test_persist(text_nodes: list[KnowledgeNode]) -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        knowledge_store = InMemoryKnowledgeStore.from_nodes(nodes=text_nodes)
        knowledge_store.cache_dir = dirpath
        knowledge_store.persist()

        filename = Path(dirpath) / f"{knowledge_store.name}.parquet"
        assert filename.exists()


def test_load(text_nodes: list[KnowledgeNode]) -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        knowledge_store = InMemoryKnowledgeStore.from_nodes(
            nodes=text_nodes, name="test_ks", cache_dir=dirpath
        )
        knowledge_store.persist()

        # load into new empty instance
        loaded_knowledge_store = InMemoryKnowledgeStore(
            name="test_ks", cache_dir=dirpath
        )
        loaded_knowledge_store.load()

        assert loaded_knowledge_store._data == knowledge_store._data


def test_load_with_missing_file_raises_error() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        knowledge_store = InMemoryKnowledgeStore(cache_dir=dirpath)

        with pytest.raises(KnowledgeStoreNotFoundError):
            knowledge_store.load()


def test_persist_overwrite(text_nodes: list[KnowledgeNode]) -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        knowledge_store = InMemoryKnowledgeStore.from_nodes(
            nodes=text_nodes, name="test_ks", cache_dir=dirpath
        )
        knowledge_store.persist()

        # overwrite
        knowledge_store.load_node(
            KnowledgeNode(
                embedding=[1.0, 1.0, 1.0],
                node_type="text",
                text_content="node 4",
                metadata={"key4": "value4"},
            )
        )
        knowledge_store.persist()

        # load into new empty instance
        loaded_knowledge_store = InMemoryKnowledgeStore(
            name="test_ks", cache_dir=dirpath
        )
        loaded_knowledge_store.load()

        assert loaded_knowledge_store._data == knowledge_store._data


def test_batch_retrieve_raises_error() -> None:
    with tempfile.TemporaryDirectory() as dirpath:
        knowledge_store = InMemoryKnowledgeStore(cache_dir=dirpath)

        with pytest.raises(NotImplementedError):
            knowledge_store.batch_retrieve(query_embs=[[1, 2, 3], [4, 5, 6]])
