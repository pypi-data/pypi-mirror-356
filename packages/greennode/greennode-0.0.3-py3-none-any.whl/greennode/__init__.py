from __future__ import annotations

from contextvars import ContextVar
from typing import Callable, TYPE_CHECKING

from greennode import (
    utils,
    error,
    constants
)

from greennode.version import VERSION

from greennode.client import GreenNode, GreenNodeAuthen

version = VERSION

log: str | None = None  # Set to either 'debug' or 'info', controls console logging

if TYPE_CHECKING:
    import requests
    from aiohttp import ClientSession

requestssession: "requests.Session" | Callable[[], "requests.Session"] | None = None

aiosession: ContextVar["ClientSession" | None] = ContextVar(
    "aiohttp-session", default=None
)

__all__ = [
    "aiosession",
    "constants",
    "utils",
    "GreenNode",
    "GreenNodeAuthen",
    "error",
    "version"
]