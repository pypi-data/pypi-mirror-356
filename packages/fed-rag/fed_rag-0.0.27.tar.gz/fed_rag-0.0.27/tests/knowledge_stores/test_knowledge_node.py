from unittest.mock import MagicMock, patch

import pytest

from fed_rag.data_structures.knowledge_node import KnowledgeNode, NodeContent


@patch("fed_rag.data_structures.knowledge_node.uuid")
def test_text_knowledge_node_init(mock_uuid: MagicMock) -> None:
    mock_uuid.uuid4.return_value = "mock_id"
    node = KnowledgeNode(
        embedding=[0.1, 0.2, 0.3], node_type="text", text_content="mock_text"
    )

    assert node.node_id == "mock_id"
    assert node.embedding == [0.1, 0.2, 0.3]
    assert node.node_type == "text"
    assert node.text_content == "mock_text"


def test_text_knowledge_node_init_raises_validation_error() -> None:
    with pytest.raises(
        ValueError, match="NodeType == 'text', but text_content is None."
    ):
        KnowledgeNode(
            node_id="mock_id", embedding=[0.1, 0.2, 0.3], node_type="text"
        )


@patch("fed_rag.data_structures.knowledge_node.uuid")
def test_image_knowledge_node_init(mock_uuid: MagicMock) -> None:
    mock_uuid.uuid4.return_value = "mock_id"
    node = KnowledgeNode(
        embedding=[0.1, 0.2, 0.3],
        node_type="image",
        image_content=b"mock_base64_str",
    )

    assert node.node_id == "mock_id"
    assert node.embedding == [0.1, 0.2, 0.3]
    assert node.node_type == "image"
    assert isinstance(node.image_content, bytes)
    assert node.image_content == b"mock_base64_str"


def test_image_knowledge_node_init_raises_validation_error() -> None:
    with pytest.raises(
        ValueError, match="NodeType == 'image', but image_content is None."
    ):
        KnowledgeNode(
            node_id="mock_id", embedding=[0.1, 0.2, 0.3], node_type="image"
        )


@patch("fed_rag.data_structures.knowledge_node.uuid")
def test_multimodal_knowledge_node_init(mock_uuid: MagicMock) -> None:
    mock_uuid.uuid4.return_value = "mock_id"
    node = KnowledgeNode(
        embedding=[0.1, 0.2, 0.3],
        node_type="multimodal",
        text_content="fake content",
        image_content=b"mock_base64_str",
    )

    assert node.node_id == "mock_id"
    assert node.embedding == [0.1, 0.2, 0.3]
    assert node.text_content == "fake content"
    assert node.node_type == "multimodal"
    assert isinstance(node.image_content, bytes)
    assert node.image_content == b"mock_base64_str"


def test_multimodal_knowledge_node_init_raises_validation_error_missing_text() -> (
    None
):
    with pytest.raises(
        ValueError, match="NodeType == 'multimodal', but text_content is None."
    ):
        KnowledgeNode(
            node_id="mock_id",
            embedding=[0.1, 0.2, 0.3],
            node_type="multimodal",
        )


def test_multimodal_knowledge_node_init_raises_validation_error_missing_image() -> (
    None
):
    with pytest.raises(
        ValueError,
        match="NodeType == 'multimodal', but image_content is None.",
    ):
        KnowledgeNode(
            node_id="mock_id",
            embedding=[0.1, 0.2, 0.3],
            node_type="multimodal",
            text_content="fake content",
        )


@pytest.mark.parametrize(
    ("node", "expected_content"),
    [
        (
            KnowledgeNode(
                node_type="text",
                embedding=[0.1, 0.2],
                text_content="fake content",
            ),
            {"text_content": "fake content", "image_content": None},
        ),
        (
            KnowledgeNode(
                node_type="image",
                embedding=[0.1, 0.2],
                image_content=b"fake-base64-str",
            ),
            {"text_content": None, "image_content": b"fake-base64-str"},
        ),
        (
            KnowledgeNode(
                node_type="multimodal",
                embedding=[0.1, 0.2],
                text_content="fake content",
                image_content=b"fake-base64-str",
            ),
            {
                "text_content": "fake content",
                "image_content": b"fake-base64-str",
            },
        ),
    ],
)
def test_get_content(
    node: KnowledgeNode, expected_content: NodeContent
) -> None:
    assert node.get_content() == expected_content


def test_serialize_metadata() -> None:
    # test when metadata is None
    node = KnowledgeNode(
        node_type="text",
        embedding=[0.1, 0.2],
        text_content="content",
    )
    serialized_content = node.model_dump()
    assert not serialized_content["metadata"]

    # test when metadata is not None
    node = KnowledgeNode(
        node_type="text",
        embedding=[0.1, 0.2],
        text_content="content",
        metadata={"key1": "value1", "key2": "value2"},
    )
    serialized_content = node.model_dump()
    assert "node_id" in serialized_content
    assert (
        serialized_content["metadata"]
        == '{"key1": "value1", "key2": "value2"}'
    )


def test_deserialize_metadata() -> None:
    # test when metadata is None
    node = KnowledgeNode(
        node_type="text",
        embedding=[0.1, 0.2],
        text_content="content",
    )
    assert node.metadata == {}

    # test when metadata is a dictionary
    node = KnowledgeNode(
        node_type="text",
        embedding=[0.1, 0.2],
        text_content="content",
        metadata={"key1": "value1", "key2": "value2"},
    )
    assert node.metadata == {"key1": "value1", "key2": "value2"}

    # test when metadata is a json string
    node = KnowledgeNode(
        node_type="text",
        embedding=[0.1, 0.2],
        text_content="content",
        metadata='{"key1": "value1", "key2": "value2"}',
    )
    assert node.metadata == {"key1": "value1", "key2": "value2"}


def test_deserialize_metadata_when_empty() -> None:
    node = KnowledgeNode(
        node_type="text",
        embedding=[0.1, 0.2],
        text_content="content",
    )
    serialized = node.model_dump()

    deserialized_node = KnowledgeNode.model_validate(serialized)

    assert node == deserialized_node
    assert serialized["metadata"] is None
