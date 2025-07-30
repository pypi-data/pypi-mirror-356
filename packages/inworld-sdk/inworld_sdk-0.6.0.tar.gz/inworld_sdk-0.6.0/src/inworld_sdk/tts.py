import json
from typing import Any, AsyncGenerator, cast, List, Optional, Union

from .http_wrapper import HTTPWrapper
from .models import AudioConfig
from .models import SynthesizeSpeechResponse
from .models import TTSLanguageCodes
from .models import TTSModelIds
from .models import TTSVoices
from .models import VoiceResponse


class TTS:
    """TTS API client"""

    def __init__(
        self,
        client: HTTPWrapper,
        audioConfig: Optional[AudioConfig] = None,
        languageCode: Optional[Union[TTSLanguageCodes, str]] = None,
        modelId: Optional[Union[TTSModelIds, str]] = None,
        voice: Optional[Union[TTSVoices, str]] = None,
    ):
        """Constructor for TTS class"""
        self.__audioConfig = audioConfig or None
        self.__client = client
        self.__languageCode = languageCode or "en-US"
        self.__modelId = modelId or None
        self.__voice = voice or "Emma"

    @property
    def audioConfig(self) -> Optional[AudioConfig]:
        """Get default audio config"""
        return self.__audioConfig

    @audioConfig.setter
    def audioConfig(self, audioConfig: AudioConfig):
        """Set default audio config"""
        self.__audioConfig = audioConfig

    @property
    def languageCode(self) -> Union[TTSLanguageCodes, str]:
        """Get default language code"""
        return self.__languageCode

    @languageCode.setter
    def languageCode(self, languageCode: Union[TTSLanguageCodes, str]):
        """Set default language code"""
        self.__languageCode = languageCode

    @property
    def modelId(self) -> Optional[Union[TTSModelIds, str]]:
        """Get default model ID"""
        return self.__modelId

    @modelId.setter
    def modelId(self, modelId: Union[TTSModelIds, str]):
        """Set default model ID"""
        self.__modelId = modelId

    @property
    def voice(self) -> Union[TTSVoices, str]:
        """Get default voice"""
        return self.__voice

    @voice.setter
    def voice(self, voice: Union[TTSVoices, str]):
        """Set default voice"""
        self.__voice = voice

    async def synthesizeSpeech(
        self,
        input: str,
        voice: Optional[Union[TTSVoices, str]] = None,
        languageCode: Optional[Union[TTSLanguageCodes, str]] = None,
        modelId: Optional[Union[TTSModelIds, str]] = None,
        audioConfig: Optional[AudioConfig] = None,
    ) -> SynthesizeSpeechResponse:
        """Synthesize speech"""
        data: dict[str, Any] = {
            "input": {"text": input},
            "voice": {
                "name": voice or self.__voice,
                "languageCode": languageCode or self.__languageCode,
            },
        }

        if audioConfig or self.__audioConfig:
            data["audioConfig"] = audioConfig or self.__audioConfig

        if modelId or self.__modelId:
            data["modelId"] = modelId or self.__modelId

        response = await self.__client.request(
            "post",
            "/tts/v1alpha/text:synthesize-sync",
            data=data,
        )
        return cast(SynthesizeSpeechResponse, response)

    async def synthesizeSpeechStream(
        self,
        input: str,
        voice: Optional[Union[TTSVoices, str]] = None,
        languageCode: Optional[Union[TTSLanguageCodes, str]] = None,
        modelId: Optional[Union[TTSModelIds, str]] = None,
        audioConfig: Optional[AudioConfig] = None,
    ) -> AsyncGenerator[SynthesizeSpeechResponse, None]:
        """Synthesize speech as a stream"""
        data: dict[str, Any] = {
            "input": {"text": input},
            "voice": {
                "name": voice or self.__voice,
                "languageCode": languageCode or self.__languageCode,
            },
        }

        if audioConfig or self.__audioConfig:
            data["audioConfig"] = audioConfig or self.__audioConfig

        if modelId or self.__modelId:
            data["modelId"] = modelId or self.__modelId

        async with self.__client.stream(
            "post",
            "/tts/v1alpha/text:synthesize",
            data=data,
        ) as response:
            async for chunk in response.aiter_lines():
                if chunk:
                    chunk_data = json.loads(chunk)
                    if isinstance(chunk_data, dict) and chunk_data.get("result"):
                        yield cast(SynthesizeSpeechResponse, chunk_data["result"])

    async def voices(
        self,
        languageCode: Optional[Union[TTSLanguageCodes, str]] = None,
        modelId: Optional[Union[TTSModelIds, str]] = None,
    ) -> List[VoiceResponse]:
        """Get voices"""
        data: dict[str, Any] = {}
        if languageCode:
            data["languageCode"] = languageCode
        if modelId:
            data["modelId"] = modelId

        response = await self.__client.request("get", "/tts/v1alpha/voices", data=data)
        voices = response.get("voices", [])
        return cast(List[VoiceResponse], voices)
