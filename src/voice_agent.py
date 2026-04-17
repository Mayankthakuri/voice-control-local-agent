"""Main Voice Agent orchestrator - coordinates all components."""

import tempfile
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

from .audio_processor import AudioProcessor
from .stt_engine import STTEngine
from .intent_classifier import IntentClassifier
from .tool_executor import ToolExecutor


@dataclass
class AgentResult:
    """Result from agent pipeline execution."""
    
    timestamp: str
    audio_duration: float
    transcription: str
    intent: str
    intent_confidence: float
    intent_reasoning: str
    tool_result: Dict[str, Any]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp,
            "audio_duration": self.audio_duration,
            "transcription": self.transcription,
            "intent": self.intent,
            "intent_confidence": self.intent_confidence,
            "intent_reasoning": self.intent_reasoning,
            "tool_result": self.tool_result,
            "error": self.error
        }


class VoiceAgent:
    """Main voice-controlled AI agent."""
    
    def __init__(
        self,
        groq_api_key: Optional[str] = None,
        ollama_host: str = "http://localhost:11434",
        sample_rate: int = 16000
    ):
        """Initialize voice agent.
        
        Args:
            groq_api_key: Groq API key for STT
            ollama_host: URL of Ollama server
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate
        self.audio_processor = AudioProcessor(sample_rate=sample_rate)
        self.stt_engine = STTEngine(api_key=groq_api_key)
        self.intent_classifier = IntentClassifier(ollama_host=ollama_host)
        self.tool_executor = ToolExecutor(ollama_host=ollama_host)
        
        # Execution history
        self.history: list[AgentResult] = []
    
    def process_audio_file(self, file_path: str) -> AgentResult:
        """Process audio file through entire pipeline.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Agent execution result with all pipeline stages
        """
        timestamp = datetime.now().isoformat()
        
        try:
            # Step 1: Load audio
            audio_data, sr = self.audio_processor.load_audio_file(file_path)
            audio_duration = len(audio_data) / sr
            
            # Step 2: Validate audio
            if not self.audio_processor.validate_audio(audio_data):
                return AgentResult(
                    timestamp=timestamp,
                    audio_duration=audio_duration,
                    transcription="",
                    intent="general_chat",
                    intent_confidence=0.0,
                    intent_reasoning="Audio validation failed - no signal detected",
                    tool_result={"success": False, "message": "Audio quality too low"},
                    error="Audio validation failed"
                )
            
            # Step 3: Save to temp file for STT (if not already wav)
            temp_file = self._save_temp_audio(audio_data, sr)
            
            # Step 4: Speech-to-Text
            transcription = self.stt_engine.transcribe(temp_file)
            
            if not transcription:
                return AgentResult(
                    timestamp=timestamp,
                    audio_duration=audio_duration,
                    transcription="",
                    intent="general_chat",
                    intent_confidence=0.0,
                    intent_reasoning="STT failed - no text transcribed",
                    tool_result={"success": False, "message": "Transcription failed"},
                    error="Failed to transcribe audio"
                )
            
            # Step 5: Intent Classification
            intent_result = self.intent_classifier.classify(transcription)
            intent = intent_result.get("intent", "general_chat")
            confidence = intent_result.get("confidence", 0.5)
            reasoning = intent_result.get("reasoning", "")
            
            # Step 6: Tool Execution
            tool_result = self.tool_executor.execute(intent, transcription)
            
            # Create result
            result = AgentResult(
                timestamp=timestamp,
                audio_duration=audio_duration,
                transcription=transcription,
                intent=intent,
                intent_confidence=confidence,
                intent_reasoning=reasoning,
                tool_result=tool_result
            )
            
            # Add to history
            self.history.append(result)
            
            # Clean up temp file
            Path(temp_file).unlink(missing_ok=True)
            
            return result
            
        except Exception as e:
            return AgentResult(
                timestamp=timestamp,
                audio_duration=0.0,
                transcription="",
                intent="general_chat",
                intent_confidence=0.0,
                intent_reasoning="Pipeline error",
                tool_result={"success": False, "message": str(e)},
                error=str(e)
            )
    
    def process_microphone_input(self, duration: int = 10) -> AgentResult:
        """Record from microphone and process through pipeline.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Agent execution result
        """
        try:
            # Record audio
            audio_data, sr = self.audio_processor.record_audio(duration=duration)
            
            # Save to temp file and process
            temp_file = self._save_temp_audio(audio_data, sr)
            result = self.process_audio_file(temp_file)
            
            return result
            
        except Exception as e:
            timestamp = datetime.now().isoformat()
            return AgentResult(
                timestamp=timestamp,
                audio_duration=0.0,
                transcription="",
                intent="general_chat",
                intent_confidence=0.0,
                intent_reasoning="Microphone error",
                tool_result={"success": False, "message": str(e)},
                error=str(e)
            )
    
    def _save_temp_audio(self, audio_data, sample_rate: int) -> str:
        """Save audio to temporary file.
        
        Args:
            audio_data: Audio samples
            sample_rate: Sample rate
            
        Returns:
            Path to temporary audio file
        """
        temp_dir = tempfile.gettempdir()
        temp_file = Path(temp_dir) / f"voice_agent_{datetime.now().timestamp()}.wav"
        
        self.audio_processor.save_audio_file(audio_data, str(temp_file), sample_rate)
        
        return str(temp_file)
    
    def get_history(self) -> list[AgentResult]:
        """Get execution history.
        
        Returns:
            List of past execution results
        """
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.history.clear()
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all components.
        
        Returns:
            Dictionary with component health status
        """
        return {
            "stt_api": self.stt_engine.validate_api_key(),
            "ollama_connection": self.intent_classifier.check_ollama_connection(),
            "audio_processor": True  # Always available
        }
