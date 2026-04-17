# 🏗️ Architecture Documentation

## System Overview

The Voice-Controlled AI Agent follows a modular, pipeline-based architecture where each component has a single responsibility:

```
User (Voice/Audio) 
    ↓
[Audio Input Layer]
    ↓
[STT Layer]
    ↓
[Intent Layer]
    ↓
[Action Layer]
    ↓
[Output Layer]
    ↓
User (Results Display)
```

## Component Deep Dive

### 1. Audio Input Layer (`audio_processor.py`)

**Responsibility**: Capture and validate audio input

```python
class AudioProcessor:
    - record_audio(duration) → audio_data, sample_rate
    - load_audio_file(path) → audio_data, sample_rate
    - save_audio_file(data, path, sr) → None
    - validate_audio(data) → bool
```

**Key Features**:
- **Microphone Input**: Uses `sounddevice` for real-time recording
- **File Input**: Uses `librosa` to load multiple audio formats
- **Validation**: RMS energy check to detect silence/noise
- **Error Handling**: Graceful fallbacks for missing dependencies

**Design Choices**:
- 16kHz sample rate (optimal for speech)
- Float32 audio (librosa standard)
- Mono channel (STT doesn't need stereo)

**Data Flow**:
```
Raw Audio (microphone/file)
    ↓ [librosa.load or sounddevice.rec]
    ↓
Normalized NumPy Array [shape: (n_samples,)]
    ↓ [Validation: check RMS energy > 1e-6]
    ↓
Valid Audio Samples ✓
```

### 2. Speech-to-Text Layer (`stt_engine.py`)

**Responsibility**: Convert audio to text

```python
class STTEngine:
    - transcribe(audio_path) → str
    - validate_api_key() → bool
```

**Implementation**: Groq API with Whisper-Large-v3-Turbo

**Why Groq?**
- Free tier available (25 requests/day planning to increase)
- Ultra-fast (2-5 sec for 10 sec audio)
- High accuracy
- No local resource requirements
- Supports many languages

**API Call Flow**:
```
Audio File (WAV format)
    ↓ [POST to api.groq.com/openai/v1/audio/transcriptions]
    ↓ [Headers: Authorization Bearer <API_KEY>]
    ↓
Groq Whisper Model
    ↓
Text Response (JSON)
    ↓
User Transcription ✓
```

**Error Handling**:
- ConnectionError: Network issue
- Timeout: API slow or offline
- Invalid API key: Auth failure
- Empty response: Transcription failed

### 3. Intent Classification Layer (`intent_classifier.py`)

**Responsibility**: Understand user intent from text

```python
class IntentClassifier:
    - classify(text) → {intent, confidence, reasoning}
    - check_ollama_connection() → bool
```

**Implementation**: Ollama + Mistral (Local LLM)

**Why Local LLM?**
- No external API calls (better privacy)
- Fast inference (~1-2 sec)
- No API key needed
- Customizable model selection

**Intent Categories**:
1. **create_file**: "Create a config file", "Make a settings.json"
2. **write_code**: "Generate a retry function", "Write Python for API call"
3. **summarize**: "Summarize the following", "Compress this text"
4. **general_chat**: Everything else

**Classification Flow**:
```
Transcribed Text
    ↓
[Prompt Engineering]
    "You are an intent classifier..."
    ↓
Ollama API (local)
    ↓
Mistral Model Inference
    ↓
JSON Response: {intent, confidence, reasoning}
    ↓
Validated Intent ✓
```

**Fallback Strategy**:
1. Try LLM classification
2. If parsing fails → Heuristic classification
3. If still ambiguous → Default to "general_chat"

**Heuristic Keywords**:
- **create_file**: "create", "make", "new file", "mkdir"
- **write_code**: "write", "code", "function", "class", "def", "python"
- **summarize**: "summarize", "summary", "sum up", "brief"

### 4. Tool Execution Layer (`tool_executor.py`)

**Responsibility**: Execute actions based on intent

```python
class ToolExecutor:
    - execute(intent, text, context) → result
    - _create_file_tool(request) → result
    - _write_code_tool(request) → result
    - _summarize_tool(input, context) → result
    - _general_chat_tool(input) → result
```

**Tool Implementation**:

#### Tool 1: Create File
```
User Request: "Create a config file"
    ↓
LLM Prompt: "Extract filename and content"
    ↓
LLM Response: {"filename": "config.json", "content": "..."}
    ↓
Sanitize Filename
    ↓
Create File in output/
    ↓
Return: {success, file_path, preview}
```

#### Tool 2: Write Code
```
User Request: "Generate a retry function"
    ↓
LLM Prompt: "Generate complete, documented code"
    ↓
LLM Response: {"code": "def retry(...)", "filename": "retry.py"}
    ↓
Detect Language from Extension
    ↓
Save to output/
    ↓
Return: {success, file_path, code_preview, language}
```

#### Tool 3: Summarize
```
User Input: "Long text..."
    ↓
LLM Prompt: "Summarize in 2-3 sentences"
    ↓
LLM Response: "Summary..."
    ↓
Return: {success, summary, length_stats}
```

#### Tool 4: General Chat
```
User Query: "How to use Python?"
    ↓
Pass to LLM as-is
    ↓
LLM Response: "Python is..."
    ↓
Return: {success, response}
```

**Safety Measures**:
- All file operations confined to `output/` folder
- Filename sanitization (remove dangerous chars)
- Max filename length: 255 chars
- No code execution (just generation)

### 5. Orchestrator (`voice_agent.py`)

**Responsibility**: Coordinate all components

```python
class VoiceAgent:
    - process_audio_file(path) → AgentResult
    - process_microphone_input(duration) → AgentResult
    - health_check() → {stt_api, ollama, audio_processor}
    - get_history() → [AgentResult]
```

**Data Structure**:
```python
@dataclass
class AgentResult:
    timestamp: str
    audio_duration: float
    transcription: str
    intent: str
    intent_confidence: float
    intent_reasoning: str
    tool_result: Dict
    error: Optional[str]
```

**Pipeline Execution**:
```python
def process_audio_file(path):
    1. Load audio
    2. Validate quality
    3. Transcribe (STT)
    4. Classify intent
    5. Execute tool
    6. Package result
    7. Add to history
    return AgentResult
```

**Error Recovery**:
- Silent audio → Return graceful error
- STT failure → Return partial result
- LLM timeout → Use heuristic classification
- Tool failure → Return error in result object

### 6. UI Layer (`app.py`)

**Framework**: Streamlit (reactive, low-maintenance)

**Key Pages**:

#### Tab 1: 🎙️ Input
- Microphone recorder
- File uploader
- Live progress indicators

#### Tab 2: 📊 Results
- Pipeline visualization
- Transcription display
- Intent + confidence
- Tool output
- Export option

#### Tab 3: 📜 History
- Execution timeline
- Statistics dashboard
- Detailed view per execution

**State Management**:
```python
st.session_state:
    .agent → VoiceAgent instance
    .current_result → Latest AgentResult
    .results → All results list
    .initialized → Setup success flag
```

## Data Flow Diagrams

### Complete Pipeline
```
┌─────────────────────────────────┐
│     Audio Input                 │
│ (Microphone or File)            │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   AudioProcessor                │
│   - Load/Record Audio           │
│   - Validate Quality            │
│   - Return 16kHz PCM            │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   STTEngine (Groq)              │
│   - Whisper-Large-v3-Turbo      │
│   - Audio → Text                │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   IntentClassifier (Ollama)     │
│   - Mistral Model               │
│   - Text → Intent + Confidence  │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   ToolExecutor                  │
│   - Route by Intent             │
│   - Execute Tool                │
│   - Generate Output             │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   VoiceAgent (Orchestrator)     │
│   - Package AgentResult         │
│   - Update History              │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   Streamlit UI                  │
│   - Display Results             │
│   - Show History                │
│   - Accept Next Input           │
└─────────────────────────────────┘
```

### Error Handling Flow
```
Input Audio
    ↓
[Validation Failed?] → Return Error + Guidance
    ↓ No
[STT Failed?] → Return Error + Retry UI
    ↓ No
[LLM Timeout?] → Use Heuristic (Fallback)
    ↓ 
[Tool Failed?] → Return Error Message in Result
    ↓ No
Success → Return Complete Result
```

## Performance Characteristics

| Stage | Latency | Bottleneck | Optimization |
|-------|---------|-----------|--------------|
| Audio Recording | Synchronous | User speech | N/A |
| STT (Groq) | 2-5 sec | API latency | Already optimized |
| Intent (Ollama) | 1-2 sec | Model inference | GPU acceleration available |
| Tool Execute | <1 sec | LLM generation | Parallelizable |
| **Total E2E** | **~15-20 sec** | Audio length | Already optimal |

## Scalability Considerations

### Horizontal Scaling
```
Multiple Ollama instances behind load balancer
Multiple Streamlit instances with shared state (database/Redis)
```

### Vertical Scaling
```
GPU acceleration for Ollama (CUDA/Metal)
Larger LLM models (Llama2-70b, Mixtral)
```

### Resource Requirements
- Minimum: 2GB RAM, 2 CPU cores
- Recommended: 8GB RAM, 4 CPU cores, GPU optional
- Ollama footprint: ~3-10GB (depending on model)

## Security Considerations

### Input Validation
- ✅ Filename sanitization
- ✅ Audio format validation
- ✅ Text length limits (prevent prompt injection)

### Secret Management
- ✅ API keys in .env (not in code)
- ✅ No logging of API keys

### File Operations
- ✅ Strict confinement to output/ folder
- ✅ No symlink following
- ✅ No code execution (only generation)

## Future Enhancements

1. **Multi-language Support**
   - Add language detection
   - Support multiple Ollama models per language

2. **Advanced Intent Training**
   - Fine-tune LLM on custom intents
   - User feedback loop

3. **Tool Expansion**
   - Database queries
   - API calls
   - File analysis

4. **Performance**
   - GPU acceleration
   - Model quantization
   - Caching layer

5. **Observability**
   - Detailed logging
   - Metrics collection
   - Performance tracking

---

**For more details, see**: `README.md` (usage), `DEPLOYMENT.md` (production setup)
