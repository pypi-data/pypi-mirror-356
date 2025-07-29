from __future__ import annotations

import json
from typing import Any, Dict

from requests import RequestException

from greennode.types.error import GreenNodeErrorResponse


class GreenNodeException(Exception):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        headers: str | Dict[Any, Any] | None = None,
        request_id: str | None = None,
        http_status: int | None = None,
    ) -> None:
        _message = (
            json.dumps(message.model_dump(exclude_none=True))
            if isinstance(message, GreenNodeErrorResponse)
            else message
        )
        if http_status is not None:
            self._message = f"Error code: {http_status} - {_message}"
        else:
            self._message = str(_message)

        super().__init__(self._message)

        self.http_status = http_status
        self.headers = headers or {}
        self.request_id = request_id

    def __repr__(self) -> str:
        repr_message = json.dumps(
            {
                "response": self._message,
                "status": self.http_status,
                "request_id": self.request_id,
                "headers": self.headers,
            }
        )
        return "%s(%r)" % (self.__class__.__name__, repr_message)


class AuthenticationError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class ResponseError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class JSONError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class InstanceError(GreenNodeException):
    def __init__(self, model: str | None = "model", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.message = f"""No running instances for {model}.
                You can start an instance with one of the following methods:
                  1. navigating to the GreenNode Playground at aiplatform.console.greennode.ai
                """


class RateLimitError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class FileTypeError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class AttributeError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class Timeout(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class APIConnectionError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class InvalidRequestError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class APIError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class ServiceUnavailableError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)


class DownloadError(GreenNodeException):
    def __init__(
        self,
        message: (
            GreenNodeErrorResponse | Exception | str | RequestException | None
        ) = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message=message, **kwargs)