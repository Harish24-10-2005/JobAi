"""
Quick test to verify database persistence works
"""
import sys
from pathlib import Path

root = str(Path(__file__).resolve().parent)
if root not in sys.path:
    sys.path.insert(0, root)

from src.services.db_service import db_service
from src.core.console import console


def test_db_persistence():
    """Test saving data to Supabase."""
    console.header("🧪 Testing Database Persistence")
    
    # Test 1: Save a job
    console.subheader("Test 1: Save discovered job")
    job_id = db_service.save_discovered_job(
        url="https://test.greenhouse.io/jobs/12345",
        title="Test Engineer",
        company="Test Corp",
        location="Remote"
    )
    if job_id:
        console.success(f"Job saved: {job_id}")
    else:
        console.error("Failed to save job")
        return False
    
    # Test 2: Save analysis
    console.subheader("Test 2: Save job analysis")
    analysis_id = db_service.save_job_analysis(
        job_id=job_id,
        role="Test Engineer",
        company="Test Corp",
        match_score=85,
        tech_stack=["Python", "SQL"],
        matching_skills=["Python", "Testing"],
        missing_skills=["Kubernetes"],
        reasoning="Good fit for testing role"
    )
    if analysis_id:
        console.success(f"Analysis saved: {analysis_id}")
    else:
        console.error("Failed to save analysis")
    
    # Test 3: Save application
    console.subheader("Test 3: Save application")
    app_id = db_service.save_application(
        job_id=job_id,
        analysis_id=analysis_id,
        status="pending"
    )
    if app_id:
        console.success(f"Application saved: {app_id}")
    else:
        console.error("Failed to save application")
    
    # Test 4: Get summary
    console.subheader("Test 4: Get applications summary")
    summary = db_service.get_applications_summary()
    console.info(f"Total applications: {summary.get('total', 0)}")
    console.info(f"By status: {summary.get('by_status', {})}")
    
    console.divider()
    console.success("Database persistence tests complete!")
    return True


if __name__ == "__main__":
    test_db_persistence()
