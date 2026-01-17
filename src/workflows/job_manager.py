
import asyncio
import yaml
from pathlib import Path

from src.core.logger import logger
from src.core.console import console
from src.models.profile import UserProfile
from src.automators.scout import ScoutAgent
from src.automators.analyst import AnalystAgent
from src.automators.applier import ApplierAgent

class JobApplicationWorkflow:
    """
    Orchestrates the end-to-end job application process.
    """
    def __init__(self):
        self.scout = ScoutAgent()
        self.analyst = AnalystAgent()
        self.applier = ApplierAgent()
        self.profile = self._load_profile()
        
        # Stats tracking
        self.stats = {
            "total_jobs": 0,
            "analyzed": 0,
            "applied": 0,
            "skipped": 0
        }

    def _load_profile(self) -> UserProfile:
        try:
            # Robust path finding
            base_dir = Path(__file__).resolve().parent.parent.parent
            profile_path = base_dir / "src/data/user_profile.yaml"
            
            with open(profile_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            return UserProfile(**data)
        except Exception as e:
            logger.critical(f"Failed to load user profile: {e}")
            console.error(f"Failed to load user profile: {e}")
            raise

    async def run(self, query: str, location: str, min_match_score: int = 70):
        # Display workflow banner
        console.workflow_start(query, location)
        
        logger.info(f"🚀 Starting Job Application Workflow for '{query}' in '{location}'")
        
        # 1. Scout
        job_urls = await self.scout.run(query, location)
        self.stats["total_jobs"] = len(job_urls)
        
        if not job_urls:
            logger.info("No jobs found. Exiting.")
            console.workflow_no_jobs()
            console.workflow_summary(0, 0, 0, 0)
            return

        resume_text = self.profile.to_resume_text()

        # 2. Iterate through jobs
        for i, url in enumerate(job_urls, 1):
            console.workflow_job_progress(i, len(job_urls), url)
            logger.info(f"--- Processing Job {i}/{len(job_urls)} ---")
            
            # 3. Analyze
            try:
                analysis = await self.analyst.run(url, resume_text)
                self.stats["analyzed"] += 1
            except Exception as e:
                logger.error(f"Analysis failed for {url}: {e}")
                console.error(f"Analysis failed: {e}")
                continue
            
            if analysis.match_score < min_match_score:
                console.workflow_skip(
                    reason=f"Score {analysis.match_score} < {min_match_score}",
                    company=analysis.company,
                    role=analysis.role,
                    score=analysis.match_score
                )
                logger.info(f"⏭️ Skipping: Score {analysis.match_score} < {min_match_score}. ({analysis.company}: {analysis.role})")
                self.stats["skipped"] += 1
                continue
            
            console.workflow_match(analysis.company, analysis.role, analysis.match_score)
            logger.info(f"✅ Match Found! Score: {analysis.match_score}. Applying to {analysis.company}...")
            
            # 4. Apply
            try:
                await self.applier.run(url, self.profile)
                logger.info(f"🎉 Application sequence completed for {url}")
                self.stats["applied"] += 1
            except Exception as e:
                logger.error(f"Application failed for {url}: {e}")
                console.error(f"Application failed: {e}")
                
            await asyncio.sleep(2)  # Brief pause
        
        # Display final summary
        console.workflow_summary(
            total_jobs=self.stats["total_jobs"],
            analyzed=self.stats["analyzed"],
            applied=self.stats["applied"],
            skipped=self.stats["skipped"]
        )

if __name__ == "__main__":
    workflow = JobApplicationWorkflow()
    asyncio.run(workflow.run("Software Engineer", "Remote"))

