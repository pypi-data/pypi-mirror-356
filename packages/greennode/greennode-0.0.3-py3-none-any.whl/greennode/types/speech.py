from __future__ import annotations

from typing import List, Literal, Optional
import base64
from pydantic import BaseModel, Field
from datetime import datetime
import requests
import json

from greennode.types.abstract import BaseModel
from greennode.types.common import (
    ObjectType,
)


class SpeechRequest(BaseModel):
    """Request model for speech API."""
    model: str = Field(description="The TTS model to use")
    voice: str | int = Field(description="Voice ID or name")
    input: str = Field(description="The text to convert to speech")
    response_format: str = Field(default="b64_json", description="Response format type")

    def to_dict(self) -> dict:
        """Convert the request to a dictionary."""
        return self.model_dump(exclude_none=True)


class SpeechChoicesData(BaseModel):
    """Represents a single generated audio data."""
    b64_json: str = Field(description="Base64 encoded audio data")
    url: Optional[str] = Field(default=None, description="URL to the audio file if available")
    content_type: Optional[str] = Field(default="audio/mp3", description="MIME type of the audio")

    def save_audio(self, filename: str) -> None:
        """Save the base64-encoded audio to a file."""
        with open(filename, "wb") as f:
            f.write(base64.b64decode(self.b64_json))

    @classmethod
    def from_binary(cls, binary_data: bytes, content_type: str = "audio/mp3") -> "SpeechChoicesData":
        """Create an instance from binary audio data."""
        b64_data = base64.b64encode(binary_data).decode('utf-8')
        return cls(b64_json=b64_data, content_type=content_type)


class SpeechResponse(BaseModel):
    """Represents the full speech response with audio data."""


    @classmethod
    def from_binary_response(cls, binary_data: bytes, output_file: str | None = None) -> "SpeechResponse":
        """Create a response object from binary audio data and save it to a file."""
        # Create audio data
        audio_data = SpeechChoicesData.from_binary(binary_data)
        
        # Save to file
        if output_file:
            with open(output_file, "wb") as f:
                f.write(binary_data)
        
        # Return response object
        return audio_data

    def get_audio_data(self) -> bytes:
        """Get the binary audio data from the first result."""
        if not self.data or not self.data[0].b64_json:
            raise ValueError("No audio data available")
        return base64.b64decode(self.data[0].b64_json)

    def save_audio(self, filename: str) -> None:
        """Save the audio data to a file."""
        audio_data = self.get_audio_data()
        with open(filename, "wb") as f:
            f.write(audio_data)