# 🎤 Voice-Controlled Local AI Agent

A powerful local AI agent that accepts audio input via microphone or file upload, transcribes speech using Groq's Whisper API, classifies user intent with a local LLM (Ollama), and executes tools—all with a clean Streamlit UI.

## 🎯 Features

- **🎙️ Audio Input**: Record from microphone or upload audio files (.wav, .mp3, .m4a, .ogg, .flac)
- **🗣️ Speech-to-Text**: Fast, accurate transcription using Groq's Whisper API
- **🧠 Intent Classification**: Local LLM-based intent understanding (no external calls)
- **⚙️ Tool Execution**: Automatic action execution based on detected intent
  - Create files and folders
  - Generate and save code
  - Summarize text
  - General chat/Q&A
- **🎨 Beautiful UI**: Interactive Streamlit interface with real-time feedback
- **📊 Results Dashboard**: View transcriptions, intents, confidence scores, and outputs
- **📜 Execution History**: Track all past executions with detailed logs

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│           Audio Input (Microphone/File)              │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         AudioProcessor (librosa, soundfile)          │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│        STTEngine (Groq Whisper API) 🌐              │
│         Returns: Transcribed Text                   │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│   IntentClassifier (Ollama - Local LLM)             │
│     Intent: [create_file|write_code|               │
│             summarize|general_chat]                 │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│     ToolExecutor (Intent-Based Actions)             │
│     - File Ops: output/ folder (safe)               │
│     - Code Gen: LLM-generated code                  │
│     - Summarize: Text compression                   │
│     - Chat: Conversational response                 │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│          Streamlit UI (Results Display)             │
│     Show: Transcription, Intent, Actions, Output   │
└─────────────────────────────────────────────────────┘
```

## 📋 Supported Intents

| Intent | Example Command | Action |
|--------|-----------------|--------|
| `create_file` | "Create a config file" | Creates file in `output/` folder |
| `write_code` | "Generate a Python retry function" | Generates code and saves to `output/` |
| `summarize` | "Summarize the following text..." | Compresses text into key points |
| `general_chat` | "What is machine learning?" | Provides conversational response |

## 🛠️ Tech Stack

### Core Components
- **Audio Processing**: `librosa`, `soundfile`, `numpy`
- **Speech-to-Text**: Groq Whisper API (fast, accurate)
- **Intent Classification**: Ollama + Mistral (local, privacy-first)
- **Tool Execution**: Python stdlib + LLM generation
- **UI**: Streamlit (interactive, responsive)

### Why These Choices?
- **Groq STT**: Fast API alternative to running Whisper locally (macOS optimization)
- **Ollama**: Lightweight local LLM—no external calls for intent classification
- **Mistral**: Fast, capable model for intent understanding
- **Streamlit**: Perfect for rapid prototyping and interactive demos

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- macOS, Linux, or Windows
- At least 4GB RAM
- Ollama installed: [ollama.ai](https://ollama.ai)
- Groq API key: [console.groq.com](https://console.groq.com)

### Step 1: Clone Repository

```bash
cd ~/Public/voice\ controlled\ ai\ agent/
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**For Ubuntu/Linux**: You may also need:
```bash
sudo apt-get install libsndfile1
```

### Step 3: Set Up Ollama

```bash
# Install Ollama (macOS/Linux)
# Visit: https://ollama.ai

# Pull the Mistral model
ollama pull mistral

# Start Ollama server
ollama serve
# Runs on http://localhost:11434
```

Leave this running in a separate terminal.

### Step 4: Set Up Groq API

```bash
# Create .env file or export environment variable
export GROQ_API_KEY="your_api_key_here"

# Or create .env file in project root:
echo "GROQ_API_KEY=your_api_key_here" > .env
```

Get your free API key from [console.groq.com](https://console.groq.com)

### Step 5: Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

## 📖 Usage Guide

### Recording from Microphone

1. Click **"🔴 Record & Process"** button
2. Speak clearly into your microphone
3. Wait for the recording to complete (default: 10 seconds)
4. View results in the **"Results"** tab

### Uploading Audio File

1. Click **"📁 Upload Audio File"**
2. Select audio file (.wav, .mp3, etc.)
3. Click **"▶️ Process File"**
4. Wait for transcription and processing
5. View results

### Example Commands

**Create a File:**
> "Create a Python requirements file for a FastAPI project"
```
→ Intent: create_file
→ Creates: output/requirements.txt with FastAPI dependencies
```

**Generate Code:**
> "Write a Python function that implements exponential backoff retry logic"
```
→ Intent: write_code
→ Creates: output/retry_function.py with complete, documented code
```

**Summarize Text:**
> "Summarize the following: [Long text passage]"
```
→ Intent: summarize
→ Returns: Concise 2-3 sentence summary
```

**General Chat:**
> "How do I use OAuth 2.0 in a web application?"
```
→ Intent: general_chat
→ Returns: Detailed explanation
```

## 📁 Project Structure

```
voice controlled ai agent/
├── app.py                    # Streamlit UI
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment template
├── src/
│   ├── __init__.py
│   ├── audio_processor.py    # Audio recording/loading
│   ├── stt_engine.py         # Speech-to-Text (Groq API)
│   ├── intent_classifier.py  # Intent detection (Ollama)
│   ├── tool_executor.py      # Tool execution
│   └── voice_agent.py        # Main orchestrator
├── output/                   # Safe zone for file creation
│   └── (generated files here)
└── tests/                    # Test files
    └── (test files here)
```

## 🔒 Safety & Constraints

### File Creation Restrictions
All file operations are strictly confined to the `output/` folder. This prevents accidental system overwrites.

```python
OUTPUT_DIR = Path(__file__).parent.parent / "output"
# All files created here only!
```

### Filename Sanitization
Dangerous characters are automatically removed from generated filenames.

### Code Generation
Generated code is saved but NOT executed. Review before running.

## 🐛 Troubleshooting

### "Ollama not running" Error
```bash
# Start Ollama in a new terminal
ollama serve

# Verify connection
curl http://localhost:11434/api/tags
```

### "STT API unavailable" Error
```bash
# Check GROQ_API_KEY
echo $GROQ_API_KEY

# Or set it
export GROQ_API_KEY="your_key_here"

# Test API connection
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.groq.com/openai/v1/models
```

### No Audio Input (Microphone)
```bash
# Install sounddevice (if missing)
pip install sounddevice

# Test microphone
python -c "import sounddevice as sd; print(sd.default_device)"
```

### "Cannot transcribe" Error
- Ensure audio is at least 1 second long
- Speak clearly (Whisper model is robust but benefits from clear audio)
- Check file format is supported (.wav, .mp3, .m4a, .ogg, .flac)

### Ollama model not found
```bash
# List available models
ollama list

# Pull Mistral (if missing)
ollama pull mistral

# Try another model
# ollama pull neural-chat  # Smaller, faster alternative
```

## 📊 Performance Metrics

| Component | Latency | Notes |
|-----------|---------|-------|
| Audio Recording | ~10 sec | User speaking duration |
| STT Transcription | ~2-5 sec | Groq API is very fast |
| Intent Classification | ~1-2 sec | Ollama local inference |
| Tool Execution | <1 sec | Most tasks instant |
| **Total End-to-End** | **~15-20 sec** | For typical use case |

## 🔧 Configuration

### Custom Ollama Host
```python
# In app, modify:
ollama_host = "http://your-server:11434"
```

### Different LLM Model
```python
# In src/intent_classifier.py, change:
self.model = "mistral"  # → "neural-chat", "llama2", etc.

# Pull the model first:
ollama pull neural-chat
```

### Audio Sample Rate
```python
# Default 16kHz (optimal for STT)
agent = VoiceAgent(sample_rate=16000)
```

## 📈 Example Output

```json
{
  "timestamp": "2025-01-15T14:32:45.123456",
  "audio_duration": 8.5,
  "transcription": "Create a Python file with a retry function",
  "intent": "write_code",
  "intent_confidence": 0.95,
  "intent_reasoning": "User specifically asks to create code",
  "tool_result": {
    "success": true,
    "message": "Code generated and saved: retry_function.py",
    "file_path": "/path/to/output/retry_function.py",
    "filename": "retry_function.py",
    "language": "python"
  }
}
```

## 🚀 Advanced Features

### Batch Processing
```python
from src.voice_agent import VoiceAgent

agent = VoiceAgent()

files = ["audio1.wav", "audio2.wav", "audio3.wav"]
results = [agent.process_audio_file(f) for f in files]

# Analyze results
for r in results:
    print(f"{r.transcription} → {r.intent}")
```

### Health Checks
```python
health = agent.health_check()
print(health)
# {'stt_api': True, 'ollama_connection': True, 'audio_processor': True}
```

### History & Analytics
```python
results = agent.get_history()

total_audio = sum(r.audio_duration for r in results)
success_rate = sum(1 for r in results if r.tool_result.get("success")) / len(results)

print(f"Total audio: {total_audio}s")
print(f"Success rate: {success_rate:.0%}")
```

## 🎥 Demo

A 2-3 minute demo video showing the system in action is available at:
- **YouTube Unlisted**: [Link to video] (to be recorded)

The demo showcases:
- Microphone recording with live transcription
- Intent classification for multiple scenarios
- Tool execution (file creation, code generation)
- Results dashboard and history

## 📝 Hardware Workarounds

### macOS (M1/M2/M3 Chips)
- **Why Groq**: Running Whisper locally on Apple Silicon can be slow
- **Solution**: Use Groq's API instead (free tier available)
- **Alternative**: Install `mlx-whisper` for on-device inference

### Low-Resource Machine
- Use lighter LLM: `ollama pull neural-chat` (3B parameters)
- Reduce recording duration
- Use GPU acceleration if available

## 🔐 API Keys & Privacy

- **STT (Groq)**: Audio sent to Groq servers (you can review their privacy policy)
- **Intent Classification**: Runs 100% locally (Ollama) - no external calls
- **Tool Execution**: All local

For maximum privacy, replace Groq STT with local Whisper:
```bash
pip install openai-whisper
# Then modify src/stt_engine.py
```

## 📚 Resources

- [Ollama Docs](https://ollama.ai)
- [Groq API](https://console.groq.com)
- [Streamlit Docs](https://docs.streamlit.io)
- [librosa Audio Processing](https://librosa.org)

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Found a bug or want to improve? You're welcome to:
1. Report issues
2. Submit pull requests
3. Suggest features

## 💬 Feedback

Have questions or suggestions? Open an issue or reach out!

---

**Built with ❤️ for voice-first computing**
