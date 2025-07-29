from __future__ import annotations

from typing import List

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    ModelObject,
    ListModelResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class Models:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def list(
        self,
    ) -> List[ModelObject]:
        """
        Method to return list of models on the API

        Returns:
            List[ModelObject]: List of model objects
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="GET",
                url="models",
            ),
            stream=False,
        )

        assert isinstance(response, GreenNodeResponse)

        return ListModelResponse(**response.data)
