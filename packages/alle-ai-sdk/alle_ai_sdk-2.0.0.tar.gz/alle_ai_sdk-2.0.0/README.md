# AlleAI Python SDK

[![PyPI version](https://badge.fury.io/py/alle-ai-sdk.svg)](https://badge.fury.io/py/alle-ai-sdk)
[![Python Version](https://img.shields.io/pypi/pyversions/alle-ai-sdk)](https://pypi.org/project/alle-ai-sdk/)
[![License](https://img.shields.io/github/license/Alle-AI/alle-ai-python)](https://github.com/Alle-AI/alle-ai-python/blob/main/LICENSE)

A Python SDK for interacting with the AlleAI platform, providing seamless access to state-of-the-art AI models for image generation, audio processing, and video creation.

## Features

- **Chat Completions API** – Generate conversational responses using multiple AI models such as GPT-4o, O4-Mini, and Claude 3 Sonnet.
- **Image Generation & Editing API** – Create and manipulate high-quality images using various AI models like Grok-2 and DALL·E 3.
- **Audio API** – Multi-model support for:
  - **Text-to-Speech (TTS):** Convert text into natural-sounding audio.
  - **Speech-to-Text (STT):** Transcribe spoken audio into text.
  - **Audio Generation:** Create unique audio content using generative AI.
- **Video Generation API** – Generate AI-powered videos with customizable parameters, backed by multiple AI models.

## Installation

Install the package using pip:

```bash
pip install alle-ai-sdk
```

## Quick Start

### Environment Setup

Create a `.env` file in your project root:

```env
ALLEAI_API_KEY=your_api_key_here
```

### Initialize Client

```python
from alleai.core import AlleAIClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ALLEAI_API_KEY")

# Initialize client
client = AlleAIClient(api_key=api_key)
```

## Usage Examples

### Chat Completions

```python
# Chat completion example
chat = client.chat.completions({
    "models": ["gpt-4o", "o4-mini", "claude-3-sonnet"],
    "messages": [
        {
            "system": [
                {
                    "type": "text",
                    "text": "You are a helpful assistant."
                }
            ]
        },
        {
            "user": [
                {
                    "type": "text",
                    "text": "tell me about photosynthesis?"
                }
            ]
        }
    ],
    "temperature": 0.7,      # Controls randomness (0.0 to 1.0)
    "max_tokens": 2000,      # Maximum response length
    "top_p": 1,              # Controls diversity
    "frequency_penalty": 0.2, # Penalizes repeated tokens
    "presence_penalty": 0.3,  # Penalizes new tokens
    "stream": False          # Enable streaming responses
})
print(chat)
```

### Image Generation

```python
# Generate an image
image_response = client.image.generate({
    "models": ["grok-2-image", "dall-e-3"],
    "prompt": "futuristic city, flying cars, robotic pedestrians.",
    "model_specific_params": {
        "grok-2-image": {
            "n": 1,
            "height": 1024,
            "width": 1024
        }
    },
    "n": 1,
    "height": 1024,
    "width": 1024,
    "seed": 8  # For reproducible results
})
print(image_response)
```

### Image Editing

```python
# Edit an existing image
response = client.image.edit({
    "models": ["nova-canvas"],
    "image_file": "path/to/image.jpg",
    "prompt": "Replace the sky with a sunset"
})
print(response)
```

### Text-to-Speech

```python
# Convert text to speech
tts_response = client.audio.tts({
    "models": ["elevenlabs-multilingual-v2", "gpt-4o-mini-tts"],
    "prompt": "Hello! You're listening to a test of a text-to-speech model...",
    "voice": "nova",
    "model_specific_params": {
        "gpt-4o-mini-tts": {
            "voice": "alternative-voice"
        }
    }
})
print(tts_response)
```

### Speech-to-Text

```python
# Transcribe audio
stt_response = client.audio.stt({
    "models": ["whisper-v3"],
    "audio_file": "path/to/your/audio.mp3"
})
print(stt_response)
```

### Audio Generation

```python
# Generate Audio
response = client.audio.generate({
    "models": ["lyria"],
    "prompt": "Create a relaxing ambient track"
})
print(response)
```

### Video Generation

```python
# Generate a video
video = client.video.generate({
    "models": ["nova-reel"],
    "prompt": "robotic arm assembling a car in a futuristic factory",
    "duration": 6,           # Video length in seconds
    "loop": False,           # Enable looping
    "aspect_ratio": "16:9",  # Video aspect ratio
    "fps": 24,              # Frames per second
    "dimension": "1280x720", # Video dimensions
    "resolution": "720p",    # Output resolution
    "seed": 8               # For reproducible results
})
print(video)
```

### Video Status Check

```python
# Check video generation status
response = client.video.get_video_status({
    "requestId": "your-request-id"
})
print(response)
```

## Error Handling

```python
from alleai.core.exceptions import InvalidRequestError

try:
    response = client.image.generate({
        "models": ["nova-canvas"],
        "prompt": "Your prompt here"
    })
except InvalidRequestError as e:
    print(f"Error: {e.message}")
    print(f"Error Code: {e.code}")
```

## Requirements

- Python 3.8 or higher
- Valid AlleAI API key
- `requests` library (automatically installed with the package)

## Support

For technical support and inquiries:
- Open an issue in our GitHub repository
- Contact our support team at contact@alle-ai.com

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security

```
```

