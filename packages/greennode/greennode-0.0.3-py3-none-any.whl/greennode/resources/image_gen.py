from __future__ import annotations

from typing import List, Any

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    ImageGenRequest,
    ImageGenResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class ImageGen:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(
        self,
        *,
        prompt: str,
        n: int,
        size: str | None = None,
        width: int | None = None,
        height: int | None = None,
        response_format: str | None = None,
        model: str | None = None,
        **kwargs: Any,
    ) -> RerankResponse:
        """
        Method to generate completions based on a given prompt using a specified model.

        Args:
            prompt (str): The prompt to generate an image from.
            n (int): The number of images to generate.
            size (str): The size of the image to generate.
            width (int): The width of the image to generate.
            height (int): The height of the image to generate.
            response_format (str): The format of the image to generate.
            model (str): The name of the model to use for image generation.

        Returns:
            RerankResponse: Object containing reranked documents
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        assert size is not None or (width is not None and height is not None), "Either size or width and height must be provided"

        payload = ImageGenRequest(
            prompt=prompt,
            n=n,
            size=size,
            width=width,
            height=height,
            response_format=response_format,
            model=model,
            **kwargs,
        )

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="POST",
                url="images/generations",
                params=payload.model_dump(exclude_none=True),
            ),
            stream=False,
        )

        assert isinstance(response, GreenNodeResponse)

        return ImageGenResponse(**response.data)