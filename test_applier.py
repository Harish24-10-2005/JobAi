"""
Test script for ApplierAgent - matches working agenttest.py pattern
"""
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = str(Path(__file__).resolve().parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.automators.applier import ApplierAgent
from src.models.profile import UserProfile
import yaml

def load_profile() -> UserProfile:
    profile_path = Path(__file__).parent / "src/data/user_profile.yaml"
    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return UserProfile(**data)

async def test_applier():
    # Test URL - same as your working test
    test_url = "https://docs.google.com/forms/d/e/1FAIpQLSeRMSLQPmKlk-jaj2Nz9YgC5tOj-kJ16Nc5JE07HbWD3vGe1g/viewform"
    
    print("=" * 60)
    print("🧪 Testing ApplierAgent")
    print("=" * 60)
    print(f"Target URL: {test_url}")
    print("=" * 60)
    
    # Load profile
    profile = load_profile()
    print(f"✅ Loaded profile for: {profile.personal_information.full_name}")
    
    # Initialize and run agent
    applier = ApplierAgent()
    
    try:
        result = await applier.run(test_url, profile)
        print(f"\n✅ Result: {result}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_applier())
