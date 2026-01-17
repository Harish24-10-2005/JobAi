
"""
Getting Started Example 2: Form Filling

This example demonstrates how to:
- Navigate to a website with forms
- Fill out input fields
- Submit forms
- Handle basic form interactions

This builds on the basic search example by showing more complex interactions.

Setup:
1. Get your API key from https://cloud.browser-use.com/new-api-key
2. Set environment variable: export BROWSER_USE_API_KEY="your-key"
"""

import asyncio
import os
import sys
import yaml

# Add the parent directory to the path so we can import browser_use
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from browser_use import Tools,Agent, ChatOpenAI, ActionResult, Browser, ChatGroq
tools = Tools()

@tools.action(description='Ask human for help with a question')
def ask_human(question: str) -> ActionResult:
    answer = input(f'{question} > ')
    return f'The human responded with: {answer}'

def load_profile():
    with open(r"D:\JobAI\src\data\user_profile.yaml", "r") as f:
        return yaml.safe_load(f)

profile = load_profile()
target_link = "https://docs.google.com/forms/d/e/1FAIpQLSeRMSLQPmKlk-jaj2Nz9YgC5tOj-kJ16Nc5JE07HbWD3vGe1g/viewform" 

task = f"""
GOAL: Navigate to {target_link} and apply for the job using my profile data.

--- 
👤 CANDIDATE PROFILE (Use this data STRICTLY):
{yaml.dump(profile)}
---

📋 EXECUTION STEPS:
1. **Navigation:** Go to the URL. If redirected to a login page, use the 'Ask Human' tool immediately.
2. **Form Filling:** - Scan the page for input fields.
   - Map 'First Name', 'Last Name', 'Email', 'Phone' from the PROFILE above.
   - If asked for "LinkedIn" or "GitHub", use the URLs in the profile.
   - If asked for "Experience", calculate it based on the 'experience' section (approx 1 year).
   - If asked for "Sponsorship" or "Visa", select "No" / "Authorized to work" (based on profile).
3. **Smart Answers:** - If there is an open-ended question like "Why do you want this job?", generate a 2-sentence answer combining my 'skills' and the job title on the page.
4. **File Upload:** - If a Resume upload button appears, upload the file at: "{profile['files']['resume']}"
   - DO NOT try to drag-and-drop. Click the input element and send the file path.
5. **Final Review:**
   - Check if all required fields are filled.
   - Click 'Submit' or 'Apply'.

⚠️ CRITICAL RULES:
- DO NOT invent information. If a field requires data not in my profile (like "SSN"), use the 'Ask Human' tool.
- If the page allows "Easy Apply" via LinkedIn, try that first if possible, otherwise use the manual form.
"""



SPEED_OPTIMIZATION_PROMPT = """
Speed optimization instructions:
- Be extremely concise and direct in your responses
- Get to the goal as quickly as possible
- Use multi-action sequences whenever possible to reduce steps
"""
sensitive_data = {'g_email': 'harish.r2023ai-ds@sece.ac.in', 'g_pass': 'Harishravikumar@24102005'}


chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
user_data_path = r"C:\Users\LENOVO\AppData\Local\Google\Chrome\User Data"
profile_dir = "Profile 1"  # Derived from your Profile Path

# 2. Configure the Browser
browser = Browser(
    executable_path=chrome_path,
    user_data_dir=user_data_path,
    profile_directory=profile_dir,
    headless=False,
)
llm = ChatOpenAI(
    # model='x-ai/grok-4',
    # model='deepcogito/cogito-v2.1-671b',
    model='qwen/qwen3-coder:free',
    base_url='https://openrouter.ai/api/v1',
    api_key=os.getenv('OPENROUTER_API_KEY'),
    )
fallback_llm=ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

async def main():

    agent = Agent(
        task=task,
        llm=llm,
        browser=browser,
        use_vision=False,
        tools=tools,
        fallback_llm=fallback_llm,
        extend_system_message=SPEED_OPTIMIZATION_PROMPT,
        sensitive_data=sensitive_data,
        )
    await agent.run()


if __name__ == '__main__':
    asyncio.run(main())

this code is workin fine...
