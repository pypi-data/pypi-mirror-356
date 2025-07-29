from __future__ import annotations

from typing import List, Any

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    EmbeddingRequest,
    EmbeddingResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class Embeddings:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(
        self,
        *,
        input: str | List[str],
        model: str,
        **kwargs: Any,
    ) -> EmbeddingResponse:
        """
        Method to generate completions based on a given prompt using a specified model.

        Args:
            input (str | List[str]): A string or list of strings to embed
            model (str): The name of the model to query.

        Returns:
            EmbeddingResponse: Object containing embeddings
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        payload = EmbeddingRequest(
            input=input,
            model=model,
            **kwargs,
        )

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="POST",
                url="embeddings",
                params=payload.model_dump(exclude_none=True),
            ),
            stream=False,
        )

        assert isinstance(response, GreenNodeResponse)

        return EmbeddingResponse(**response.data)
