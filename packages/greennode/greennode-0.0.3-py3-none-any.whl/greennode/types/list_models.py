from __future__ import annotations

from enum import Enum
from typing import Literal, List

from greennode.types.abstract import BaseModel
from greennode.types.common import ObjectType


class ModelType(str, Enum):
    CHAT = "chat"
    LANGUAGE = "language"
    CODE = "code"
    IMAGE = "image"
    EMBEDDING = "embedding"
    MODERATION = "moderation"
    RERANK = "rerank"
    AUDIO = "audio"


class PricingObject(BaseModel):
    input: float | None = None
    output: float | None = None
    hourly: float | None = None
    base: float | None = None
    finetune: float | None = None


class ModelObject(BaseModel):
    # model id
    id: str
    # object type
    object: Literal[ObjectType.Model]
    created: int | None = None
    root: str | None = None
    parent: str | None = None
    max_model_len: int | None = None

class ListModelResponse(BaseModel):
    # object type
    object: Literal["list"] | None = None
    # list of models
    data: List[ModelObject] | None = None