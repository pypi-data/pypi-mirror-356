"""
fed_rag.types

Only components defined in `__all__` are considered stable and public.
"""

from .bridge import BridgeMetadata
from .knowledge_node import KnowledgeNode, NodeContent, NodeType
from .rag import RAGConfig, RAGResponse, SourceNode
from .results import TestResult, TrainResult

__all__ = [
    # bridge
    "BridgeMetadata",
    # results
    "TrainResult",
    "TestResult",
    # knowledge node
    "KnowledgeNode",
    "NodeType",
    "NodeContent",
    # rag
    "RAGConfig",
    "RAGResponse",
    "SourceNode",
]

__deprecated__ = True
