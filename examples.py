"""Quick start examples for Voice Agent."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src.voice_agent import VoiceAgent
from src.intent_classifier import IntentClassifier


def example_basic_pipeline():
    """Example: Complete pipeline with an audio file."""
    print("\n🎤 Voice Agent - Basic Pipeline Example")
    print("=" * 50)
    
    try:
        # Initialize agent
        agent = VoiceAgent()
        print("✅ Agent initialized successfully")
        
        # Check health
        health = agent.health_check()
        print(f"\n📊 System Health:")
        print(f"   STT API: {'✅' if health['stt_api'] else '❌'}")
        print(f"   Ollama: {'✅' if health['ollama_connection'] else '❌'}")
        print(f"   Audio: {'✅' if health['audio_processor'] else '❌'}")
        
        if not health['stt_api']:
            print("\n⚠️  STT API not available. Set GROQ_API_KEY environment variable.")
            print("   Export: export GROQ_API_KEY='your_key_here'")
        
        if not health['ollama_connection']:
            print("\n⚠️  Ollama not running. Start it with:")
            print("   ollama serve")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_intent_classification():
    """Example: Test intent classification."""
    print("\n🎯 Intent Classification Examples")
    print("=" * 50)
    
    try:
        classifier = IntentClassifier()
        
        test_inputs = [
            "Create a new Python file",
            "Write a function that validates email addresses",
            "Summarize the following article about machine learning basics",
            "What is the capital of France?"
        ]
        
        for text in test_inputs:
            print(f"\n📝 Input: \"{text}\"")
            result = classifier.classify(text)
            print(f"   Intent: {result['intent']}")
            print(f"   Confidence: {result['confidence']:.0%}")
            print(f"   Reasoning: {result['reasoning']}")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nNote: Ollama server must be running (ollama serve)")


def example_microphone_demo():
    """Example: Record from microphone and process."""
    print("\n🎙️ Microphone Input Example")
    print("=" * 50)
    
    try:
        import sounddevice
        agent = VoiceAgent()
        
        print("\n💡 This will record 5 seconds of audio from your microphone.")
        print("   Make sure to speak clearly!")
        
        input("Press Enter to start recording...")
        
        result = agent.process_microphone_input(duration=5)
        
        print(f"\n✅ Processing complete!")
        print(f"\n📝 Transcription: {result.transcription}")
        print(f"🎯 Intent: {result.intent}")
        print(f"📊 Confidence: {result.intent_confidence:.0%}")
        print(f"\n⚙️ Tool Result:")
        print(f"   Success: {result.tool_result.get('success')}")
        print(f"   Message: {result.tool_result.get('message')}")
        
        if result.error:
            print(f"\n⚠️ Error: {result.error}")
    
    except ImportError:
        print("❌ sounddevice not installed. Install with:")
        print("   pip install sounddevice")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Voice Agent Examples")
    parser.add_argument(
        "--example",
        choices=["health", "intent", "microphone"],
        default="health",
        help="Which example to run"
    )
    
    args = parser.parse_args()
    
    if args.example == "health":
        example_basic_pipeline()
    elif args.example == "intent":
        example_intent_classification()
    elif args.example == "microphone":
        example_microphone_demo()
