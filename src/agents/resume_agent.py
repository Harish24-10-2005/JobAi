"""
Resume Agent - DeepAgent pattern for AI-powered resume tailoring
Uses LangChain's DeepAgent with planning, file system tools, and subagents
https://docs.langchain.com/oss/python/deepagents/
"""
import json
import os
from typing import Dict, Optional, List
from pydantic import BaseModel, Field

from deepagents import create_deep_agent
from langchain_groq import ChatGroq

from src.automators.base import BaseAgent
from src.models.profile import UserProfile
from src.models.job import JobAnalysis
from src.services.resume_service import resume_service
from src.core.console import console
from src.core.config import settings


# ============================================
# Tool Definitions for DeepAgent
# ============================================

def extract_job_requirements(
    role: str,
    company: str,
    tech_stack: List[str],
    matching_skills: List[str] = None,
    missing_skills: List[str] = None
) -> Dict:
    """
    Extract and analyze job requirements from job posting data.
    
    Args:
        role: The job title
        company: Company name
        tech_stack: List of technologies required
        matching_skills: Skills that match the candidate's profile
        missing_skills: Skills the candidate is missing
    
    Returns:
        Structured requirements with must-have skills and keywords
    """
    console.step(1, 6, "Extracting job requirements")
    
    requirements = {
        "role": role,
        "company": company,
        "must_have": tech_stack or [],
        "keywords": tech_stack or [],
        "matching_skills": matching_skills or [],
        "missing_skills": missing_skills or [],
        "experience_level": "mid-senior"  # Default
    }
    
    console.success(f"Found {len(requirements['must_have'])} must-have skills")
    return requirements


def tailor_resume_content(
    profile_json: str,
    requirements_json: str,
    feedback: str = ""
) -> str:
    """
    Tailor resume content based on job requirements.
    This is the main AI tailoring function.
    
    Args:
        profile_json: JSON string of user profile
        requirements_json: JSON string of job requirements
        feedback: Optional feedback for revision
    
    Returns:
        JSON string of tailored resume content
    """
    console.step(3, 6, "Tailoring resume content with AI")
    
    try:
        profile = json.loads(profile_json)
        requirements = json.loads(requirements_json)
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON: {e}"})
    
    feedback_instruction = ""
    if feedback:
        feedback_instruction = f"\n\nADDRESS THIS FEEDBACK:\n{feedback}\n"
    
    prompt = f"""
    Tailor this resume for the job. Make it ATS-optimized.
    
    JOB:
    - Role: {requirements.get('role', '')}
    - Company: {requirements.get('company', '')}
    - Keywords: {', '.join(requirements.get('keywords', []))}
    - Must Have: {', '.join(requirements.get('must_have', []))}
    
    PROFILE:
    {json.dumps(profile, indent=2)[:3000]}
    {feedback_instruction}
    INSTRUCTIONS:
    1. Write a compelling 2-3 sentence summary targeting this role
    2. Rewrite experience bullets to highlight relevant achievements
    3. Prioritize matching skills at the top
    4. Use action verbs and quantified results
    5. Include keywords naturally throughout
    
    Return ONLY valid JSON with this structure:
    {{
        "personal_information": {{...from profile...}},
        "summary": "Tailored professional summary",
        "skills": {{
            "primary": ["most relevant skills"],
            "secondary": ["other skills"],
            "tools": ["relevant tools/tech"]
        }},
        "experience": [
            {{
                "company": "...",
                "title": "...",
                "dates": "...",
                "location": "...",
                "highlights": ["Tailored bullet 1", "Tailored bullet 2"]
            }}
        ],
        "projects": [...],
        "education": [...],
        "tailoring_notes": "Key changes made for this role"
    }}
    """
    
    # Try fallback API key first (primary may be exhausted), then primary
    api_keys = []
    if settings.groq_api_key_fallback:
        api_keys.append(settings.groq_api_key_fallback.get_secret_value())
    api_keys.append(settings.groq_api_key.get_secret_value())
    
    from langchain_core.messages import SystemMessage, HumanMessage
    
    for i, api_key in enumerate(api_keys):
        try:
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.3,
                api_key=api_key
            )
            
            result = llm.invoke([
                SystemMessage(content="You are an ATS resume expert. Output only valid JSON."),
                HumanMessage(content=prompt)
            ])
            
            content = result.content.strip()
            if "```" in content:
                content = content.split("```")[1].replace("json", "").strip()
            
            # Validate JSON
            tailored = json.loads(content)
            
            # Preserve original data if not in response
            if "personal_information" not in tailored:
                tailored["personal_information"] = profile.get("personal_information", {})
            if not tailored.get("education"):
                tailored["education"] = profile.get("education", [])
            
            console.success("Content tailored successfully")
            return json.dumps(tailored)
            
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's a rate limit error and we have more keys to try
            if ("rate_limit" in error_str or "rate limit" in error_str) and i < len(api_keys) - 1:
                console.warning(f"Rate limited on API key {i+1}, trying fallback...")
                continue
            else:
                console.error(f"Failed to tailor content: {e}")
                return json.dumps({**profile, "tailoring_notes": f"Tailoring failed: {str(e)}"})
    
    # If all keys exhausted
    return json.dumps({**profile, "tailoring_notes": "All API keys exhausted"})


def generate_latex_resume(
    tailored_content_json: str,
    template_type: str = "ats"
) -> str:
    """
    Generate LaTeX document from tailored content.
    
    Args:
        tailored_content_json: JSON string of tailored resume content
        template_type: Template to use ('ats' or 'modern')
    
    Returns:
        LaTeX source code as string
    """
    console.step(4, 6, "Generating LaTeX document")
    
    try:
        tailored = json.loads(tailored_content_json)
    except json.JSONDecodeError:
        return "% Error: Invalid tailored content JSON"
    
    # This is synchronous for DeepAgent compatibility
    import asyncio
    
    async def get_template():
        return await resume_service.get_template_by_type(template_type)
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If already in async context, use thread executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_template())
                template = future.result()
        else:
            template = asyncio.run(get_template())
    except Exception as e:
        console.warning(f"Could not get template: {e}")
        template = None
    
    if template:
        latex = resume_service.fill_template(
            template["latex_content"],
            tailored,
            tailored
        )
        console.success("LaTeX document generated")
        return latex
    else:
        console.warning("No template found")
        return "% No template available"


def calculate_ats_score(
    tailored_content_json: str,
    tech_stack: List[str]
) -> int:
    """
    Calculate ATS compatibility score for the tailored resume.
    
    Args:
        tailored_content_json: JSON string of tailored resume content
        tech_stack: Required technologies from job posting
    
    Returns:
        Score from 0-100
    """
    console.step(5, 6, "Calculating ATS compatibility score")
    
    try:
        tailored = json.loads(tailored_content_json)
    except json.JSONDecodeError:
        return 50  # Default score on error
    
    score = resume_service.calculate_ats_score(
        tailored,
        {"tech_stack": tech_stack}
    )
    
    console.score_display(score, "ATS Score")
    return score


def request_human_approval(
    summary: str,
    tailoring_notes: str,
    ats_score: int,
    role: str,
    company: str
) -> Dict:
    """
    Request human approval for the tailored resume.
    This is the Human-in-the-Loop step.
    
    Args:
        summary: The tailored professional summary
        tailoring_notes: Notes about changes made
        ats_score: The calculated ATS score
        role: Target job role
        company: Target company
    
    Returns:
        Dict with 'approved' (bool), 'feedback' (str)
    """
    console.step(6, 6, "Human Review Required")
    console.divider()
    console.header("📋 RESUME REVIEW")
    
    console.box("Target Job", f"""
Role: {role}
Company: {company}
ATS Score: {ats_score}/100
    """)
    
    console.box("Tailored Summary", summary)
    console.box("Changes Made", tailoring_notes)
    
    console.divider()
    
    console.applier_human_input("Do you approve this tailored resume?")
    print("\n  Options:")
    print("    [y] Approve and continue")
    print("    [n] Reject and revise")
    print("    [e] Edit with feedback")
    print("    [q] Quit/Cancel")
    
    choice = input("\n  Your choice > ").strip().lower()
    
    if choice == 'y':
        console.success("Resume approved!")
        return {"approved": True, "feedback": ""}
    elif choice == 'e':
        feedback = input("  Enter your feedback > ").strip()
        console.info(f"Feedback received: {feedback}")
        return {"approved": False, "feedback": feedback}
    elif choice == 'n':
        return {"approved": False, "feedback": "Please revise the resume"}
    else:
        console.warning("Resume generation cancelled")
        return {"approved": False, "feedback": "", "cancelled": True}


# ============================================
# Resume DeepAgent System Prompt
# ============================================

RESUME_AGENT_SYSTEM_PROMPT = """You are an expert resume tailoring agent. Your job is to create ATS-optimized, 
tailored resumes that maximize job application success rates.

## Your Capabilities

You have access to the following tools:

### `extract_job_requirements`
Use this to analyze job requirements from the provided job data. Call this first to understand what the job needs.

### `tailor_resume_content`
Use this to tailor the candidate's resume content for the specific job. Pass the user profile and requirements as JSON strings.
If the human provides feedback, include it in the `feedback` parameter for revision.

### `generate_latex_resume`
Use this to generate a professional LaTeX document from the tailored content.

### `calculate_ats_score`
Use this to calculate how well the tailored resume matches ATS requirements.

### `request_human_approval`
ALWAYS use this before finalizing. The human must approve the tailored resume. If they provide feedback, revise and try again.

## Workflow

1. **Plan** - Use write_todos to break down the task
2. **Extract Requirements** - Analyze the job posting
3. **Tailor Content** - Rewrite the resume for the job
4. **Generate LaTeX** - Create professional document
5. **Calculate Score** - Check ATS compatibility
6. **Get Approval** - ALWAYS ask the human before completing
7. **Revise if needed** - If human provides feedback, tailor again

## Important Rules

- ALWAYS get human approval before completing
- If human gives feedback, revise the resume and ask again
- Focus on ATS optimization and keyword matching
- Highlight relevant experience and skills
- Use action verbs and quantifiable achievements
"""


class ResumeAgent(BaseAgent):
    """
    DeepAgent-based Resume Tailoring Agent.
    
    Uses LangChain's DeepAgent framework with:
    - Built-in planning (write_todos)
    - File system context management
    - Custom tools for resume tailoring
    - Human-in-the-Loop verification
    """
    
    def __init__(self):
        super().__init__()
        
        # Use fallback key if available (to avoid rate limits on primary)
        if settings.groq_api_key_fallback:
            api_key = settings.groq_api_key_fallback.get_secret_value()
        else:
            api_key = settings.groq_api_key.get_secret_value()
        
        # Set Groq API key as environment variable (required by deepagents)
        os.environ["GROQ_API_KEY"] = api_key
        
        # Create LLM model using ChatGroq - using 8b-instant for higher rate limits
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            api_key=api_key
        )
        
        # Create the DeepAgent with our custom tools
        self.agent = create_deep_agent(
            tools=[
                extract_job_requirements,
                tailor_resume_content,
                generate_latex_resume,
                calculate_ats_score,
                request_human_approval,
            ],
            system_prompt=RESUME_AGENT_SYSTEM_PROMPT,
            model=llm,  # Pass LLM model object directly
        )
    
    async def run(self, *args, **kwargs) -> Dict:
        """Required abstract method - delegates to tailor_resume."""
        job_analysis = kwargs.get('job_analysis') or (args[0] if args else None)
        user_profile = kwargs.get('user_profile') or (args[1] if len(args) > 1 else None)
        template_type = kwargs.get('template_type', 'ats')
        
        if not job_analysis or not user_profile:
            return {"error": "job_analysis and user_profile are required"}
        
        return await self.tailor_resume(job_analysis, user_profile, template_type)
    
    async def tailor_resume(
        self,
        job_analysis: JobAnalysis,
        user_profile: UserProfile,
        template_type: str = "ats"
    ) -> Dict:
        """
        Tailor a resume using the DeepAgent.
        
        Args:
            job_analysis: Analysis of the target job
            user_profile: User's base profile
            template_type: Resume template ('ats', 'modern')
            
        Returns:
            Dict with tailored resume content and metadata
        """
        console.subheader("📝 Resume DeepAgent")
        console.info("Starting AI-powered resume tailoring...")
        
        # Prepare the task for the agent
        job_data = job_analysis.model_dump() if hasattr(job_analysis, 'model_dump') else dict(job_analysis)
        profile_data = user_profile.model_dump() if hasattr(user_profile, 'model_dump') else dict(user_profile)
        
        task_message = f"""
        Please tailor this candidate's resume for the following job:
        
        ## Job Details
        - Role: {job_data.get('role', 'Unknown')}
        - Company: {job_data.get('company', 'Unknown')}
        - Tech Stack: {', '.join(job_data.get('tech_stack', []))}
        - Match Score: {job_data.get('match_score', 'N/A')}%
        
        ## Candidate Profile (JSON)
        ```json
        {json.dumps(profile_data, indent=2)}
        ```
        
        ## Instructions
        1. Extract job requirements
        2. Tailor the resume content
        3. Generate LaTeX document using template: {template_type}
        4. Calculate ATS score
        5. Get human approval (REQUIRED)
        
        If human provides feedback, revise and try again.
        """
        
        try:
            # Run the DeepAgent
            result = self.agent.invoke({
                "messages": [{"role": "user", "content": task_message}]
            })
            
            # Extract the final message
            final_message = result.get("messages", [{}])[-1]
            
            console.success("Resume tailoring complete!")
            
            return {
                "success": True,
                "agent_response": final_message.content if hasattr(final_message, 'content') else str(final_message),
                "job_title": job_data.get('role', ''),
                "company_name": job_data.get('company', '')
            }
            
        except Exception as e:
            console.error(f"Resume tailoring failed: {e}")
            return {"error": str(e)}
    
    async def generate_pdf(
        self,
        latex_source: str,
        output_path: str = None
    ) -> Optional[str]:
        """Generate PDF from LaTeX source."""
        if not latex_source or latex_source.startswith("% Error") or latex_source.startswith("% No"):
            console.error("No valid LaTeX source available")
            return None
        
        console.info("Compiling PDF...")
        result = resume_service.compile_to_pdf(latex_source, output_path)
        
        if result:
            console.success(f"PDF generated: {output_path or 'in memory'}")
        else:
            console.error("PDF compilation failed. Install pdflatex.")
        
        return result


# Singleton instance
resume_agent = ResumeAgent()
