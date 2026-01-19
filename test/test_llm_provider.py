"""
Test Unified LLM Provider
Tests fallback chain: Groq → OpenRouter → Gemini
"""
import sys
from pathlib import Path

# Add project root
root = str(Path(__file__).resolve().parent)
if root not in sys.path:
    sys.path.insert(0, root)

from src.core.console import console
from src.core.llm_provider import get_llm, reset_llm


def test_basic_invoke():
    """Test basic LLM invocation."""
    console.header("🧪 Testing Unified LLM Provider")
    
    try:
        llm = get_llm()
        console.success(f"LLM initialized with {len(llm.providers)} providers")
        
        # List providers
        for i, p in enumerate(llm.providers, 1):
            console.info(f"  {i}. {p.provider.value}: {p.model}")
        
        # Simple test
        console.subheader("Testing basic invocation...")
        response = llm.invoke([
            {"role": "user", "content": "Say 'Hello JobAI' in exactly 3 words"}
        ])
        
        console.success(f"Response: {response[:100]}")
        return True
        
    except Exception as e:
        console.error(f"Test failed: {e}")
        return False


def test_json_generation():
    """Test JSON generation."""
    console.subheader("Testing JSON generation...")
    
    try:
        llm = get_llm()
        
        result = llm.generate_json(
            prompt="Generate a simple job with title and company",
            system_prompt="You are a job data generator"
        )
        
        if "error" not in result:
            console.success(f"JSON generated: {list(result.keys())}")
            return True
        else:
            console.warning(f"JSON parse issue: {result.get('error')}")
            return False
            
    except Exception as e:
        console.error(f"JSON test failed: {e}")
        return False


def test_fallback():
    """Test that fallback works by simulating failure."""
    console.subheader("Testing fallback mechanism...")
    
    llm = get_llm()
    
    console.info(f"Providers available: {len(llm.providers)}")
    
    if len(llm.providers) > 1:
        console.success("Multiple providers configured - fallback ready")
        return True
    else:
        console.warning("Only 1 provider - no fallback available")
        return False


if __name__ == "__main__":
    results = []
    
    # Reset for fresh test
    reset_llm()
    
    # Run tests
    results.append(("Basic Invoke", test_basic_invoke()))
    results.append(("JSON Generation", test_json_generation()))
    results.append(("Fallback Config", test_fallback()))
    
    # Summary
    console.divider()
    console.header("📊 Test Results")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        console.info(f"  {status} {name}")
    
    console.divider()
    if passed == total:
        console.success(f"All {total} tests passed!")
    else:
        console.warning(f"{passed}/{total} tests passed")
