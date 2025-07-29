from __future__ import annotations

from typing import List, Any

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    RerankRequest,
    RerankResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class Reranks:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(
        self,
        *,
        query: str,
        documents: List[str],
        model: str,
        **kwargs: Any,
    ) -> RerankResponse:
        """
        Method to generate completions based on a given prompt using a specified model.

        Args:
            query (str): The query to rerank
            documents (List[str]): A list of documents to rerank
            model (str): The name of the model to query.

        Returns:
            RerankResponse: Object containing reranked documents
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        payload = RerankRequest(
            query=query,
            documents=documents,
            model=model,
            **kwargs,
        )

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="POST",
                url="rerank",
                params=payload.model_dump(exclude_none=True),
            ),
            stream=False,
        )

        assert isinstance(response, GreenNodeResponse)

        return RerankResponse(**response.data)