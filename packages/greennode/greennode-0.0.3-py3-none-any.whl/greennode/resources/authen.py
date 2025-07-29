from __future__ import annotations

from greennode.abstract import api_requestor
from greennode.greennode_response import GreenNodeResponse
from greennode.types import (
    GreenNodeClient,
    GreenNodeRequest,
    AuthorizationHeaders,
    AuthorizationRequest,
    AuthorizationResponse
)
from greennode.utils import string_to_base64


def createAuthorizationHeaders(client: GreenNodeClient):
    auth_token = string_to_base64(client.api_key)
    headers = AuthorizationHeaders(
        authorization=f"Basic {auth_token}",
        content_type="application/x-www-form-urlencoded"
    )
    return headers.to_dict()


class Authorization:
    def __init__(self, client: GreenNodeClient) -> None:
        self._client = client

    def create(self):
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )
        headers = createAuthorizationHeaders(self._client)
        payload = AuthorizationRequest(grant_type="client_credentials")

        response, _, _ = requestor.request(
            options=GreenNodeRequest(
                method="POST",
                headers=headers,
                url="/auth/token",
                params=payload.model_dump(exclude_none=True),
                override_headers=True
            ),
            stream=False,
        )

        assert isinstance(response, GreenNodeResponse)

        return AuthorizationResponse(**response.data)
