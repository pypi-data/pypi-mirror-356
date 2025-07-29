"""
Inworld SDK - A Python SDK for Inworld
"""

from typing import Literal, Optional

from .http_client import HttpClient
from .models import TTSAudioEncoding
from .models import TTSLanguageCodes
from .models import TTSModelIds
from .models import TTSVoices
from .tts import TTS

__all__ = ["InworldClient", "TTSAudioEncoding", "TTSLanguageCodes", "TTSModelIds", "TTSVoices"]


class InworldClient:
    """Client for interacting with Inworld's services."""

    def __init__(
        self,
        api_key: str,
        auth_type: Optional[Literal["basic", "bearer"]] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize the Inworld client.

        Args:
            api_key: Your Inworld API key
            auth_type: Optional authentication type, defaults to "basic"
            base_url: Optional custom base URL for the API, defaults to https://api.inworld.ai/
        """
        client = HttpClient(api_key, auth_type, base_url)
        self.__tts = TTS(client)

    @property
    def tts(self) -> TTS:
        return self.__tts
