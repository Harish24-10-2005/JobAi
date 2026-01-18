"""
Test Company Research Agent
"""
import asyncio
from src.agents.company_agent import (
    company_agent, 
    search_company_info, 
    analyze_company_culture,
    identify_red_flags
)


async def test_full_research():
    """Test complete company research."""
    print("=" * 60)
    print("🏢 Testing Company Research Agent")
    print("=" * 60)
    
    result = await company_agent.research_company(
        company="Google",
        role="Senior Software Engineer"
    )
    
    if result.get("success"):
        print("\n✅ Company research complete!")
        
        # Company info
        info = result.get("company_info", {})
        print(f"\n📊 Company: {info.get('company_name', 'Unknown')}")
        print(f"   Industry: {info.get('industry', 'Unknown')}")
        print(f"   Size: {info.get('size', 'Unknown')}")
        
        # Culture
        culture = result.get("culture_analysis", {})
        print(f"\n🎭 Culture Type: {culture.get('culture_type', 'Unknown')}")
        wlb = culture.get("work_life_balance", {})
        print(f"   Work-Life Balance: {wlb.get('rating', 'Unknown')}")
        
        # Red flags
        flags = result.get("red_flags", {})
        print(f"\n⚠️  Risk Level: {flags.get('overall_risk_level', 'Unknown')}")
        
        # Interview insights
        insights = result.get("interview_insights", {})
        process = insights.get("interview_process", {})
        print(f"\n🎯 Interview Difficulty: {process.get('difficulty', 'Unknown')}")
    else:
        print(f"\n❌ Failed: {result.get('error')}")
    
    return result


def test_individual_tools():
    """Test individual tools."""
    print("\n" + "=" * 60)
    print("🔧 Testing Individual Tools")
    print("=" * 60)
    
    # Test search_company_info
    print("\n1. Testing search_company_info...")
    info = search_company_info("Microsoft", "Data Engineer")
    if "error" not in info:
        print(f"   ✅ Found: {info.get('industry', 'N/A')} company")
    else:
        print(f"   ⚠️ Error: {info.get('error')[:50]}")
    
    # Test analyze_company_culture
    print("\n2. Testing analyze_company_culture...")
    culture = analyze_company_culture("Netflix")
    if "error" not in culture:
        print(f"   ✅ Culture: {culture.get('culture_type', 'N/A')}")
    else:
        print(f"   ⚠️ Error: {culture.get('error')[:50]}")
    
    # Test identify_red_flags
    print("\n3. Testing identify_red_flags...")
    flags = identify_red_flags("Startup XYZ", "Fast-paced environment, wear many hats")
    if "error" not in flags:
        print(f"   ✅ Risk Level: {flags.get('overall_risk_level', 'N/A')}")
    else:
        print(f"   ⚠️ Error: {flags.get('error')[:50]}")


async def test_quick_check():
    """Test quick company check."""
    print("\n" + "=" * 60)
    print("🏢 Testing Quick Check")
    print("=" * 60)
    
    result = await company_agent.quick_check("Amazon")
    
    print(f"\n📊 Company: {result.get('company', 'Unknown')}")
    print(f"⚠️  Risk Level: {result.get('risk_level', 'Unknown')}")
    print(f"🔍 Key Concerns: {len(result.get('key_concerns', []))} found")


if __name__ == "__main__":
    # Test individual tools first
    test_individual_tools()
    
    # Test quick check
    asyncio.run(test_quick_check())
    
    # Full research (may hit rate limits)
    # asyncio.run(test_full_research())
    
    print("\n" + "=" * 60)
    print("✅ Company Agent Test Complete!")
    print("=" * 60)
