from __future__ import annotations

from typing import List, Any

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    TranscriptionsRequest,
    TranscriptionsResponse,
    GreenNodeClient,
    GreenNodeRequest,
)


class Transcriptions:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(
        self,
        *,
        model: str,
        file_: str,
        response_format: str,
        temperature: float,
        language: str,
        **kwargs: Any,
    ) -> TranscriptionsResponse:
        """
        Method to convert speech to text using a specified model.

        Args:
            model (str): The name of the model to use for speech to text.
            file_ (str): The file_ to convert to text.
            response_format (str): The format of the response.
            temperature (float): The temperature of the response.
            language (str): The language of the response.

        Returns:
            TranscriptionsResponse: Object containing speech to text response
        """

        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        # Prepare multipart/form-data
        params = {
            "model": model,
            "response_format": response_format,
            "temperature": str(temperature),
            "language": language,
        }
        params.update(kwargs)
        files = {"file": open(file_, "rb")}

        try:
            response, _, _ = requestor.request(
                options=GreenNodeRequest(
                    method="POST",
                    url="audio/transcriptions",
                    params=params,
                    files=files,
                ),
                stream=False,
            )
        finally:
            files["file"].close()
        assert isinstance(response, GreenNodeResponse)
        return TranscriptionsResponse(**response.data)