"""
Test Groq API keys - check which one works
"""
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from src.core.config import settings

def test_api_key(key_name: str, api_key: str):
    print(f"\nTesting {key_name}...")
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            api_key=api_key
        )
        result = llm.invoke([HumanMessage(content="Say 'Hello' in one word.")])
        print(f"  ✅ {key_name} works! Response: {result.content[:50]}")
        return True
    except Exception as e:
        error_str = str(e)
        if "rate_limit" in error_str.lower():
            print(f"  ⚠️ {key_name} rate limited")
        else:
            print(f"  ❌ {key_name} failed: {error_str[:100]}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Testing Groq API Keys")
    print("=" * 50)
    
    # Test primary key
    primary_works = test_api_key("GROQ_API_KEY (Primary)", 
                                  settings.groq_api_key.get_secret_value())
    
    # Test fallback key
    if settings.groq_api_key_fallback:
        fallback_works = test_api_key("GROQ_API_KEY1 (Fallback)", 
                                       settings.groq_api_key_fallback.get_secret_value())
    else:
        print("\n  ⚠️ No fallback key configured")
        fallback_works = False
    
    print("\n" + "=" * 50)
    if primary_works or fallback_works:
        print("✅ At least one API key is working!")
    else:
        print("❌ Both keys are rate limited. Try again later.")
    print("=" * 50)
