class OuteAIError(Exception):
    """Base exception for the OuteAI SDK."""
    pass

class AuthenticationError(OuteAIError):
    """Raised when authentication fails."""
    pass

class APIError(OuteAIError):
    """Raised when the API returns a non-2xx status code."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = f"API Error {status_code}: {message}"
        super().__init__(self.message)

class NoAudioReceivedError(OuteAIError):
    """Raised when the stream completes without sending any audio data."""
    pass
