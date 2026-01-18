"""
Test Salary Negotiator Agent
"""
import asyncio
from src.agents.salary_agent import salary_agent, search_market_salary, calculate_counter_offer


async def test_salary_research():
    """Test salary market research."""
    print("=" * 60)
    print("💰 Testing Salary Agent - Research Mode")
    print("=" * 60)
    
    result = await salary_agent.research_salary(
        role="Senior Software Engineer",
        location="San Francisco, CA",
        experience_years=5
    )
    
    if result.get("success"):
        market = result.get("market_data", {})
        salary_range = market.get("salary_range", {})
        
        print("\n✅ Market Research Complete!")
        print(f"\n📊 Salary Range for Senior SWE in SF:")
        print(f"   25th percentile: ${salary_range.get('p25', 0):,}")
        print(f"   50th percentile: ${salary_range.get('p50', 0):,}")
        print(f"   75th percentile: ${salary_range.get('p75', 0):,}")
        print(f"   90th percentile: ${salary_range.get('p90', 0):,}")
        
        print(f"\n💡 Recommendation: {result.get('recommendation')}")
    else:
        print(f"\n❌ Failed: {result.get('error')}")
    
    return result


async def test_negotiation():
    """Test full negotiation flow."""
    print("\n" + "=" * 60)
    print("💰 Testing Salary Agent - Negotiation Mode")
    print("=" * 60)
    
    result = await salary_agent.negotiate_offer(
        role="Python Developer",
        location="Remote, USA",
        current_offer=120000,
        bonus=10000,
        equity=50000,
        experience_years=4,
        competing_offers=[125000]
    )
    
    if result.get("success"):
        counter = result.get("counter_offer", {})
        analysis = result.get("offer_analysis", {}).get("market_comparison", {})
        
        print("\n✅ Negotiation Analysis Complete!")
        print(f"\n📊 Your Offer Analysis:")
        print(f"   Current Offer: ${counter.get('current_offer', 0):,}")
        print(f"   Market Rating: {analysis.get('rating', 'Unknown')}")
        print(f"   Percentile: {analysis.get('percentile', 'Unknown')}")
        
        print(f"\n🎯 Counter-Offer Recommendation:")
        print(f"   Recommended Counter: ${counter.get('recommended_counter', 0):,}")
        print(f"   Increase: ${counter.get('increase_amount', 0):,} ({counter.get('increase_percentage', 0)}%)")
        print(f"   Strategy: {counter.get('strategy', 'Unknown')}")
        
        scripts = result.get("negotiation_scripts", {})
        if isinstance(scripts, dict) and "power_phrases" in scripts:
            print(f"\n💬 Power Phrases:")
            for phrase in scripts.get("power_phrases", [])[:2]:
                print(f"   • {phrase}")
    else:
        print(f"\n❌ Failed: {result.get('error')}")
    
    return result


def test_quick_counter():
    """Test quick counter calculation."""
    print("\n" + "=" * 60)
    print("💰 Testing Quick Counter Calculation")
    print("=" * 60)
    
    print("\n1. Testing search_market_salary...")
    market = search_market_salary(
        role="ML Engineer",
        location="New York, NY",
        experience_years=3
    )
    if "error" not in market:
        print(f"   ✅ Market data retrieved")
    
    print("\n2. Testing calculate_counter_offer...")
    counter = calculate_counter_offer(
        current_offer=150000,
        your_experience_years=5,
        competing_offers=[160000]
    )
    print(f"   ✅ Recommended counter: ${counter.get('recommended_counter', 0):,}")
    print(f"   ✅ Strategy: {counter.get('strategy')}")


if __name__ == "__main__":
    # Test individual tools
    test_quick_counter()
    
    # Test full agent
    asyncio.run(test_salary_research())
    asyncio.run(test_negotiation())
    
    print("\n" + "=" * 60)
    print("✅ Salary Agent Test Complete!")
    print("=" * 60)
