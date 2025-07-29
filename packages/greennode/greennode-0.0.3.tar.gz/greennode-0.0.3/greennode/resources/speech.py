from __future__ import annotations

from typing import List, Any

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    SpeechRequest,
    SpeechResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class Speech:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(
        self,
        *,
        model: str,
        voice: str | int,
        input: str,
        **kwargs: Any,
    ) -> SpeechResponse:
        """
        Method to generate completions based on a given prompt using a specified model.

        Args:
            model (str): The name of the model to use for text to speech.
            voice (str | int): The voice to use for text to speech.
            input (str): The input to generate text to speech from.

        Returns:
            RerankResponse: Object containing reranked documents
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        payload = SpeechRequest(
            model=model,
            voice=voice,
            input=input,
            **kwargs,
        )

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="POST",
                url="audio/speech",
                params=payload.model_dump(exclude_none=True),
            ),
            stream=False,
        )
        assert isinstance(response, GreenNodeResponse)
        #response is binary audio data
        return SpeechResponse.from_binary_response(response.data)