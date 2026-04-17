"""Unit tests for Voice Agent components."""

import pytest
import tempfile
from pathlib import Path
import numpy as np
from unittest.mock import Mock, patch, MagicMock

import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.audio_processor import AudioProcessor
from src.intent_classifier import IntentClassifier
from src.tool_executor import ToolExecutor


class TestAudioProcessor:
    """Test AudioProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance."""
        return AudioProcessor(sample_rate=16000)
    
    def test_initialization(self, processor):
        """Test initialization."""
        assert processor.sample_rate == 16000
    
    def test_validate_audio_valid(self, processor):
        """Test validation of valid audio."""
        # Create valid audio signal
        audio = np.random.randn(16000) * 0.1  # 1 second at 16kHz
        assert processor.validate_audio(audio) is True
    
    def test_validate_audio_silent(self, processor):
        """Test validation of silent audio."""
        # Create silent audio
        audio = np.zeros(16000)
        assert processor.validate_audio(audio) is False
    
    def test_validate_audio_empty(self, processor):
        """Test validation of empty audio."""
        audio = np.array([])
        assert processor.validate_audio(audio) is False
    
    def test_save_and_load_audio(self, processor):
        """Test saving and loading audio."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create audio
            audio = np.random.randn(16000) * 0.1
            file_path = Path(tmpdir) / "test.wav"
            
            # Save
            processor.save_audio_file(audio, str(file_path), 16000)
            assert file_path.exists()
            
            # Load
            loaded_audio, sr = processor.load_audio_file(str(file_path))
            assert sr == 16000
            assert len(loaded_audio) > 0
    
    def test_load_nonexistent_file(self, processor):
        """Test loading nonexistent file."""
        with pytest.raises(FileNotFoundError):
            processor.load_audio_file("/nonexistent/file.wav")


class TestIntentClassifier:
    """Test IntentClassifier class."""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance."""
        return IntentClassifier()
    
    def test_initialization(self, classifier):
        """Test initialization."""
        assert classifier.model == "mistral"
        assert "create_file" in classifier.SUPPORTED_INTENTS
        assert "write_code" in classifier.SUPPORTED_INTENTS
        assert "summarize" in classifier.SUPPORTED_INTENTS
        assert "general_chat" in classifier.SUPPORTED_INTENTS
    
    def test_heuristic_classify_create_file(self, classifier):
        """Test heuristic classification for create_file."""
        text = "Create a new file called config.json"
        intent = classifier._heuristic_classify(text)
        assert intent == "create_file"
    
    def test_heuristic_classify_write_code(self, classifier):
        """Test heuristic classification for write_code."""
        text = "Write a Python function for exponential backoff"
        intent = classifier._heuristic_classify(text)
        assert intent == "write_code"
    
    def test_heuristic_classify_summarize(self, classifier):
        """Test heuristic classification for summarize."""
        text = "Summarize the following article about machine learning"
        intent = classifier._heuristic_classify(text)
        assert intent == "summarize"
    
    def test_heuristic_classify_general_chat(self, classifier):
        """Test heuristic classification for general_chat."""
        text = "What is the meaning of life?"
        intent = classifier._heuristic_classify(text)
        assert intent == "general_chat"
    
    def test_empty_text_classification(self, classifier):
        """Test classification of empty text."""
        result = classifier.classify("")
        assert result["intent"] == "general_chat"
        assert result["confidence"] == 0.0


class TestToolExecutor:
    """Test ToolExecutor class."""
    
    @pytest.fixture
    def executor(self):
        """Create executor instance."""
        return ToolExecutor()
    
    def test_initialization(self, executor):
        """Test initialization."""
        assert executor.model == "mistral"
        assert executor.OUTPUT_DIR.exists()
    
    def test_sanitize_filename_remove_slashes(self, executor):
        """Test filename sanitization removes slashes."""
        filename = "folder/file.txt"
        sanitized = executor._sanitize_filename(filename)
        assert "/" not in sanitized
        assert sanitized == "folder_file.txt"
    
    def test_sanitize_filename_remove_special_chars(self, executor):
        """Test filename sanitization removes special chars."""
        filename = "file*.txt?"
        sanitized = executor._sanitize_filename(filename)
        assert "*" not in sanitized and "?" not in sanitized
    
    def test_sanitize_filename_max_length(self, executor):
        """Test filename length is limited."""
        filename = "a" * 300 + ".txt"
        sanitized = executor._sanitize_filename(filename)
        assert len(sanitized) <= 255
    
    def test_detect_language_python(self, executor):
        """Test language detection for Python."""
        lang = executor._detect_language("script.py")
        assert lang == "python"
    
    def test_detect_language_javascript(self, executor):
        """Test language detection for JavaScript."""
        lang = executor._detect_language("app.js")
        assert lang == "javascript"
    
    def test_detect_language_unknown(self, executor):
        """Test language detection for unknown."""
        lang = executor._detect_language("file.unknown")
        assert lang == "text"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
