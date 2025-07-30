from typing import Literal, Optional
from urllib.parse import urljoin

import httpx


class HTTPWrapper:
    """HTTP wrapper client"""

    def __init__(
        self,
        api_key: str,
        auth_type: Optional[Literal["basic", "bearer"]] = None,
        base_url: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        """Constructor for HTTP wrapper client

        Args:
            api_key: The API key to use for authentication
            auth_type: Authentication type, either "basic" or "bearer". Defaults to "basic"
            base_url: Optional base URL for the API, defaults to https://api.inworld.ai/v1
            http_client: Optional httpx.AsyncClient to use for the API requests
        """
        self.__http_client = http_client or httpx.AsyncClient()
        auth_type = auth_type or "basic"
        self.__base_url = base_url or "https://api.inworld.ai/v1"

        if auth_type.lower() not in ["basic", "bearer"]:
            raise ValueError("auth_type must be either 'basic' or 'bearer'")

        auth_prefix = "Basic" if auth_type.lower() == "basic" else "Bearer"
        self.__headers = {
            "Content-Type": "application/json",
            "Authorization": f"{auth_prefix} {api_key}",
        }

    async def request(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
    ) -> dict:
        requestUrl = urljoin(self.__base_url, path)
        json_data = data if method.lower() != "get" else None
        params_data = data if method.lower() == "get" else None

        response = await self.__http_client.request(
            method,
            url=requestUrl,
            params=params_data,
            json=json_data,
            headers=self.__headers,
        )

        result = response.json()
        await response.aclose()
        return result

    def stream(
        self,
        method: str,
        path: str,
        data: Optional[dict] = None,
    ):
        requestUrl = urljoin(self.__base_url, path)
        json_data = data if method.lower() != "get" else None
        params_data = data if method.lower() == "get" else None

        return self.__http_client.stream(
            method,
            url=requestUrl,
            params=params_data,
            json=json_data,
            headers=self.__headers,
        )

    async def close(self):
        await self.__http_client.aclose()
