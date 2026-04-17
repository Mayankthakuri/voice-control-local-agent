"""Audio processing module for microphone and file input."""

import os
import tempfile
from pathlib import Path
from typing import Tuple, Optional
import numpy as np
import soundfile as sf
import librosa


class AudioProcessor:
    """Handles audio input from microphone or files."""
    
    def __init__(self, sample_rate: int = 16000):
        """Initialize audio processor.
        
        Args:
            sample_rate: Target sample rate for audio processing
        """
        self.sample_rate = sample_rate
    
    def load_audio_file(self, file_path: str) -> Tuple[np.ndarray, int]:
        """Load audio from file (.wav, .mp3, etc.).
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        try:
            # librosa.load handles various formats
            audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
            return audio_data, sr
        except Exception as e:
            raise ValueError(f"Failed to load audio file: {str(e)}")
    
    def save_audio_file(
        self, 
        audio_data: np.ndarray, 
        file_path: str, 
        sample_rate: int
    ) -> None:
        """Save audio data to file.
        
        Args:
            audio_data: Audio samples
            file_path: Path where to save
            sample_rate: Sample rate of audio
        """
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        sf.write(file_path, audio_data, sample_rate)
    
    def record_audio(self, duration: int = 10) -> Tuple[np.ndarray, int]:
        """Record audio from microphone.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            import sounddevice as sd
        except ImportError:
            raise ImportError(
                "sounddevice not installed. "
                "Install with: pip install sounddevice"
            )
        
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        print("Recording complete!")
        
        return audio_data.squeeze(), self.sample_rate
    
    def validate_audio(self, audio_data: np.ndarray) -> bool:
        """Validate audio data quality.
        
        Args:
            audio_data: Audio samples to validate
            
        Returns:
            True if audio is valid, False otherwise
        """
        if audio_data.size == 0:
            return False
        
        # Check if audio has signal (not silent)
        rms_energy = np.sqrt(np.mean(audio_data**2))
        return rms_energy > 1e-6
