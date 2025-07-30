"""
Inworld SDK - A Python SDK for Inworld
"""

from typing import Literal, Optional

import httpx

from .http_wrapper import HTTPWrapper
from .models import __all__ as models_all
from .tts import TTS

__all__ = ["InworldClient"] + models_all


class InworldClient:
    """Client for interacting with Inworld's services."""

    def __init__(
        self,
        api_key: str,
        auth_type: Optional[Literal["basic", "bearer"]] = None,
        base_url: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        """
        Initialize the Inworld client.

        Args:
            api_key: Your Inworld API key
            auth_type: Optional authentication type, defaults to "basic"
            base_url: Optional custom base URL for the API, defaults to https://api.inworld.ai/
            http_client: Optional httpx.AsyncClient to use for the API requests
        """
        client = HTTPWrapper(api_key, auth_type, base_url, http_client)
        self.__tts = TTS(client)

    @property
    def tts(self) -> TTS:
        return self.__tts
