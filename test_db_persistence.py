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
        url="https://test2.greenhouse.io/jobs/67890",
        title="Senior Developer",
        company="Acme Corp",
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
        role="Senior Developer",
        company="Acme Corp",
        match_score=90,
        tech_stack=["Python", "Django", "PostgreSQL"],
        matching_skills=["Python", "Backend"],
        missing_skills=["Go"],
        reasoning="Excellent fit for senior role"
    )
    if analysis_id:
        console.success(f"Analysis saved: {analysis_id}")
    else:
        console.error("Failed to save analysis")
    
    # Test 3: Save cover letter
    console.subheader("Test 3: Save cover letter")
    cover_id = db_service.save_cover_letter(
        job_title="Senior Developer",
        company_name="Acme Corp",
        content={"greeting": "Dear Hiring Manager", "body": "I am excited to apply..."},
        job_url="https://test2.greenhouse.io/jobs/67890"
    )
    if cover_id:
        console.success(f"Cover letter saved: {cover_id}")
    else:
        console.error("Failed to save cover letter")
    
    # Test 4: Save generated resume
    console.subheader("Test 4: Save generated resume")
    resume_id = db_service.save_generated_resume(
        tailored_content={"summary": "Experienced engineer...", "skills": ["Python", "SQL"]},
        job_title="Senior Developer",
        company="Acme Corp",
        job_url="https://test2.greenhouse.io/jobs/67890"
    )
    if resume_id:
        console.success(f"Resume saved: {resume_id}")
    else:
        console.error("Failed to save resume")
    
    # Test 5: Get summary
    console.subheader("Test 5: Get applications summary")
    summary = db_service.get_applications_summary()
    console.info(f"Total applications: {summary.get('total', 0)}")
    
    console.divider()
    console.success("All database persistence tests complete!")
    return True


if __name__ == "__main__":
    test_db_persistence()
