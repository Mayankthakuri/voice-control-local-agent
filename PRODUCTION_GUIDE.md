# 🚀 Production Deployment Guide

## Installation & Setup

### 1. Prerequisites
- Python 3.10+
- Ollama installed (https://ollama.ai)
- Groq API key (https://console.groq.com)

### 2. Quick Setup

```bash
# Clone/Navigate to project
cd "/Users/mayankchand/Public/voice controlled ai agent"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY="gsk_your_key_here"
export OLLAMA_HOST="http://localhost:11434"

# Pull Mistral model
ollama pull mistral
ollama serve  # In a separate terminal

# Run application
streamlit run app.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | Required | Your Groq API key |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |

### Settings in Application

Access via **Advanced** tab:
- Recording duration: 5-60 seconds
- Model temperature: 0.0-1.0
- Retry attempts for API calls
- System diagnostics

## 📊 Features

### Core Features
✅ **Real-time Voice Recording** - Capture audio from microphone
✅ **Audio File Upload** - Process MP3, WAV, FLAC, M4A, OGG, AAC
✅ **AI Intent Classification** - Automatically categorize user requests
✅ **Automatic Task Execution** - Execute actions based on detected intent
✅ **Processing History** - View past requests and results
✅ **System Health Monitoring** - Real-time service status

### Supported Intents
- 🗂️ **create_file** - Create text files with AI-generated content
- 💻 **write_code** - Generate code in various programming languages
- 📄 **summarize** - Summarize large texts efficiently
- 💬 **general_chat** - General conversation and Q&A

## 🔒 Security Best Practices

1. **API Keys**
   - Never commit `.env` files to version control
   - Use environment variables for sensitive data
   - Rotate keys periodically

2. **Data Privacy**
   - Audio files are processed locally when possible
   - Output files stored in `/output` directory
   - No data sent to external services except Groq

3. **Access Control**
   - Run on trusted networks
   - Consider firewall rules for production
   - Use environment-based configuration

## 🚀 Deployment Options

### Local Deployment
```bash
streamlit run app.py
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### Cloud Deployment (Streamlit Cloud)
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy from main branch
4. Set environment variables in dashboard

## 📈 Performance Optimization

### Audio Processing
- Optimal recording: 10-30 seconds
- Supported formats: WAV, MP3, FLAC, M4A, OGG, AAC
- Sample rate: 16kHz (auto-detected)

### API Calls
- Groq Whisper: ~2-5 seconds for 10s audio
- Ollama Mistral: ~3-10 seconds for inference
- Caching enabled for session-level optimization

### Memory Usage
- Typical memory footprint: 1-2GB
- Recommended: 4GB+ for smooth operation
- Stream processing for large files

## 🔍 Monitoring & Logging

### Health Checks
- Access via "⚙️ Advanced" tab → "System Diagnostics"
- Checks: Groq API, Ollama Connection, Audio System
- Real-time status indicators

### Logs
Location: Application console output
- `INFO` - Standard operations
- `WARNING` - Non-critical issues
- `ERROR` - Failures requiring attention

### Troubleshooting
- Check environment variables are set
- Verify Ollama is running
- Ensure models are downloaded
- Check network connectivity

## 📝 Usage Examples

### Recording Audio
1. Click "🎙️ Record Audio" tab
2. Set duration (5-60 seconds)
3. Click "🔴 Start Recording"
4. Speak clearly into microphone
5. View results in "📊 Results" tab

### Upload File
1. Click "📁 Upload File" tab
2. Select audio file (MP3, WAV, etc.)
3. Click "📤 Process File"
4. Check "📊 Results" tab for output

### View History
1. Click "📜 History" tab
2. View processing timeline
3. Expand entries to see details
4. Track confidence scores and intents

## 🆘 Support & Troubleshooting

### Common Issues

**"GROQ_API_KEY not set"**
```bash
export GROQ_API_KEY="gsk_your_actual_key"
```

**"Ollama connection failed"**
```bash
# In separate terminal:
ollama serve

# Check if running:
curl http://localhost:11434/api/tags
```

**"No models installed"**
```bash
ollama pull mistral
```

**Recording not working**
- Check microphone permissions
- Try "🎵 Microphone Test" button
- Verify audio input device is set

## 📋 Maintenance

### Regular Tasks
- Monitor disk usage in `/output` directory
- Review and archive old results
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Check Ollama and Groq service status

### Updates
```bash
# Update Mistral model
ollama pull mistral

# Update dependencies
pip install --upgrade -r requirements.txt
```

## 📞 Support

For issues or features:
- GitHub Issues: https://github.com
- Documentation: https://github.com/README.md
- Groq Support: https://console.groq.com

---

**Version**: 1.0  
**Last Updated**: April 17, 2026  
**Status**: Production Ready ✅
