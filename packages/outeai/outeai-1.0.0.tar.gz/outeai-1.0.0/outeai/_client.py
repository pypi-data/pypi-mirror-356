import os
import httpx
from typing import Optional

from ._exceptions import AuthenticationError
from ._api.generate import Generate, AsyncGenerate

class _BaseClient:
    """Base client for handling authentication and client setup."""
    def __init__(self, *, token: Optional[str] = None, base_url: Optional[str] = None):
        if token is None:
            token = os.environ.get("OUTEAI_API_TOKEN")
        if not token:
            raise AuthenticationError(
                "No API token provided. Set the OUTEAI_API_TOKEN environment variable "
                "or pass the token argument to the client."
            )
        self.token = token

        if base_url is None:
            base_url = "https://outeai.com/api/v1"

        self.base_url = base_url


class OuteAI(_BaseClient):
    """
    The synchronous client for interacting with the OuteAI API.

    Example:
        from outeai import OuteAI

        # Reads token from OUTEAI_API_TOKEN environment variable
        client = OuteAI()

        # Or initialize with a token
        client = OuteAI(token="your_token_here")
    """
    def __init__(self, *, token: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(token=token, base_url=base_url)
        self._client = httpx.Client(base_url=self.base_url)
        self.generate = Generate(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes the underlying HTTPX client."""
        self._client.close()


class AsyncOuteAI(_BaseClient):
    """
    The asynchronous client for interacting with the OuteAI API.

    Example:
        import asyncio
        from outeai import AsyncOuteAI

        client = AsyncOuteAI() # Reads token from environment variable

        async def main():
            output = await client.generate.audio(...)
            output.save("output.mp3")
            await client.close()

        asyncio.run(main())
    """
    def __init__(self, *, token: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(token=token, base_url=base_url)
        self._client = httpx.AsyncClient(base_url=self.base_url)
        self.generate = AsyncGenerate(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Closes the underlying HTTPX client."""
        await self._client.aclose()
