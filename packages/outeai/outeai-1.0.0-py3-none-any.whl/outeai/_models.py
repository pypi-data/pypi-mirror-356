import base64
from dataclasses import dataclass
from loguru import logger

@dataclass
class AudioOutput:
    """
    Class for handling the audio output from the TTS API.
    Contains the raw audio bytes and a convenience method to save the audio to a file.
    """
    audio_bytes: bytes
    duration: float
    audio_token_count: int

    def save(self, path: str) -> None:
        """
        Saves the audio to the specified path.
        If the path does not end with '.mp3', it will be appended.

        Args:
            path (str): The file path where the audio will be saved.
        """
        if not path.lower().endswith(".mp3"):
            path += ".mp3"
        try:
            with open(path, "wb") as audio_file:
                audio_file.write(self.audio_bytes)
            logger.success(f"Audio file saved to: {path}")
        except IOError as e:
            logger.error(f"Failed to save audio file to {path}: {e}")
            raise

    @property
    def audio_base64(self) -> str:
        """Returns the audio data as a base64 encoded string."""
        return base64.b64encode(self.audio_bytes).decode("utf-8")
