# 🎯 Getting Started - Detailed Walkthrough

This guide walks you through setting up and using the Voice Agent.

## Part 1: Installation

### 1A. Install Ollama

**macOS:**
```bash
# Download from website
open https://ollama.ai

# Or with Homebrew
brew install ollama

# Verify
ollama --version
```

**Linux (Ubuntu/Debian):**
```bash
curl https://ollama.ai/install.sh | sh
```

**Windows:**
- Download from https://ollama.ai
- Run installer
- Add to PATH

### 1B. Download Projects

```bash
# No GitHub setup needed for local testing
cd ~/Public/voice\ controlled\ ai\ agent/
```

### 1C. Install Python Dependencies

```bash
# Navigate to project
cd ~/Public/voice\ controlled\ ai\ agent/

# Create isolated environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\Activate.ps1  # Windows

# Install all packages
pip install --upgrade pip
pip install -r requirements.txt

# Verify
python -c "import streamlit; print('✅ Streamlit OK')"
```

### 1D. Get Groq API Key

1. Visit https://console.groq.com
2. Sign up (free account)
3. Create API key
4. Copy the key

```bash
# Set environment variable
export GROQ_API_KEY="gsk_your_actual_key_here"

# Or create .env file
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# Verify
echo $GROQ_API_KEY  # Should show your key
```

## Part 2: Startup

### Terminal 1: Start Ollama

```bash
# Pull Mistral model (first time only)
ollama pull mistral

# Start server
ollama serve

# You should see:
# "Listening on 127.0.0.1:11434"
# Keep this running!
```

### Terminal 2: Verify Everything Works

```bash
# Navigate to project
cd ~/Public/voice\ controlled\ ai\ agent/

# Activate environment
source venv/bin/activate

# Run verification script
python verify_setup.py

# Should show:
# ✅ Streamlit
# ✅ All dependencies
# ✅ GROQ_API_KEY set
# ✅ Ollama running
```

### Terminal 2: Start Application

```bash
# (Keep virtual environment activated from above)

# Run Streamlit
streamlit run app.py

# Should open automatically at:
# http://localhost:8501
```

## Part 3: Using the Application

### First Time Setup

1. **Check System Health**
   - Sidebar: Click 🔍 "Check System Health"
   - All should show ✅ (green)

2. **Understand the UI**
   - **🎙️ Input Tab**: Record or upload audio
   - **📊 Results Tab**: See what the system did
   - **📜 History Tab**: Past executions

### Recording Audio

1. Go to **🎙️ Input** tab
2. Click **"🔴 Record & Process"** button
3. Speak clearly for 10 seconds
   - Example: *"Create a Python file with a retry function"*
4. Wait for processing (~15-20 seconds total)
5. Results appear in **📊 Results** tab

### Uploading Files

1. Go to **🎙️ Input** tab
2. Click **"📁 Upload Audio File"**
3. Select file (.wav, .mp3, .m4a, .ogg)
4. Click **"▶️ Process File"**
5. Wait for processing
6. Results appear in **📊 Results** tab

### Understanding Results

The **📊 Results** tab shows:

```
📋 Pipeline Results
─────────────────────
Duration:      8.5s         (your audio length)
Intent:        Write Code   (what you asked for)
Confidence:    95%          (how sure AI is)
Status:        ✅ Success   (did it work?)

📝 Transcription
─────────────────────
"Create a Python file with a retry function"
↓ (what Whisper heard)

🎯 Intent Classification
─────────────────────
Intent:   write_code
Confidence: 0.95
Reasoning: User specifically asks to write code
↓ (what local LLM understood)

⚙️ Tool Execution
─────────────────────
{
  "success": true,
  "message": "Code generated and saved: retry_function.py",
  "file_path": "/Users/.../output/retry_function.py",
  "language": "python"
}
↓ (what tool created)
```

### Viewing Generated Files

Generated files are saved in the `output/` folder:

```bash
# View what was created
ls -la output/

# Open a generated file
cat output/retry_function.py

# Download from UI: Go to Results tab → "Download as JSON"
```

## Part 4: Example Commands

### Example 1: Create File
**Say:** "Create a config file for a web server"

```
→ Intent:    create_file
→ Result:    output/config.json created
→ Content:   {
               "port": 8000,
               "host": "0.0.0.0",
               "debug": false
             }
```

### Example 2: Write Code
**Say:** "Generate a Python function that validates email addresses"

```
→ Intent:    write_code
→ Result:    output/email_validator.py created
→ Content:   def validate_email(email: str) -> bool:
               """Validates email format..."""
               ...
```

### Example 3: Summarize Text
**Say:** "Summarize the following: [paste long text]"

```
→ Intent:    summarize
→ Result:    Summary displayed
→ Summary:   "The article discusses recent advances in
              machine learning and their applications
              in healthcare industry..."
```

### Example 4: General Chat
**Say:** "What are the benefits of microservices architecture?"

```
→ Intent:    general_chat
→ Result:    Response displayed
→ Response:  "Microservices architecture provides
              several benefits including scalability,
              flexibility, and independent deployment..."
```

## Part 5: Troubleshooting

### "Red X marks" in System Health

**STT API ❌**
```bash
# Problem: GROQ_API_KEY not set or invalid
echo $GROQ_API_KEY
# If empty, set it:
export GROQ_API_KEY="gsk_your_key_from_console.groq.com"
```

**Ollama ❌**
```bash
# Problem: Ollama not running
# Solution: Start Ollama in Terminal 1
ollama serve

# Or check if it's listening
curl http://localhost:11434/api/tags
```

### "No transcription available"

**Possible causes:**
1. Audio too quiet → Speak louder
2. Audio too short → Record for at least 3 seconds
3. Groq API rate limit → Wait a minute, try again
4. No microphone → Use file upload instead

### "Intent classification failed"

**Possible causes:**
1. Ollama crashed → Restart: `ollama serve`
2. Model not installed → Run: `ollama pull mistral`
3. Network error → Check internet connection

### "Cannot create files"

**Possible causes:**
1. output/ folder missing → Automatically recreated, restart
2. No write permission → Check folder permissions
3. Disk full → Free up space

## Part 6: Advanced Usage

### Batch Processing

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.voice_agent import VoiceAgent

agent = VoiceAgent()

# Process multiple files
files = ["audio1.wav", "audio2.wav", "audio3.wav"]
for file in files:
    result = agent.process_audio_file(file)
    print(f"{result.transcription} → {result.intent}")
```

### Access History

```python
# Get all past results
history = agent.get_history()

for result in history:
    print(f"[{result.timestamp}] {result.transcription}")
    print(f"  Intent: {result.intent} ({result.intent_confidence:.0%})")
    print()
```

### Custom Configuration

Edit `config.py` to customize:
```python
# Change sample rate
AUDIO_SAMPLE_RATE = 44100

# Change recording duration
AUDIO_RECORDING_DURATION = 30

# Change LLM model
OLLAMA_MODEL = "neural-chat"  # Smaller, faster
```

## Part 7: Next Steps

1. ✅ **Try all intent types** - test each command
2. ✅ **Upload different audio formats** - .mp3, .m4a, etc.
3. ✅ **Check generated files** - inspect output/
4. ✅ **Review history** - 📜 History tab
5. ✅ **Read architecture** - See `ARCHITECTURE.md`
6. ✅ **Deploy to cloud** - See `DEPLOYMENT.md`

## Support & Docs

- **Quick issues?** → See Troubleshooting above
- **More details?** → Read `README.md`
- **Technical deep dive?** → Read `ARCHITECTURE.md`
- **Deploy online?** → Read `DEPLOYMENT.md`
- **Examples?** → Run `python examples.py --example health`

---

**You're all set! Start with the input tab and try saying:**

> *"Create a Python file that prints 'Hello, Voice Agent!'"*

Enjoy! 🎤✨
