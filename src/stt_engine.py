"""Speech-to-Text engine using Groq API."""

import os
from typing import Optional
import requests
from pathlib import Path


class STTEngine:
    """Speech-to-Text engine using Groq API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize STT engine.
        
        Args:
            api_key: Groq API key. If None, tries to load from environment.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key not found. "
                "Set GROQ_API_KEY environment variable or pass api_key parameter."
            )
        
        self.api_url = "https://api.groq.com/openai/v1/audio/transcriptions"
        self.model = "whisper-large-v3-turbo"
    
    def transcribe(self, audio_file_path: str) -> str:
        """Transcribe audio file to text.
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text
            
        Raises:
            FileNotFoundError: If audio file not found
            RuntimeError: If API call fails
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                # Detect MIME type from file extension
                file_ext = Path(audio_file_path).suffix.lower()
                mime_type_map = {
                    '.wav': 'audio/wav',
                    '.mp3': 'audio/mpeg',
                    '.m4a': 'audio/mp4',
                    '.ogg': 'audio/ogg',
                    '.flac': 'audio/flac',
                    '.aac': 'audio/aac'
                }
                mime_type = mime_type_map.get(file_ext, 'audio/wav')
                
                files = {
                    "file": (
                        Path(audio_file_path).name,
                        audio_file,
                        mime_type
                    )
                }
                headers = {"Authorization": f"Bearer {self.api_key}"}
                data = {"model": self.model}
                
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=60  # Increased timeout for better reliability
                )
                
                response.raise_for_status()
                result = response.json()
                
                text = result.get("text", "").strip()
                if not text:
                    raise RuntimeError("Empty transcription returned by API")
                
                return text
                
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Transcription API error: {str(e)}")
    
    def validate_api_key(self) -> bool:
        """Validate API key by making a test call.
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
