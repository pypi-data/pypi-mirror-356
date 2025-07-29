# OuteAI Python SDK

The official Python SDK for the [OuteAI API](https://outeai.com).

## Installation

```bash
pip install outeai
```

## Authentication

The SDK requires an API token for authentication. We recommend setting it as an environment variable for security and convenience.

```bash
export OUTEAI_API_TOKEN='your_access_token_here'
```

Alternatively, you can pass the token directly when initializing the client.

## Quickstart: Synchronous Usage

Here's how to generate audio using the standard synchronous client.

```python
from outeai import OuteAI, APIError

try:
    # It is recommended to set the token as an environment variable
    # Reads from OUTEAI_API_TOKEN automatically
    client = OuteAI()

    # Or initialize the client with the token directly
    # client = OuteAI(token="your_access_token_here")

    print("Generating audio...")
    output = client.generate.audio(
        model="OuteTTS-1-Pro",
        text="Hello, world! This is a test of the text to speech API.",
        speaker_id="EN-FEMALE-1-NEUTRAL",
        temperature=0.4
    )

    # The output object contains the audio data and can be saved directly
    output.save("generated_audio.mp3")

    print(f"Audio generation complete. Duration: {output.duration:.2f}s")

except APIError as e:
    print(f"An API error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # It's good practice to close the client
    if 'client' in locals():
        client.close()

```

## Asynchronous Usage

For applications using `asyncio`, the `AsyncOuteAI` client provides non-blocking I/O.

```python
import asyncio
from outeai import AsyncOuteAI, APIError

async def main():
    # Using the client as an async context manager handles setup and teardown
    async with AsyncOuteAI() as client:
        try:
            print("Generating audio asynchronously...")
            output = await client.generate.audio(
                model="OuteTTS-1-Pro",
                text="This is an asynchronous test of the API.",
                speaker_id="EN-FEMALE-1-NEUTRAL",
                temperature=0.5
            )

            output.save("generated_audio_async.mp3")
            print(f"Async audio generation complete. Duration: {output.duration:.2f}s")

        except APIError as e:
            print(f"An API error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```
