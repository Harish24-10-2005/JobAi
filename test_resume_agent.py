"""
Test script for Resume Agent - Verify Feature 1
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.agents.resume_agent import resume_agent
from src.models.profile import UserProfile
from src.models.job import JobAnalysis
import yaml


def load_profile() -> UserProfile:
    """Load user profile from YAML."""
    profile_path = Path(__file__).parent / "src/data/user_profile.yaml"
    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return UserProfile(**data)


async def test_resume_agent():
    """Test the Resume Deep Agent with Human-in-the-Loop."""
    print("=" * 60)
    print("🧪 Testing Resume Deep Agent")
    print("=" * 60)
    
    # Load profile
    profile = load_profile()
    print(f"✅ Loaded profile for: {profile.personal_information.full_name}")
    
    # Create a mock job analysis
    job_analysis = JobAnalysis(
        role="Senior Python Developer",
        company="TechCorp AI",
        salary="$150,000 - $180,000",
        tech_stack=["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "LangChain"],
        matching_skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        missing_skills=["AWS", "LangChain"],
        match_score=85,
        analysis="Strong match for the position with relevant Python and backend experience."
    )
    
    print(f"\n📋 Target Job: {job_analysis.role} at {job_analysis.company}")
    print(f"   Match Score: {job_analysis.match_score}%")
    print(f"   Tech Stack: {', '.join(job_analysis.tech_stack)}")
    print("=" * 60)
    
    # Run the resume agent with Human-in-the-Loop
    try:
        result = await resume_agent.tailor_resume(
            job_analysis=job_analysis,
            user_profile=profile,
            template_type="ats"
        )
        
        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
        else:
            print("\n" + "=" * 60)
            print("✅ RESUME TAILORING RESULT")
            print("=" * 60)
            print(f"ATS Score: {result.get('ats_score', 'N/A')}/100")
            print(f"Human Approved: {result.get('human_approved', False)}")
            
            tailored = result.get("tailored_content", {})
            if tailored.get("summary"):
                print(f"\nSummary:\n{tailored['summary'][:300]}...")
            
            if tailored.get("tailoring_notes"):
                print(f"\nChanges Made:\n{tailored['tailoring_notes']}")
            
            print("=" * 60)
            print("✅ Test completed successfully!")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_resume_agent())
