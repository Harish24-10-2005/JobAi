"""
Test Job Tracker Agent
"""
import asyncio
from src.agents.tracker_agent import (
    job_tracker_agent,
    add_job_application,
    update_application_status,
    get_applications_by_status,
    generate_tracker_report
)


async def test_add_applications():
    """Test adding job applications."""
    print("=" * 60)
    print("📝 Testing Job Tracker - Add Applications")
    print("=" * 60)
    
    # Add test applications
    apps = [
        {"company": "Google", "role": "Senior SWE", "priority": "High", "salary_range": "$150k-180k"},
        {"company": "Meta", "role": "Data Engineer", "priority": "High", "salary_range": "$140k-170k"},
        {"company": "Amazon", "role": "SDE II", "priority": "Medium", "salary_range": "$130k-160k"},
    ]
    
    for app in apps:
        result = add_job_application(**app)
        print(f"✅ Added: {app['role']} at {app['company']}")
    
    return True


async def test_update_status():
    """Test updating application status."""
    print("\n" + "=" * 60)
    print("🔄 Testing Status Update")
    print("=" * 60)
    
    result = update_application_status(
        company="Google",
        new_status="Interview",
        next_step="Technical phone screen on Monday"
    )
    
    if result.get("success"):
        print(f"✅ Updated: {result.get('message')}")
    else:
        print(f"⚠️ Update issue: {result.get('message')}")
    
    return result


async def test_get_report():
    """Test generating report."""
    print("\n" + "=" * 60)
    print("📊 Testing Report Generation")
    print("=" * 60)
    
    report = generate_tracker_report()
    
    summary = report.get("summary", {})
    print(f"\n📈 Total Applications: {summary.get('total_applications', 0)}")
    print(f"📊 Response Rate: {summary.get('response_rate', '0%')}")
    
    by_status = report.get("by_status", {})
    print("\n📋 By Status:")
    for status, count in by_status.items():
        print(f"   {status}: {count}")
    
    recs = report.get("recommendations", [])
    if recs:
        print("\n💡 Recommendations:")
        for rec in recs:
            print(f"   • {rec}")
    
    return report


async def test_full_flow():
    """Test complete tracker flow."""
    
    # Add applications
    await test_add_applications()
    
    # Update status
    await test_update_status()
    
    # Get report
    await test_get_report()
    
    print("\n" + "=" * 60)
    print("✅ Job Tracker Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_full_flow())
