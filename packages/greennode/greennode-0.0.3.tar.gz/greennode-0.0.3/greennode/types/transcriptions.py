from __future__ import annotations

from typing import List, Literal

from greennode.types.abstract import BaseModel
from greennode.types.common import (
    ObjectType,
)
from typing import Any


class Segment(BaseModel):
    start: float 
    end: float
    text: str


class TranscriptionsRequest(BaseModel):
    model: str
    file: Any
    response_format: str
    temperature: float
    language: str


class TranscriptionsChoicesData(BaseModel):
    """Represents a single speech to text response."""
    text: str
    relevance_score: float
    object: ObjectType | None = None  # Not present in response, set to None by default
    embedding: List[float] | None = None  # Not present in response, keep for compatibility


class TranscriptionsResponse(BaseModel):
    """Represents the full speech to text response."""
    text: str | None = None
    language: str | None = None
    duration: float | None = None
    segments: List[Segment] | None = None