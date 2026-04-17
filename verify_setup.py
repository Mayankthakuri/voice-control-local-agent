"""Setup verification script."""

import sys
import os
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))


def check_dependencies():
    """Check if all required packages are installed."""
    print("\n📦 Checking Python Dependencies...")
    print("=" * 50)
    
    required = [
        "streamlit",
        "librosa",
        "soundfile",
        "numpy",
        "scipy",
        "requests",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def check_environment():
    """Check environment configuration."""
    print("\n🔧 Checking Environment Configuration...")
    print("=" * 50)
    
    groq_key = os.getenv("GROQ_API_KEY")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    if groq_key:
        print(f"✅ GROQ_API_KEY: Set (first 8 chars: {groq_key[:8]}...)")
    else:
        print(f"❌ GROQ_API_KEY: Not set")
        print("   Set with: export GROQ_API_KEY='your_key'")
    
    print(f"✅ OLLAMA_HOST: {ollama_host}")
    
    return bool(groq_key)


def check_ollama():
    """Check if Ollama is running."""
    print("\n🧠 Checking Ollama Connection...")
    print("=" * 50)
    
    try:
        import requests
        
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=2
        )
        
        if response.status_code == 200:
            print("✅ Ollama is running!")
            models = response.json().get("models", [])
            if models:
                print(f"\n   Available models:")
                for m in models:
                    print(f"   - {m.get('name')}")
            else:
                print("   ⚠️  No models installed")
                print("   Pull Mistral: ollama pull mistral")
            return True
        else:
            print("❌ Ollama not responding properly")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Ollama not running!")
        print("   Start with: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {str(e)}")
        return False


def check_groq_api():
    """Check if Groq API key is valid."""
    print("\n🌐 Checking Groq API...")
    print("=" * 50)
    
    import requests
    
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not groq_key:
        print("❌ GROQ_API_KEY not set")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {groq_key}"}
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Groq API key is valid!")
            return True
        else:
            print("❌ Groq API key is invalid!")
            print(f"   Response: {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print("⚠️  Timeout connecting to Groq API (network issue?)")
        return False
    except Exception as e:
        print(f"❌ Error checking Groq API: {str(e)}")
        return False


def check_output_dir():
    """Check if output directory exists and is writable."""
    print("\n📁 Checking Output Directory...")
    print("=" * 50)
    
    output_dir = Path(__file__).parent / "output"
    
    if output_dir.exists():
        print(f"✅ Output directory exists: {output_dir}")
    else:
        print(f"⚠️  Output directory doesn't exist: {output_dir}")
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created output directory")
        except Exception as e:
            print(f"❌ Failed to create output directory: {str(e)}")
            return False
    
    # Test write permission
    try:
        test_file = output_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Output directory is writable")
        return True
    except Exception as e:
        print(f"❌ Output directory is not writable: {str(e)}")
        return False


def main():
    """Run all checks."""
    print("\n" + "=" * 50)
    print("🚀 Voice Agent Setup Verification")
    print("=" * 50)
    
    all_good = True
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
    
    # Check environment
    if not check_environment():
        all_good = False
    
    # Check Ollama
    if not check_ollama():
        all_good = False
    
    # Check Groq API
    if not check_groq_api():
        all_good = False
    
    # Check output directory
    if not check_output_dir():
        all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("✅ All checks passed! Ready to run:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some checks failed. See above for details.")
    print("=" * 50 + "\n")
    
    return all_good


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
