import yaml
from src.automators.base import BaseAgent
from src.models.profile import UserProfile
from src.core.console import console

# Import browser_use at module level like the working example
from browser_use import Tools, Agent, ChatOpenAI, ActionResult, Browser, ChatGroq

# Initialize Tools at module level (like working example)
tools = Tools()

@tools.action(description='Ask human for help with a question')
def ask_human(question: str) -> ActionResult:
    console.applier_human_input(question)
    answer = input(f'\n  ❓ Your answer > ')
    console.applier_status("Received human input", "Response recorded")
    return f'The human responded with: {answer}'


class ApplierAgent(BaseAgent):
    """
    Agent responsible for applying to jobs using Browser automation.
    """
    def __init__(self):
        super().__init__()
        self.browser = None

    async def run(self, url: str, profile: UserProfile) -> str:
        """
        Executes the application process.
        """
        # Rich console output
        console.applier_header(url)
        self.logger.info(f"🚀 ApplierAgent: Starting application for {url}")
        
        # Convert profile to YAML format (like working example)
        profile_dict = profile.model_dump()
        profile_yaml = yaml.dump(profile_dict)
        resume_path = profile.files.resume
        
        console.applier_status("Preparing application", "Loading profile and resume")
        
        task_prompt = f"""
GOAL: Navigate to {url} and apply for the job using my profile data.

--- 
👤 CANDIDATE PROFILE (Use this data STRICTLY):
{profile_yaml}
---

📋 EXECUTION STEPS:
1. **Navigation:** Go to the URL. If redirected to a login page, use the 'ask_human' tool immediately.
2. **Form Filling:** 
   - Scan the page for input fields.
   - Map 'First Name', 'Last Name', 'Email', 'Phone' from the PROFILE above.
   - If asked for "LinkedIn" or "GitHub", use the URLs in the profile.
   - If asked for "Experience", calculate based on the 'experience' section.
   - If asked for "Sponsorship" or "Visa", select "No" / "Authorized to work".
3. **Smart Answers:** 
   - If there is an open-ended question like "Why do you want this job?", generate a 2-sentence answer.
4. **File Upload:** 
   - If a Resume upload button appears, upload: "{resume_path}"
   - DO NOT try to drag-and-drop. Click the input element and send the file path.
5. **Final Review:**
   - Check if all required fields are filled.
   - Click 'Submit' or 'Apply'.

⚠️ CRITICAL RULES:
- DO NOT invent information. If a field requires data not in the profile (like "SSN"), use 'ask_human'.
- If the page allows "Easy Apply" via LinkedIn, try that first if possible, otherwise use the manual form.
"""

        console.applier_status("Initializing browser", "Chrome automation starting...")
        
        # Initialize Browser (matching working example exactly)
        browser = Browser(
            executable_path=self.settings.chrome_path,
            user_data_dir=self.settings.user_data_dir,
            profile_directory=self.settings.profile_directory,
            headless=self.settings.headless
        )
        
        console.applier_status("Configuring AI models", "OpenRouter + Groq fallback")
        
        # Configure LLMs (matching working example - no api_key for ChatGroq)
        llm = ChatOpenAI(
            model='qwen/qwen3-coder:free',
            base_url='https://openrouter.ai/api/v1',
            api_key=self.settings.get_openrouter_key()
        )
        fallback_llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
        
        SPEED_OPTIMIZATION_PROMPT = """
Speed optimization instructions:
- Be extremely concise and direct in your responses
- Get to the goal as quickly as possible
- Use multi-action sequences whenever possible to reduce steps
"""
        
        try:
            agent = Agent(
                task=task_prompt,
                llm=llm,
                browser=browser,
                use_vision=False,
                tools=tools,
                fallback_llm=fallback_llm,
                extend_system_message=SPEED_OPTIMIZATION_PROMPT,
            )
            
            console.applier_status("Running browser agent", "Navigating and filling forms...")
            await agent.run()
            
            console.applier_complete(True)
            return "Application process finished."
            
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            console.applier_complete(False, str(e))
            raise
