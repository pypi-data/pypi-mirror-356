from __future__ import annotations

from greennode.types.abstract import BaseModel


class AuthorizationHeaders(BaseModel):
    authorization: str | None = None
    content_type: str | None = None

    def to_dict(self):
        return {
            "Authorization": self.authorization,
            "Content-Type": self.content_type
        }


class AuthorizationRequest(BaseModel):
    grant_type: str | None = None


class AuthorizationResponse(BaseModel):
    token_type: str | None = None
    access_token: str | None = None
    expires_in: int | None = None
    refresh_expires_in: int | None = None
