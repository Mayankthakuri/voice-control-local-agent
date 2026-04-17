# ⚡ Quick Start Guide

Get started with Voice Agent in **5 minutes**!

## Prerequisites

- Python 3.10+
- Ollama installed
- Groq API key

## Step 1: Setup (2 min)

```bash
# Navigate to project
cd ~/Public/voice\ controlled\ ai\ agent/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Set API key (replace with your actual key)
export GROQ_API_KEY="gsk_your_key_here"
```

## Step 2: Start Ollama (1 min)

Open a **new terminal**:

```bash
# Pull and start Ollama
ollama pull mistral
ollama serve
```

Wait for: `Listening on 127.0.0.1:11434`

## Step 3: Run App (1 min)

Go back to **first terminal**:

```bash
streamlit run app.py
```

Automatically opens at: `http://localhost:8501`

## Step 4: Test (1 min)

1. Click **"🔴 Record & Process"**
2. Speak: *"Create a Python file with a retry function"*
3. See results!

---

## Verify Setup

Not sure if everything is working?

```bash
# Comprehensive check
python verify_setup.py
```

Checks:
- ✅ Python dependencies
- ✅ GROQ_API_KEY configured
- ✅ Ollama running
- ✅ Output directory writable

---

## Common Issues

### "Ollama connection refused"
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Verify (new terminal)
curl http://localhost:11434/api/tags
```

### "GROQ_API_KEY not found"
```bash
# Set it
export GROQ_API_KEY="your_key_from_console.groq.com"

# Verify
echo $GROQ_API_KEY
```

### "Audio not recording"
```bash
# Install microphone support
pip install sounddevice

# Test:
python -c "import sounddevice; print('OK')"
```

---

## Example Use Cases

### Create a File
Say: **"Create a requirements file for a Django project"**

→ Status: ✅ Success  
→ File: `output/requirements.txt`  
→ Content: FastAPI, SQLAlchemy, etc.

### Generate Code
Say: **"Write a Python decorator for caching function results"**

→ Status: ✅ Success  
→ File: `output/caching_decorator.py`  
→ Language: Python with docstrings

### Summarize Text
Say: **"Summarize this long article about AI safety"**

→ Status: ✅ Success  
→ Summary: 2-3 key points extracted

### General Chat
Say: **"What are the security best practices for API design?"**

→ Status: ✅ Success  
→ Response: Detailed explanation

---

## Next Steps

1. **Try different commands** - explore all intents
2. **Upload audio files** - test with .mp3, .wav files
3. **View history** - check the "📜 History" tab
4. **Read full docs** - see `README.md` for advanced features

---

## Performance Tips

| Action | Time |
|--------|------|
| Recording audio | ~10 sec (depends on you) |
| Transcription | ~2-5 sec |
| Intent classification | ~1-2 sec |
| Tool execution | <1 sec |
| **Total** | **~15-20 sec** |

💡 **Tip**: Keep Ollama running in background for faster inference!

---

## What's Inside?

```
📦 voice-agent/
├── app.py                 ← Run this: streamlit run app.py
├── src/
│   ├── audio_processor.py ← Microphone/file input
│   ├── stt_engine.py      ← Speech-to-Text
│   ├── intent_classifier.py ← LLM intent detection
│   ├── tool_executor.py   ← Execute actions
│   └── voice_agent.py     ← Orchestrator
├── output/                ← Generated files stored here
├── README.md              ← Full documentation
└── ARCHITECTURE.md        ← Technical deep dive
```

---

Enjoy! 🎤✨

For support: [Check README.md troubleshooting section](README.md#-troubleshooting)
