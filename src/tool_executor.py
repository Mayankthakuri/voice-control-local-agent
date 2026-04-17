"""Tool execution engine for file operations, code generation, and text processing."""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
import requests
from functools import lru_cache

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Execute tools based on classified intent."""
    
    OUTPUT_DIR = Path(__file__).parent.parent / "output"
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        """Initialize tool executor.
        
        Args:
            ollama_host: Ollama server URL
        """
        self.ollama_host = ollama_host
        self.model = "mistral"
        self.api_endpoint = f"{ollama_host}/api/generate"
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Ensure output directory exists."""
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    def execute(self, intent: str, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute tool based on intent.
        
        Args:
            intent: Classified intent
            text: Original user input
            context: Additional context
            
        Returns:
            Execution result
        """
        context = context or {}
        
        if intent == "create_file":
            return self._create_file_tool(text)
        elif intent == "write_code":
            return self._write_code_tool(text)
        elif intent == "summarize":
            return self._summarize_tool(text, context)
        else:  # general_chat
            return self._general_chat_tool(text)
    
    def _create_file_tool(self, user_request: str) -> Dict[str, Any]:
        """Create file based on user request.
        
        Args:
            user_request: User's file creation request
            
        Returns:
            Tool execution result
        """
        try:
            prompt = f"""Create file from request. JSON ONLY:
{{"filename": "name.ext", "content": "content"}}

Request: {user_request}"""
            
            response_text = self._call_ollama(prompt, retries=2)
            
            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                plan = json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                logger.warning(f"Failed to parse response: {response_text[:100]}")
                return {
                    "success": False,
                    "message": "Failed to parse file creation",
                    "details": None
                }
            
            filename = plan.get("filename", "output.txt")
            content = plan.get("content", "")
            
            # Sanitize filename
            filename = self._sanitize_filename(filename)
            file_path = self.OUTPUT_DIR / filename
            
            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(file_path, "w") as f:
                f.write(content)
            
            logger.info(f"Created file: {filename}")
            
            return {
                "success": True,
                "message": f"File created: {filename}",
                "file_path": str(file_path),
                "filename": filename,
                "content_preview": content[:200] + "..." if len(content) > 200 else content
            }
            
        except Exception as e:
            logger.error(f"Error creating file: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "details": None
            }
    
    def _write_code_tool(self, user_request: str) -> Dict[str, Any]:
        """Generate and write code.
        
        Args:
            user_request: Code generation request
            
        Returns:
            Tool execution result
        """
        try:
            prompt = f"""Generate code from request. JSON ONLY:
{{"code": "full code", "filename": "name.py"}}

Request: {user_request}"""
            
            response_text = self._call_ollama(prompt, retries=2, temperature=0.5)
            
            try:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                logger.warning(f"Failed to parse code response: {response_text[:100]}")
                return {
                    "success": False,
                    "message": "Failed to generate code",
                    "details": None
                }
            
            code = result.get("code", "")
            filename = result.get("filename", "generated_code.py")
            filename = self._sanitize_filename(filename)
            
            file_path = self.OUTPUT_DIR / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w") as f:
                f.write(code)
            
            logger.info(f"Generated code: {filename}")
            
            return {
                "success": True,
                "message": f"Code saved: {filename}",
                "file_path": str(file_path),
                "filename": filename,
                "code_preview": code[:300] + "..." if len(code) > 300 else code,
                "language": self._detect_language(filename)
            }
            
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "details": None
            }
    
    def _summarize_tool(self, user_input: str, context: Dict) -> Dict[str, Any]:
        """Summarize text concisely.
        
        Args:
            user_input: User input
            context: Context with content
            
        Returns:
            Tool execution result
        """
        try:
            text_to_summarize = context.get("content", user_input)
            
            prompt = f"""Summarize in 2-3 sentences:

\"{text_to_summarize}\"

Summary:"""
            
            summary = self._call_ollama(prompt, retries=1, temperature=0.2).strip()
            
            logger.info("Text summarized")
            
            return {
                "success": True,
                "message": "Summarized successfully",
                "summary": summary,
                "original_length": len(text_to_summarize),
                "summary_length": len(summary)
            }
            
        except Exception as e:
            logger.error(f"Error summarizing: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "details": None
            }
    
    def _general_chat_tool(self, user_input: str) -> Dict[str, Any]:
        """Generate chat response.
        
        Args:
            user_input: User input
            
        Returns:
            Chat response
        """
        try:
            response = self._call_ollama(user_input, retries=1)
            
            logger.debug("Chat response generated")
            
            return {
                "success": True,
                "message": "Response generated",
                "response": response
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "details": None
            }
    
    def _call_ollama(self, prompt: str, retries: int = 1, temperature: float = 0.3) -> str:
        """Call Ollama API with retry logic.
        
        Args:
            prompt: Prompt for the model
            retries: Number of retries on failure
            temperature: Model temperature (0.0-1.0)
            
        Returns:
            Model response
            
        Raises:
            RuntimeError: If API call fails after retries
        """
        last_error = None
        
        for attempt in range(retries + 1):
            try:
                response = requests.post(
                    self.api_endpoint,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "temperature": temperature
                    },
                    timeout=45
                )
                response.raise_for_status()
                result = response.json()
                text = result.get("response", "").strip()
                
                if text:
                    logger.debug(f"Ollama response (attempt {attempt + 1})")
                    return text
                    
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < retries:
                    logger.warning(f"Ollama API error (attempt {attempt + 1}/{retries + 1}): {str(e)}")
                    continue
        
        error_msg = f"Ollama API failed after {retries + 1} attempts: {str(last_error)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe writing.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove dangerous characters
        dangerous_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Ensure it's not empty
        if not filename or filename == "":
            filename = "output.txt"
        
        return filename[:255]  # Max filename length
    
    def _detect_language(self, filename: str) -> str:
        """Detect programming language from filename.
        
        Args:
            filename: Filename
            
        Returns:
            Language name
        """
        ext_to_lang = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".go": "go",
            ".rs": "rust",
            ".rb": "ruby",
            ".php": "php",
            ".sql": "sql",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".yaml": "yaml",
            ".xml": "xml",
            ".sh": "bash",
        }
        
        ext = Path(filename).suffix.lower()
        return ext_to_lang.get(ext, "text")