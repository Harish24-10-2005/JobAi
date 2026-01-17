
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.workflows.job_manager import JobApplicationWorkflow

if __name__ == "__main__":
    query = "Software Engineer"
    location = "Remote"
    
    if len(sys.argv) > 2:
        query = sys.argv[1]
        location = sys.argv[2]
        
    workflow = JobApplicationWorkflow()
    try:
        asyncio.run(workflow.run(query, location))
    except KeyboardInterrupt:
        print("\n🛑 Execution stopped by user.")
    except Exception as e:
        print(f"❌ Fatal Error: {e}")
