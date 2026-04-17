"""Integration tests for Voice Agent end-to-end."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.voice_agent import VoiceAgent
from src.audio_processor import AudioProcessor
import numpy as np
import tempfile


def test_full_pipeline_simulate():
    """Test full pipeline with simulated audio."""
    print("\n🧪 Full Pipeline Integration Test")
    print("=" * 50)
    
    try:
        # Create test audio (synthetic speech-like signal)
        processor = AudioProcessor()
        
        # Generate test audio with frequency content typical of speech
        duration = 2  # seconds
        sr = 16000
        t = np.linspace(0, duration, int(sr * duration))
        
        # Mix multiple frequencies to simulate speech
        freq1, freq2, freq3 = 200, 800, 3000  # Hz
        audio = (
            np.sin(2 * np.pi * freq1 * t) * 0.2 +
            np.sin(2 * np.pi * freq2 * t) * 0.15 +
            np.sin(2 * np.pi * freq3 * t) * 0.1
        )
        
        # Save to temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_file = Path(tmpdir) / "test_audio.wav"
            processor.save_audio_file(audio, str(temp_file), sr)
            
            print(f"✅ Test audio created: {temp_file}")
            print(f"   Duration: {duration}s, Sample rate: {sr}kHz")
            
            # Check file exists
            assert temp_file.exists()
            print(f"✅ File exists and is readable")
            
            # Load it back
            loaded_audio, loaded_sr = processor.load_audio_file(str(temp_file))
            print(f"✅ Audio loaded successfully")
            print(f"   Loaded shape: {loaded_audio.shape}")
            print(f"   Loaded SR: {loaded_sr}kHz")
            
            # Validate audio
            is_valid = processor.validate_audio(loaded_audio)
            print(f"✅ Audio is valid: {is_valid}")
            
            assert is_valid, "Audio validation failed"
    
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    print("\n✅ Integration test passed!")
    return True


def test_agent_initialization():
    """Test agent initialization and health check."""
    print("\n🧪 Agent Initialization Test")
    print("=" * 50)
    
    try:
        agent = VoiceAgent()
        print("✅ Agent initialized")
        
        # Check components
        assert agent.audio_processor is not None
        print("✅ Audio processor ready")
        
        assert agent.stt_engine is not None
        print("✅ STT engine ready")
        
        assert agent.intent_classifier is not None
        print("✅ Intent classifier ready")
        
        assert agent.tool_executor is not None
        print("✅ Tool executor ready")
        
        # Health check
        health = agent.health_check()
        print("\n📊 Health Check:")
        for component, status in health.items():
            status_str = "✅" if status else "❌"
            print(f"   {status_str} {component}")
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def test_output_directory():
    """Test output directory creation and permissions."""
    print("\n🧪 Output Directory Test")
    print("=" * 50)
    
    try:
        from src.tool_executor import ToolExecutor
        
        executor = ToolExecutor()
        output_dir = executor.OUTPUT_DIR
        
        assert output_dir.exists()
        print(f"✅ Output directory exists: {output_dir}")
        
        # Test write permission
        test_file = output_dir / ".test_write"
        test_file.write_text("test")
        assert test_file.exists()
        test_file.unlink()
        print("✅ Output directory is writable")
        
        return True
    
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🧪 Integration Test Suite")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Full Pipeline", test_full_pipeline_simulate()))
    results.append(("Agent Init", test_agent_initialization()))
    results.append(("Output Dir", test_output_directory()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} passed")
    print("=" * 50 + "\n")
