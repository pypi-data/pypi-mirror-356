import json
import base64
from typing import TYPE_CHECKING, Optional

from .._models import AudioOutput
from .._exceptions import APIError, NoAudioReceivedError

if TYPE_CHECKING:
    from .._client import OuteAI, AsyncOuteAI

class Generate:
    """Handles synchronous requests to the generate API endpoints."""
    def __init__(self, client: "OuteAI"):
        self._client = client

    def audio(
        self,
        *,
        model: str,
        text: str,
        speaker_type: str = "default",
        speaker_id: str,
        temperature: float = 0.4,
        verbose: bool = True
    ) -> AudioOutput:
        """
        Generates audio from text using a streaming connection.

        Args:
            model: The model to use for generation (e.g., "OuteTTS-1-Pro").
            text: The text to convert to speech.
            speaker_type: The type of speaker ('default' or 'custom').
            speaker_id: The ID of the speaker to use.
            temperature: The generation temperature (creativity).

        Returns:
            An AudioOutput object containing the generated audio bytes.
        """
        payload = {
            "model": model,
            "prompt": text,
            "speaker_type": speaker_type,
            "speaker_id": speaker_id,
            "temperature": temperature,
        }

        buffer = ""
        final_audio_data = None

        with self._client._client.stream(
            "POST",
            "/audio",
            params={"token": self._client.token},
            json=payload,
            timeout=120,
        ) as response:
            if response.status_code != 200:
                try:
                    error_body = response.read().decode()
                    raise APIError(response.status_code, error_body)
                except Exception:
                     raise APIError(response.status_code, response.reason_phrase)

            for chunk in response.iter_text():
                buffer += chunk
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)
                        if verbose:
                            print("Generated audio tokens:", data.get("audio_token_count", 0))
                        if "audio_data" in data and data["audio_data"].get("audio_bytes"):
                            final_audio_data = data["audio_data"]
                            break
                    except json.JSONDecodeError:
                        pass
                if final_audio_data:
                    break

        if not final_audio_data:
            raise NoAudioReceivedError("The stream ended without providing the final audio data.")

        return AudioOutput(
            audio_bytes=base64.b64decode(final_audio_data["audio_bytes"]),
            duration=final_audio_data.get("duration", 0.0),
            audio_token_count=data.get("audio_token_count", 0)
        )


class AsyncGenerate:
    """Handles asynchronous requests to the generate API endpoints."""
    def __init__(self, client: "AsyncOuteAI"):
        self._client = client

    async def audio(
        self,
        *,
        model: str,
        text: str,
        speaker_type: str = "default",
        speaker_id: str,
        temperature: float = 0.4,
        verbose: bool = True
    ) -> AudioOutput:
        """
        Generates audio from text using a streaming connection (asynchronously).

        Args:
            model: The model to use for generation (e.g., "OuteTTS-1-Pro").
            text: The text to convert to speech.
            speaker_type: The type of speaker ('default' or 'custom').
            speaker_id: The ID of the speaker to use.
            temperature: The generation temperature (creativity).

        Returns:
            An AudioOutput object containing the generated audio bytes.
        """
        payload = {
            "model": model,
            "prompt": text,
            "speaker_type": speaker_type,
            "speaker_id": speaker_id,
            "temperature": temperature,
        }

        buffer = ""
        final_audio_data = None

        async with self._client._client.stream(
            "POST",
            "/audio",
            params={"token": self._client.token},
            json=payload,
            timeout=120,
        ) as response:
            if response.status_code != 200:
                try:
                    error_body = await response.aread()
                    raise APIError(response.status_code, error_body.decode())
                except Exception:
                    raise APIError(response.status_code, response.reason_phrase)

            async for chunk in response.aiter_text():
                buffer += chunk
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if not line.strip():
                        continue

                    try:
                        data = json.loads(line)
                        if verbose:
                            print("Generated audio tokens:", data.get("audio_token_count", 0))
                        if "audio_data" in data and data["audio_data"].get("audio_bytes"):
                            final_audio_data = data["audio_data"]
                            break
                    except json.JSONDecodeError:
                        pass
                if final_audio_data:
                    break

        if not final_audio_data:
            raise NoAudioReceivedError("The stream ended without providing the final audio data.")

        return AudioOutput(
            audio_bytes=base64.b64decode(final_audio_data["audio_bytes"]),
            duration=final_audio_data.get("duration", 0.0),
            audio_token_count=data.get("audio_token_count", 0)
        )
