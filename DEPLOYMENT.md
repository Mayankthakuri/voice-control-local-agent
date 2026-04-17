# 📦 Deployment Guide

## Local Development Setup

### macOS

**1. Install Required Tools**
```bash
# Using Homebrew
brew install python3 ollama

# Or download from:
# - Python: https://www.python.org/downloads
# - Ollama: https://ollama.ai
```

**2. Clone and Setup Project**
```bash
cd ~/Public/voice\ controlled\ ai\ agent/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# For microphone support (optional)
pip install sounddevice
```

**3. Configure APIs**
```bash
# Get Groq API key from https://console.groq.com
export GROQ_API_KEY="your_key_here"

# Or create .env file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

**4. Start Ollama Server**
```bash
# In terminal 1
ollama serve

# In terminal 2, pull models
ollama pull mistral
ollama pull neural-chat  # Optional: lightweight alternative

# Verify
curl http://localhost:11434/api/tags
```

**5. Run Application**
```bash
# Terminal 3 (in project directory with venv activated)
streamlit run app.py

# Opens at http://localhost:8501
```

### Linux (Ubuntu/Debian)

**1. Install Dependencies**
```bash
# Update package manager
sudo apt update && sudo apt upgrade

# Install Python and development tools
sudo apt install -y python3-pip python3-venv python3-dev
sudo apt install -y libsndfile1  # Audio library

# Install Ollama
curl https://ollama.ai/install.sh | sh
```

**2. Setup Project**
```bash
cd ~/voice-controlled-ai-agent

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
pip install sounddevice  # For microphone support
```

**3. Configure and Run**
```bash
# Set API key
export GROQ_API_KEY="your_key_here"

# Start Ollama (background)
ollama serve &

# Wait for Ollama startup
sleep 3

# Pull Mistral
ollama pull mistral

# Start Streamlit
streamlit run app.py
```

### Windows

**1. Install Requirements**
```powershell
# Download and install:
# - Python 3.10+: https://python.org
# - Ollama: https://ollama.ai
# - Git (optional): https://git-scm.com

# Open PowerShell as Administrator
python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
pip install sounddevice
```

**2. Set Environment Variable**
```powershell
# Set API key
$env:GROQ_API_KEY="your_key_here"

# Or permanently (Settings → Environment Variables)
```

**3. Run**
```powershell
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Activate venv and run app
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

---

## Docker Deployment

### Build Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501 || exit 1

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t voice-agent:latest .

# Run container (requires external Ollama)
docker run -e GROQ_API_KEY="your_key" \
           -p 8501:8501 \
           --network host \
           voice-agent:latest

# Or with Docker Compose (see below)
```

### Docker Compose Setup

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    command: serve

  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - OLLAMA_HOST=http://ollama:11434
    depends_on:
      - ollama
    volumes:
      - ./output:/app/output

volumes:
  ollama_data:
```

**Run with Compose:**
```bash
# Set environment variable
export GROQ_API_KEY="your_key_here"

# Start both services
docker-compose up

# Stop
docker-compose down
```

---

## Cloud Deployment

### Option 1: Render

**Create `render.yaml`:**
```yaml
services:
  - type: web
    name: voice-agent
    env: python
    plan: standard
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port 10000 --server.address 0.0.0.0
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: OLLAMA_HOST
        value: http://ollama-service:11434
```

**Deploy:**
```bash
# Push to GitHub
git push origin main

# Connect repo to Render.com
# → Select Python
# → Build & Deploy
```

### Option 2: Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

### Option 3: AWS EC2

**1. Launch EC2 Instance**
```bash
# AMI: Ubuntu 22.04 LTS
# Instance: t3.medium or larger
# Storage: 20GB minimum
```

**2. SSH and Setup**
```bash
ssh -i key.pem ubuntu@instance-ip

# Install dependencies
sudo apt update && sudo apt upgrade
sudo apt install -y python3-pip python3-venv \
                   libsndfile1 curl docker.io

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install Ollama
curl https://ollama.ai/install.sh | sh
```

**3. Deploy Application**
```bash
# Clone repo
git clone <your-repo> voice-agent
cd voice-agent

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Ollama
ollama serve &
sleep 2
ollama pull mistral

# Start Streamlit with Nginx reverse proxy
nohup streamlit run app.py > app.log 2>&1 &
```

**4. Setup Nginx Reverse Proxy**
```bash
sudo apt install -y nginx

# Configure /etc/nginx/sites-available/default
sudo nano /etc/nginx/sites-available/default
```

**Nginx config:**
```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://streamlit;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

---

## Production Checklist

- [ ] Environment variables set (GROQ_API_KEY, OLLAMA_HOST)
- [ ] Ollama running and accessible
- [ ] output/ directory created and writable
- [ ] SSL/HTTPS configured
- [ ] Logging enabled
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] API rate limiting configured
- [ ] Error handling tested
- [ ] Performance baseline measured

---

## Monitoring

### Application Logs

```bash
# Streamlit logs
tail -f ~/.streamlit/logs/streamlit.log

# Custom logging (add to app.py)
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Health Checks

```bash
# Ollama health
curl http://localhost:11434/api/tags

# Groq API health
curl -H "Authorization: Bearer $GROQ_API_KEY" \
     https://api.groq.com/openai/v1/models

# Application health
curl http://localhost:8501/health
```

### Performance Monitoring

```python
# Add to task execution
import time

start = time.time()
result = agent.process_audio_file(file)
duration = time.time() - start

logger.info(f"Processing took {duration:.2f}s")
```

---

## Scaling Strategies

### Horizontal Scaling
```yaml
# Load-balanced setup
- Multiple app instances (Streamlit)
- Shared session state (Redis/Database)
- Distributed Ollama (GPU cluster)
```

### Vertical Scaling
```yaml
# Single machine optimization
- GPU acceleration (CUDA/Metal)
- Larger models (Llama2-70b)
- Increased resources (CPU/RAM)
```

### Caching
```python
# Add Redis caching layer
import redis
cache = redis.Redis()

# Cache common classifications
cached = cache.get(f"intent:{text}")
if cached:
    return json.loads(cached)
```

---

## Troubleshooting Deployment

### "Port already in use"
```bash
# Find and kill process
lsof -i :8501
kill -9 <PID>
```

### "Ollama connection refused"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve &
```

### "Low memory"
```bash
# Use lightweight model
ollama pull neural-chat

# Configure quantization
# In code: load models with reduced precision
```

### "High latency"
```bash
# Profile bottleneck
time streamlit run app.py

# Check individual components
python examples.py --example intent
```

---

For more information, see `README.md` and `ARCHITECTURE.md`.
