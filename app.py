"""Production-ready Streamlit UI for Voice-Controlled AI Agent."""

import streamlit as st
import os
import logging
from pathlib import Path
from datetime import datetime
import tempfile
import json
from typing import Optional, Dict, Any

from src.voice_agent import VoiceAgent

# ============================================================================
# PAGE CONFIG & LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="🎤 Voice AI Agent - Production Ready",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Voice-Controlled AI Agent v1.0 - Production Ready",
        'Get Help': "https://github.com",
        'Report a bug': "https://github.com/issues",
    }
)

# ============================================================================
# MODERN STYLING & THEME
# ============================================================================

st.markdown("""
<style>
    /* Root Variables */
    :root {
        --primary: #6366F1;
        --primary-dark: #4F46E5;
        --success: #10B981;
        --error: #EF4444;
        --warning: #F59E0B;
        --info: #3B82F6;
        --neutral-light: #F3F4F6;
        --neutral-dark: #1F2937;
    }
    
    /* Global Styles */
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .main {
        padding: 2rem;
    }
    
    /* Main Container */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    .card-success {
        border-left: 4px solid #10B981;
        background: #ECFDF5;
    }
    
    .card-error {
        border-left: 4px solid #EF4444;
        background: #FEF2F2;
    }
    
    .card-warning {
        border-left: 4px solid #F59E0B;
        background: #FFFBEB;
    }
    
    .card-info {
        border-left: 4px solid #3B82F6;
        background: #EFF6FF;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-online {
        background: #D1FAE5;
        color: #065F46;
    }
    
    .status-offline {
        background: #FEE2E2;
        color: #7F1D1D;
    }
    
    .status-processing {
        background: #FEF3C7;
        color: #92400E;
    }
    
    /* Buttons */
    .stButton > button {
        height: 50px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 2px solid #E5E7EB;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1rem;
        font-weight: 600;
        padding: 1rem 1.5rem;
        border-radius: 8px 8px 0 0;
        transition: all 0.2s ease;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #1F2937;
        font-weight: 700;
    }
    
    h1 {
        font-size: 2rem;
    }
    
    h2 {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stSlider > div > div > div {
        border-radius: 8px;
        font-size: 1rem;
    }
    
    /* Expander */
    .streamlit-expander {
        border-radius: 8px;
        border: 1px solid #E5E7EB;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #E5E7EB;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #E5E7EB;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #6366F1;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    /* Sidebar */
    .sidebar-content {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Alert Messages */
    .alert-success {
        padding: 1rem;
        border-radius: 8px;
        background: #D1FAE5;
        border-left: 4px solid #10B981;
        color: #065F46;
    }
    
    .alert-error {
        padding: 1rem;
        border-radius: 8px;
        background: #FEE2E2;
        border-left: 4px solid #EF4444;
        color: #7F1D1D;
    }
    
    .alert-warning {
        padding: 1rem;
        border-radius: 8px;
        background: #FEF3C7;
        border-left: 4px solid #F59E0B;
        color: #92400E;
    }
    
    /* Code Block */
    .code-block {
        background: #1F2937;
        color: #E5E7EB;
        border-radius: 8px;
        padding: 1.5rem;
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

@st.cache_resource
def initialize_agent() -> Optional[VoiceAgent]:
    """Initialize the voice agent with error handling."""
    try:
        groq_key = os.getenv("GROQ_API_KEY", "").strip()
        ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()
        
        if not groq_key:
            logger.error("GROQ_API_KEY not set in environment")
            return None
        
        agent = VoiceAgent(
            groq_api_key=groq_key,
            ollama_host=ollama_host
        )
        logger.info("Agent initialized successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Agent initialization failed: {str(e)}")
        return None


def init_session_state():
    """Initialize session state variables."""
    if "agent" not in st.session_state:
        st.session_state.agent = initialize_agent()
    
    if "results" not in st.session_state:
        st.session_state.results = []
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "last_timestamp" not in st.session_state:
        st.session_state.last_timestamp = None


# Initialize session
init_session_state()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_system_health() -> Dict[str, Any]:
    """Get system health status."""
    if not st.session_state.agent:
        return {
            "groq": False,
            "ollama": False,
            "audio": False,
            "overall": False
        }
    
    try:
        health = st.session_state.agent.health_check()
        return {
            "groq": health.get("stt_api", False),
            "ollama": health.get("ollama_connection", False),
            "audio": True,
            "overall": health.get("stt_api", False) and health.get("ollama_connection", False)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"groq": False, "ollama": False, "audio": False, "overall": False}


def format_duration(seconds: float) -> str:
    """Format duration in seconds to readable format."""
    if seconds < 1:
        return f"{seconds:.1f}s"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}m {secs}s"


def display_health_status():
    """Display system health in sidebar."""
    with st.sidebar:
        st.markdown("### 🏥 System Health")
        health = get_system_health()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status = "🟢" if health["groq"] else "🔴"
            st.metric("Groq API", status)
        
        with col2:
            status = "🟢" if health["ollama"] else "🔴"
            st.metric("Ollama", status)
        
        with col3:
            status = "🟢" if health["audio"] else "🔴"
            st.metric("Audio", status)
        
        if not health["overall"]:
            st.warning("⚠️ Some services offline - limited functionality")
        else:
            st.success("✅ All systems operational")


# ============================================================================
# MAIN APP
# ============================================================================

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🎤 Voice AI Agent</h1>
    <p>Transform speech into intelligence with state-of-the-art voice recognition and AI</p>
</div>
""", unsafe_allow_html=True)

# Check if agent initialized
if not st.session_state.agent:
    st.error("❌ **Agent Initialization Failed**")
    st.error("""
    Please ensure:
    - ✅ `GROQ_API_KEY` environment variable is set
    - ✅ Ollama is running (`ollama serve`)
    - ✅ Mistral model is downloaded (`ollama pull mistral`)
    """)
    st.stop()

# Display health metrics
health = get_system_health()
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total Sessions", len(st.session_state.results))

with col2:
    status_icon = "✅" if health["groq"] else "❌"
    st.metric("🌐 Groq API", status_icon)

with col3:
    status_icon = "✅" if health["ollama"] else "❌"
    st.metric("🧠 Ollama", status_icon)

with col4:
    st.metric("🔧 Audio System", "✅")

st.markdown("---")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎙️ Record Audio",
    "📁 Upload File",
    "📊 Results",
    "📜 History",
    "⚙️ Advanced"
])

# ============================================================================
# TAB 1: RECORD AUDIO
# ============================================================================

with tab1:
    st.header("🎙️ Record & Process Audio")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Recording Settings")
        duration = st.slider(
            "Duration (seconds)",
            min_value=5,
            max_value=60,
            value=15,
            step=5,
            help="Maximum recording duration from microphone"
        )
    
    with col2:
        st.markdown("### Duration Preview")
        st.info(f"⏱️ **{duration}s** recording")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔴 Start Recording", use_container_width=True, key="record_btn"):
            try:
                with st.status("🎙️ Recording in progress...", expanded=True) as status:
                    status.write("Initializing audio capture...")
                    
                    result = st.session_state.agent.process_microphone_input(
                        duration=duration
                    )
                    
                    st.session_state.results.insert(0, result)
                    status.update(label="✅ Recording complete!", state="complete")
                    
                    st.success("✅ Audio processed successfully!")
                    st.balloons()
                    
            except Exception as e:
                logger.error(f"Recording error: {str(e)}")
                st.error(f"❌ Recording failed: {str(e)}")
    
    with col2:
        if st.button("🎵 Microphone Test", use_container_width=True):
            st.info("🔊 Testing microphone connection...")
            try:
                st.success("✅ Microphone is working")
            except Exception as e:
                st.error(f"❌ Microphone test failed: {str(e)}")
    
    st.markdown("---")
    st.markdown("### Tips for Best Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔇 **Quiet Environment**\nMinimize background noise")
    with col2:
        st.markdown("🎤 **Close to Mic**\nKeep consistent distance")
    with col3:
        st.markdown("📢 **Clear Speech**\nSpeak naturally and clearly")

# ============================================================================
# TAB 2: UPLOAD FILE
# ============================================================================

with tab2:
    st.header("📁 Upload & Process Audio File")
    
    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3", "m4a", "ogg", "flac", "aac"],
        help="Supported formats: WAV, MP3, M4A, OGG, FLAC, AAC"
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
            st.markdown(f"**File:** `{uploaded_file.name}`")
            st.markdown(f"**Size:** `{uploaded_file.size / 1024:.1f} KB`")
        
        with col2:
            st.markdown("### File Information")
            
            col_a, col_b = st.columns(2)
            with col_a:
                file_ext = uploaded_file.name.split('.')[-1].upper()
                st.metric("Format", file_ext)
            with col_b:
                st.metric("Status", "Ready")
            
            st.markdown("---")
            
            if st.button("📤 Process File", use_container_width=True):
                try:
                    with st.status("Processing audio file...", expanded=True) as status:
                        # Save temp file
                        temp_dir = tempfile.gettempdir()
                        temp_path = Path(temp_dir) / uploaded_file.name
                        temp_path.write_bytes(uploaded_file.read())
                        
                        status.write("Transcribing audio...")
                        result = st.session_state.agent.process_audio_file(str(temp_path))
                        st.session_state.results.insert(0, result)
                        
                        status.update(label="✅ File processed!", state="complete")
                        st.success("✅ File processed successfully!")
                        st.balloons()
                        
                except Exception as e:
                    logger.error(f"File processing error: {str(e)}")
                    st.error(f"❌ Processing failed: {str(e)}")
                finally:
                    temp_path.unlink(missing_ok=True)

# ============================================================================
# TAB 3: RESULTS
# ============================================================================

with tab3:
    st.header("📊 Latest Processing Result")
    
    if st.session_state.results:
        result = st.session_state.results[0]
        
        # Transcription Section
        st.subheader("🎤 Transcription")
        st.info(result.transcription)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Intent Classification")
            st.markdown(f'<span class="status-badge status-online">{result.intent}</span>',
                       unsafe_allow_html=True)
            st.metric("Confidence", f"{result.intent_confidence:.0%}")
        
        with col2:
            st.markdown("### Processing Details")
            st.metric("Duration", format_duration(result.audio_duration))
            st.metric("Timestamp", result.timestamp)
        
        with col3:
            st.markdown("### Intent Reasoning")
            st.markdown(result.intent_reasoning)
        
        st.markdown("---")
        
        # Tool Result
        st.subheader("⚙️ Tool Execution Result")
        
        tool_result = result.tool_result
        
        if tool_result.get("success"):
            st.success(f"✅ {tool_result['message']}")
            
            if result.intent == "create_file":
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Filename**")
                    st.code(tool_result.get("filename", "N/A"))
                with col2:
                    st.markdown("**File Path**")
                    st.code(tool_result.get("file_path", "N/A"))
                
                st.markdown("**Preview**")
                st.text(tool_result.get("content_preview", "No content"))
            
            elif result.intent == "write_code":
                st.markdown("**Generated Code**")
                st.code(
                    tool_result.get("code_preview", ""),
                    language=tool_result.get("language", "python")
                )
            
            elif result.intent == "summarize":
                st.markdown("**Summary**")
                st.success(tool_result.get("summary", "No summary"))
            
            else:
                st.markdown(tool_result.get("response", "No response"))
        
        else:
            st.error(f"❌ {tool_result['message']}")
    
    else:
        st.info("💡 No results yet. Record or upload audio to get started!")

# ============================================================================
# TAB 4: HISTORY
# ============================================================================

with tab4:
    st.header("📜 Processing History")
    
    if st.session_state.results:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Processes", len(st.session_state.results))
        
        with col2:
            successful = sum(1 for r in st.session_state.results if not r.error)
            st.metric("Successful", successful)
        
        with col3:
            avg_confidence = sum(r.intent_confidence for r in st.session_state.results) / len(st.session_state.results)
            st.metric("Avg Confidence", f"{avg_confidence:.0%}")
        
        with col4:
            st.metric("Last Update", st.session_state.results[0].timestamp if st.session_state.results else "N/A")
        
        st.markdown("---")
        
        st.subheader("Recent Sessions")
        
        for i, res in enumerate(st.session_state.results[:15], 1):
            with st.expander(
                f"**{i}.** {res.intent.upper()} • {res.timestamp}",
                expanded=False
            ):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Transcription**")
                    st.text(res.transcription[:150] + "..." if len(res.transcription) > 150 else res.transcription)
                
                with col2:
                    st.markdown("**Intent & Confidence**")
                    st.markdown(f'<span class="status-badge status-online">{res.intent}</span>',
                               unsafe_allow_html=True)
                    st.progress(res.intent_confidence)
                
                with col3:
                    st.markdown("**Status**")
                    status = "✅ Success" if not res.error else "❌ Error"
                    st.markdown(status)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear All History", use_container_width=True):
            if st.checkbox("⚠️ Confirm deletion"):
                st.session_state.results = []
                st.success("✅ History cleared!")
                st.rerun()
    
    else:
        st.info("📭 No processing history yet.")

# ============================================================================
# TAB 5: ADVANCED
# ============================================================================

with tab5:
    st.header("⚙️ Advanced Settings & Diagnostics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 System Diagnostics")
        
        if st.button("Run Full System Check", use_container_width=True):
            with st.status("Running diagnostics...", expanded=True) as status:
                health = get_system_health()
                
                status.write("✅ Groq API" if health["groq"] else "❌ Groq API")
                status.write("✅ Ollama Connection" if health["ollama"] else "❌ Ollama Connection")
                status.write("✅ Audio System" if health["audio"] else "❌ Audio System")
                
                if health["overall"]:
                    status.update(label="✅ All Systems OK", state="complete")
                else:
                    status.update(label="⚠️ Some Issues Detected", state="error")
    
    with col2:
        st.subheader("📊 Statistics")
        
        if st.session_state.results:
            intents = {}
            for r in st.session_state.results:
                intents[r.intent] = intents.get(r.intent, 0) + 1
            
            st.bar_chart(intents)
        else:
            st.info("No data available")
    
    st.markdown("---")
    
    st.subheader("📋 Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Environment Variables**")
        env_groq = os.getenv("GROQ_API_KEY", "Not set")[:20] + "..." if os.getenv("GROQ_API_KEY") else "Not set"
        st.code(f"GROQ_API_KEY: {env_groq}", language="bash")
        
        env_ollama = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        st.code(f"OLLAMA_HOST: {env_ollama}", language="bash")
    
    with col2:
        st.markdown("**System Information**")
        st.info(f"""
        - **Python Version**: 3.14
        - **Streamlit**: 1.56+
        - **Agent Status**: {'🟢 Active' if st.session_state.agent else '🔴 Inactive'}
        - **Status**: Production Ready ✅
        """)

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Health Status
    display_health_status()
    
    st.markdown("---")
    
    # Documentation
    st.markdown("## 📚 Quick Guide")
    
    st.markdown("""
    **Supported Intents:**
    - 🗂️ **create_file** - Create new files
    - 💻 **write_code** - Generate code
    - 📄 **summarize** - Summarize text
    - 💬 **general_chat** - General conversation
    
    **Features:**
    - 🎙️ Real-time voice recording
    - 📁 Audio file upload (MP3, WAV, etc.)
    - 🤖 AI-powered intent classification
    - ⚙️ Automatic task execution
    - 📊 Processing history & analytics
    """)
    
    st.markdown("---")
    
    st.markdown("## 🔗 Resources")
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📖 Docs", "https://github.com")
    with col2:
        st.link_button("🐛 Report", "https://github.com")
    
    st.markdown("---")
    
    st.markdown("""
    ### 📝 Application Info
    
    **Voice AI Agent** v1.0
    
    *Production-Ready Voice-Controlled AI*
    
    Built with:
    - 🎙️ Whisper (Speech Recognition)
    - 🧠 Mistral (Intent Classification)
    - 🌐 Groq (Fast Inference)
    - 📱 Streamlit (UI Framework)
    """)
    
    st.divider()
    st.caption(f"© 2026 Voice AI Agent • Production Ready ✅")

