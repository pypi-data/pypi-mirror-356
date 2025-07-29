"""Qdrant Knowledge Store"""

import warnings
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Generator, Literal, Optional

from pydantic import Field, PrivateAttr, SecretStr, model_validator

from fed_rag.base.knowledge_store import BaseKnowledgeStore
from fed_rag.data_structures.knowledge_node import KnowledgeNode
from fed_rag.exceptions import (
    InvalidDistanceError,
    KnowledgeStoreError,
    KnowledgeStoreNotFoundError,
    KnowledgeStoreWarning,
    LoadNodeError,
)

from .utils import (
    check_qdrant_installed,
    convert_knowledge_node_to_qdrant_point,
    convert_scored_point_to_knowledge_node_and_score_tuple,
)

if TYPE_CHECKING:  # pragma: no cover
    from qdrant_client import QdrantClient


def _get_qdrant_client(
    host: str,
    port: int,
    grpc_port: int,
    https: bool = False,
    timeout: int | None = None,
    api_key: str | None = None,
    in_memory: bool = False,
    **kwargs: Any,
) -> "QdrantClient":
    """Get a QdrantClient

    NOTE: should be used within `QdrantKnowledgeStore` post validation that the
    qdrant extra has been installed.
    """
    from qdrant_client import QdrantClient

    if in_memory:
        return QdrantClient(":memory:")
    else:
        return QdrantClient(
            host=host,
            port=port,
            grpc_port=grpc_port,
            api_key=api_key,
            timeout=timeout,
            https=https,
            **kwargs,
        )


class QdrantKnowledgeStore(BaseKnowledgeStore):
    """Qdrant Knowledge Store Class

    NOTE: This is a minimal implementation in order to just get started using Qdrant.
    """

    host: str = Field(default="localhost")
    port: int = Field(default=6333)
    grpc_port: int = Field(default=6334)
    https: bool = Field(default=False)
    api_key: SecretStr | None = Field(default=None)
    collection_name: str = Field(description="Name of Qdrant collection")
    collection_distance: Literal[
        "Cosine", "Euclid", "Dot", "Manhattan"
    ] = Field(
        description="Distance definition for collection", default="Cosine"
    )
    client_kwargs: dict[str, Any] = Field(default_factory=dict)
    timeout: int | None = Field(default=None)
    in_memory: bool = Field(
        default=False,
        description="Specifies whether the client should refer to an in-memory service.",
    )
    load_nodes_kwargs: dict[str, Any] = Field(default_factory=dict)
    _in_memory_client: Optional["QdrantClient"] = PrivateAttr(default=None)

    @contextmanager
    def get_client(
        self,
    ) -> Generator["QdrantClient", None, None]:
        if self.in_memory:
            if self._in_memory_client is None:
                self._in_memory_client = _get_qdrant_client(
                    in_memory=self.in_memory,
                    host=self.host,
                    port=self.port,
                    grpc_port=self.grpc_port,
                    https=self.https,
                    timeout=self.timeout,
                    api_key=self.api_key.get_secret_value()
                    if self.api_key
                    else None,
                    **self.client_kwargs,
                )

            yield self._in_memory_client  # yield persistent in-memory client
        else:
            # create a new client connection and yield this
            client = _get_qdrant_client(
                host=self.host,
                port=self.port,
                grpc_port=self.grpc_port,
                https=self.https,
                timeout=self.timeout,
                api_key=self.api_key.get_secret_value()
                if self.api_key
                else None,
                **self.client_kwargs,
            )

            try:
                yield client
            finally:
                try:
                    client.close()
                except Exception as e:
                    warnings.warn(
                        f"Unable to close client: {str(e)}",
                        KnowledgeStoreWarning,
                    )

    def _collection_exists(self) -> bool:
        """Check if a collection exists."""
        with self.get_client() as client:
            return client.collection_exists(self.collection_name)  # type: ignore[no-any-return]

    def _create_collection(
        self, collection_name: str, vector_size: int, distance: str
    ) -> None:
        from qdrant_client.models import Distance, VectorParams

        try:
            # Try to convert to enum
            distance = Distance(distance)
        except ValueError:
            # Catch the ValueError from enum conversion and raise your custom error
            raise InvalidDistanceError(
                f"Unsupported distance: {distance}. "
                f"Mode must be one of: {', '.join([m.value for m in Distance])}"
            )

        with self.get_client() as client:
            try:
                client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size, distance=distance
                    ),
                )
            except Exception as e:
                raise KnowledgeStoreError(
                    f"Failed to create collection: {str(e)}"
                ) from e

    def _ensure_collection_exists(self) -> None:
        if not self._collection_exists():
            raise KnowledgeStoreNotFoundError(
                f"Collection '{self.collection_name}' does not exist."
            )

    def _check_if_collection_exists_otherwise_create_one(
        self, vector_size: int
    ) -> None:
        if not self._collection_exists():
            try:
                self._create_collection(
                    collection_name=self.collection_name,
                    vector_size=vector_size,
                    distance=self.collection_distance,
                )
            except Exception as e:
                raise KnowledgeStoreError(
                    f"Failed to create new collection: '{self.collection_name}'"
                ) from e

    @model_validator(mode="before")
    @classmethod
    def check_dependencies(cls, data: Any) -> Any:
        """Validate that qdrant dependencies are installed."""
        check_qdrant_installed()
        return data

    def load_node(self, node: KnowledgeNode) -> None:
        self._check_if_collection_exists_otherwise_create_one(
            vector_size=len(node.embedding)
        )

        point = convert_knowledge_node_to_qdrant_point(node)
        with self.get_client() as client:
            try:
                client.upsert(
                    collection_name=self.collection_name, points=[point]
                )
            except Exception as e:
                raise LoadNodeError(
                    f"Failed to load node {node.node_id} into collection '{self.collection_name}': {str(e)}"
                ) from e

    def load_nodes(self, nodes: list[KnowledgeNode]) -> None:
        if not nodes:
            return

        self._check_if_collection_exists_otherwise_create_one(
            vector_size=len(nodes[0].embedding)
        )

        points = [convert_knowledge_node_to_qdrant_point(n) for n in nodes]
        with self.get_client() as client:
            try:
                client.upload_points(
                    collection_name=self.collection_name,
                    points=points,
                    **self.load_nodes_kwargs,
                )
            except Exception as e:
                raise LoadNodeError(
                    f"Loading nodes into collection '{self.collection_name}' failed: {str(e)}"
                ) from e

    def retrieve(
        self, query_emb: list[float], top_k: int
    ) -> list[tuple[float, KnowledgeNode]]:
        """Retrieve top-k nodes from the vector store."""
        from qdrant_client.conversions.common_types import QueryResponse

        self._ensure_collection_exists()

        with self.get_client() as client:
            try:
                hits: QueryResponse = client.query_points(
                    collection_name=self.collection_name,
                    query=query_emb,
                    limit=top_k,
                )
            except Exception as e:
                raise KnowledgeStoreError(
                    f"Failed to retrieve from collection '{self.collection_name}': {str(e)}"
                ) from e

        return [
            convert_scored_point_to_knowledge_node_and_score_tuple(pt)
            for pt in hits.points
        ]

    def batch_retrieve(
        self, query_embs: list[list[float]], top_k: int
    ) -> list[list[tuple[float, "KnowledgeNode"]]]:
        """Batch retrieve top-k nodes from the vector store."""
        from qdrant_client.conversions.common_types import QueryResponse
        from qdrant_client.http.models import QueryRequest

        self._ensure_collection_exists()

        with self.get_client() as client:
            try:
                batch_hits: list[QueryResponse] = client.query_batch_points(
                    collection_name=self.collection_name,
                    requests=[
                        QueryRequest(query=emb, limit=top_k, with_payload=True)
                        for emb in query_embs
                    ],
                )
            except Exception as e:
                raise KnowledgeStoreError(
                    f"Failed to batch retrieve from collection '{self.collection_name}': {str(e)}"
                ) from e

        return [
            [
                convert_scored_point_to_knowledge_node_and_score_tuple(pt)
                for pt in hits.points
            ]
            for hits in batch_hits
        ]

    def delete_node(self, node_id: str) -> bool:
        """Delete a node based on its node_id."""
        from qdrant_client.http.models import (
            FieldCondition,
            Filter,
            MatchValue,
            UpdateResult,
            UpdateStatus,
        )

        self._ensure_collection_exists()

        with self.get_client() as client:
            try:
                res: UpdateResult = client.delete(
                    collection_name=self.collection_name,
                    points_selector=Filter(
                        must=[
                            FieldCondition(
                                key="node_id", match=MatchValue(value=node_id)
                            )
                        ]
                    ),
                )
            except Exception:
                raise KnowledgeStoreError(
                    f"Failed to delete node: '{node_id}' from collection '{self.collection_name}'"
                )

        return bool(res.status == UpdateStatus.COMPLETED)

    def clear(self) -> None:
        self._ensure_collection_exists()

        # delete the collection
        with self.get_client() as client:
            try:
                client.delete_collection(collection_name=self.collection_name)
            except Exception as e:
                raise KnowledgeStoreError(
                    f"Failed to delete collection '{self.collection_name}': {str(e)}"
                ) from e

    @property
    def count(self) -> int:
        from qdrant_client.http.models import CountResult

        self._ensure_collection_exists()

        with self.get_client() as client:
            try:
                res: CountResult = client.count(
                    collection_name=self.collection_name
                )
                return int(res.count)
            except Exception as e:
                raise KnowledgeStoreError(
                    f"Failed to get vector count for collection '{self.collection_name}': {str(e)}"
                ) from e

    def persist(self) -> None:
        """Persist a knowledge store to disk."""
        raise NotImplementedError(
            "`persist()` is not available in QdrantKnowledgeStore."
        )

    def load(self) -> None:
        """Load a previously persisted knowledge store."""
        raise NotImplementedError(
            "`load()` is not available in QdrantKnowledgeStore. "
            "Data is automatically persisted and loaded from the Qdrant server."
        )
