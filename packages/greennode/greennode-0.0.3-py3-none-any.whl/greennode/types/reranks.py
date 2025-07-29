from __future__ import annotations

from typing import List, Literal

from greennode.types.abstract import BaseModel
from greennode.types.common import (
    ObjectType,
)


class RerankRequest(BaseModel):
    # input or list of inputs
    query: str
    documents: List[str]
    # model to query
    model: str


class RerankChoicesData(BaseModel):
    """Represents a single reranked document and its score."""
    index: int
    document: dict  # expects {"text": str}
    relevance_score: float
    object: ObjectType | None = None  # Not present in response, set to None by default
    embedding: List[float] | None = None  # Not present in response, keep for compatibility


class RerankResponse(BaseModel):
    """Represents the full rerank response."""
    id: str | None = None
    model: str | None = None
    usage: dict | None = None  # expects {"total_tokens": int, ...}
    object: str | None = "list"  # Not present in response, set to 'list' by default
    data: List[RerankChoicesData] | None = None