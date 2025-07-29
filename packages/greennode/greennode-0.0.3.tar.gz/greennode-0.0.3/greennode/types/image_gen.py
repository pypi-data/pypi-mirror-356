from __future__ import annotations

from typing import List, Literal

from greennode.types.abstract import BaseModel
from greennode.types.common import (
    ObjectType,
)


class ImageGenRequest(BaseModel):
    prompt: str
    n: int
    size: str | None = None
    width: int | None = None
    height: int | None = None
    response_format: str | None = None
    model: str | None = None


class ImageGenChoicesData(BaseModel):
    """Represents a single generated image."""
    b64_json: str
    url: str | None = None


class ImageGenResponse(BaseModel):
    """Represents the full image generation response."""
    created: int
    usage: dict | None = None  # expects {"total_tokens": int, ...}
    object: str | None = "list"  # Not present in response, set to 'list' by default
    data: List[ImageGenChoicesData] | None = None