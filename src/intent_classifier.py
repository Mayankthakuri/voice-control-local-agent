"""Intent classification using local LLM."""

import json
from typing import Dict, List, Optional, Any
import requests
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class IntentClassifier:
    """Classify user intents using local LLM (Ollama)."""
    
    SUPPORTED_INTENTS = {
        "create_file": "Create a new file or folder",
        "write_code": "Write or generate code to a file",
        "summarize": "Summarize provided text content",
        "general_chat": "General conversation or question"
    }
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        """Initialize intent classifier.
        
        Args:
            ollama_host: Ollama server URL
        """
        self.ollama_host = ollama_host
        self.model = "mistral"  # Fast, capable model for local use
        self.api_endpoint = f"{ollama_host}/api/generate"
    
    def classify(self, text: str) -> Dict[str, any]:
        """Classify intent from user text.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with intent and confidence score
        """
        if not text or len(text.strip()) == 0:
            return {
                "intent": "general_chat",
                "confidence": 0.0,
                "reasoning": "Empty input"
            }
        
        prompt = self._create_prompt(text)
        
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3
                },
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            response_text = result.get("response", "").strip()
            
            return self._parse_response(response_text, text)
            
        except requests.exceptions.RequestException as e:
            return {
                "intent": "general_chat",
                "confidence": 0.5,
                "reasoning": f"LLM error: {str(e)}"
            }
    
    def _create_prompt(self, text: str) -> str:
        """Create classification prompt for LLM.
        
        Args:
            text: User input text
            
        Returns:
            Formatted prompt
        """
        intents_list = "\n".join([f"- {k}: {v}" for k, v in self.SUPPORTED_INTENTS.items()])
        
        return f"""You are an intent classifier. Analyze the user's input and classify it into ONE of these intents:

{intents_list}

Respond with ONLY a JSON object (no markdown, no text before or after) in this exact format:
{{"intent": "create_file|write_code|summarize|general_chat", "confidence": 0.0-1.0, "reasoning": "1-2 words"}}

User input: \"{text}\"

JSON Response:"""
    
    def _parse_response(self, response: str, original_text: str) -> Dict[str, Any]:
        """Parse LLM response.
        
        Args:
            response: Response from LLM
            original_text: Original user input
            
        Returns:
            Parsed classification result
        """
        try:
            # Try to extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                return self._default_classification(original_text)
            
            json_str = response[json_start:json_end]
            parsed = json.loads(json_str)
            
            # Validate intent
            intent = parsed.get("intent", "general_chat")
            if intent not in self.SUPPORTED_INTENTS:
                intent = self._heuristic_classify(original_text)
            
            return {
                "intent": intent,
                "confidence": float(parsed.get("confidence", 0.7)),
                "reasoning": parsed.get("reasoning", "")
            }
            
        except (json.JSONDecodeError, ValueError):
            return self._default_classification(original_text)
    
    def _heuristic_classify(self, text: str) -> str:
        """Fallback heuristic classification.
        
        Args:
            text: User input text
            
        Returns:
            Classified intent
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["create", "make", "new file", "mkdir"]):
            return "create_file"
        elif any(word in text_lower for word in ["write", "code", "function", "class", "def", "python", "javascript"]):
            return "write_code"
        elif any(word in text_lower for word in ["summarize", "summary", "sum up", "brief"]):
            return "summarize"
        
        return "general_chat"
    
    def _default_classification(self, text: str) -> Dict[str, Any]:
        """Return default classification when parsing fails.
        
        Args:
            text: User input text
            
        Returns:
            Default classification result
        """
        intent = self._heuristic_classify(text)
        return {
            "intent": intent,
            "confidence": 0.5,
            "reasoning": "Fallback heuristic classification"
        }
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running.
        
        Returns:
            True if Ollama is accessible
        """
        try:
            response = requests.get(
                f"{self.ollama_host}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
