from __future__ import annotations

import os
from typing import Dict

from greennode import resources
from greennode.constants import BASE_URL, MAX_RETRIES, TIMEOUT_SECS, AUTH_URL
from greennode.types import GreenNodeClient
from greennode.utils.tools import enforce_trailing_slash

from greennode.error import AuthenticationError


class GreenNodeAuthen:
    auth: resources.Authorization
    client: GreenNodeClient

    def __init__(
            self,
            *,
            client_id: str | None = None,
            client_secret: str | None = None,
            base_url: str | None = None,
            timeout: float | None = None,
            max_retries: int | None = None,
            supplied_headers: Dict[str, str] | None = None,
    ) -> None:

        if not client_id:
            # Raise errors
            raise AuthenticationError(
                "The client_id client option must be set either by passing client_id to the client or by setting the "
                "GREENNODE_CLIENT_ID environment variable"
            )
        if not client_secret:
            raise AuthenticationError(
                "The client_secret client option must be set either by passing api_key to the client or by setting the "
                "GREENNODE_SECRET environment variable"
            )

        if not base_url:
            base_url = os.environ.get("GREENNODE_AUTH_URL")

        if not base_url:
            base_url = AUTH_URL

        if timeout is None:
            timeout = TIMEOUT_SECS

        if max_retries is None:
            max_retries = MAX_RETRIES

        # GreenNodeClient object
        self.client = GreenNodeClient(
            api_key=f"{client_id}:{client_secret}",
            base_url=enforce_trailing_slash(base_url),
            timeout=timeout,
            max_retries=max_retries,
            supplied_headers=supplied_headers,
        )

        self.auth = resources.Authorization(self.client)



class GreenNode:
    chat: resources.Chat
    completions: resources.Completions
    embeddings: resources.Embeddings

    client: GreenNodeClient

    def __init__(
            self,
            *,
            api_key: str | None = None,
            base_url: str | None = None,
            timeout: float | None = None,
            max_retries: int | None = None,
            supplied_headers: Dict[str, str] | None = None,
    ) -> None:
        if not api_key:
            api_key = os.environ.get("GREENNODE_API_KEY")

        if not api_key:
            # Raise errors
            raise AuthenticationError(
                "The api_key client option must be set either by passing api_key to the client or by setting the "
                "GREENNODE_API_KEY environment variable"
            )

        # get base url
        if not base_url:
            base_url = os.environ.get("GREENNODE_BASE_URL")

        if not base_url:
            base_url = BASE_URL

        if timeout is None:
            timeout = TIMEOUT_SECS

        if max_retries is None:
            max_retries = MAX_RETRIES

        # GreenNodeClient object
        self.client = GreenNodeClient(
            api_key=api_key,
            base_url=enforce_trailing_slash(base_url),
            timeout=timeout,
            max_retries=max_retries,
            supplied_headers=supplied_headers,
        )
        self.chat = resources.Chat(self.client)
        self.completions = resources.Completions(self.client)
        self.embeddings = resources.Embeddings(self.client)
        self.models = resources.Models(self.client)
        self.reranks = resources.Reranks(self.client)
        self.image_gen = resources.ImageGen(self.client)
        self.speech = resources.Speech(self.client)
        self.transcriptions = resources.Transcriptions(self.client)