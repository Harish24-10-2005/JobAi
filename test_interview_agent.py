"""
Test Interview Prep Agent
"""
import asyncio
import json
from src.agents.interview_agent import interview_agent, analyze_job_requirements, generate_behavioral_questions


async def test_quick_prep():
    """Test quick interview prep without full profile."""
    print("=" * 60)
    print("🎯 Testing Interview Prep Agent - Quick Mode")
    print("=" * 60)
    
    result = await interview_agent.quick_prep(
        role="Senior Python Developer",
        company="Google",
        tech_stack=["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "Kubernetes"]
    )
    
    if result.get("success"):
        print("\n✅ Quick prep successful!")
        print(f"\n📊 Analysis: Senior Role = {result['analysis'].get('is_senior_role')}")
        print(f"   Interview Rounds: {', '.join(result['analysis'].get('interview_rounds', []))}")
        
        # Show some behavioral questions
        behavioral = result.get("behavioral_questions", {})
        questions = behavioral.get("questions", [])
        if questions:
            print(f"\n📝 Sample Behavioral Questions ({len(questions)} total):")
            for i, q in enumerate(questions[:3], 1):
                print(f"   {i}. {q.get('question', str(q))[:80]}...")
        
        # Show some technical questions
        technical = result.get("technical_questions", {})
        tech_qs = technical.get("technical_questions", [])
        if tech_qs:
            print(f"\n💻 Sample Technical Questions ({len(tech_qs)} total):")
            for i, q in enumerate(tech_qs[:3], 1):
                print(f"   {i}. [{q.get('category', 'general')}] {q.get('question', str(q))[:60]}...")
    else:
        print(f"\n❌ Failed: {result.get('error')}")
    
    return result


def test_individual_tools():
    """Test individual tools."""
    print("\n" + "=" * 60)
    print("🔧 Testing Individual Tools")
    print("=" * 60)
    
    # Test analyze_job_requirements
    print("\n1. Testing analyze_job_requirements...")
    analysis = analyze_job_requirements(
        role="Data Engineer",
        company="Netflix",
        tech_stack=["Python", "Spark", "Kafka", "AWS", "SQL"],
        job_description="Build data pipelines..."
    )
    print(f"   ✅ Senior role: {analysis.get('is_senior_role')}")
    print(f"   ✅ Tech focus: {analysis.get('technical_focus')}")
    
    # Test generate_behavioral_questions
    print("\n2. Testing generate_behavioral_questions...")
    questions_json = generate_behavioral_questions(
        role="Data Engineer",
        company="Netflix",
        is_senior=False,
        focus_areas=["Teamwork", "Problem Solving"]
    )
    
    questions = json.loads(questions_json)
    if "error" not in questions:
        print(f"   ✅ Generated {len(questions.get('questions', []))} questions")
    else:
        print(f"   ⚠️ Error: {questions.get('error')[:50]}")


if __name__ == "__main__":
    # Test individual tools first
    test_individual_tools()
    
    # Then test full agent
    asyncio.run(test_quick_prep())
    
    print("\n" + "=" * 60)
    print("✅ Interview Agent Test Complete!")
    print("=" * 60)
