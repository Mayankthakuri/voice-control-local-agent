"""Configuration module for Voice Agent."""

import os
from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


class Config:
    """Application configuration."""
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Ollama
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # Audio
    AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    AUDIO_RECORDING_DURATION = int(os.getenv("AUDIO_RECORDING_DURATION", "10"))
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent
    OUTPUT_DIR = PROJECT_ROOT / "output"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration.
        
        Returns:
            True if all required configs are set
        """
        if not cls.GROQ_API_KEY:
            print("⚠️  Warning: GROQ_API_KEY not set. STT will fail.")
            return False
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """Get configuration as dictionary.
        
        Returns:
            Configuration dictionary
        """
        return {
            "groq_api_key_set": bool(cls.GROQ_API_KEY),
            "ollama_host": cls.OLLAMA_HOST,
            "ollama_model": cls.OLLAMA_MODEL,
            "audio_sample_rate": cls.AUDIO_SAMPLE_RATE,
            "output_dir": str(cls.OUTPUT_DIR)
        }
