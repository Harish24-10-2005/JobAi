"""
Company Research Agent - AI-powered company analysis
Uses LangChain's DeepAgent for pre-interview company research
"""
import json
import os
from typing import Dict, List, Optional

from deepagents import create_deep_agent
from langchain_groq import ChatGroq

from src.automators.base import BaseAgent
from src.core.console import console
from src.core.config import settings


# ============================================
# Tool Definitions for Company DeepAgent
# ============================================

def search_company_info(
    company: str,
    role: str = ""
) -> Dict:
    """
    Search for basic company information.
    
    Args:
        company: Company name
        role: Target role (optional, for context)
    
    Returns:
        Company overview with key facts
    """
    console.step(1, 4, f"Researching {company}")
    
    api_key = settings.groq_api_key_fallback.get_secret_value() if settings.groq_api_key_fallback else settings.groq_api_key.get_secret_value()
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=api_key
    )
    
    prompt = f"""
    Provide a company research summary for {company}.
    Context: Candidate interviewing for {role or 'a position'} there.
    
    Return ONLY valid JSON with realistic, helpful information:
    {{
        "company_name": "{company}",
        "industry": "Tech/Finance/etc",
        "size": "Startup/Mid-size/Enterprise",
        "employee_count": "approximate",
        "founded": "year",
        "headquarters": "location",
        "mission": "company mission statement",
        "values": ["value1", "value2"],
        "tech_stack": ["known technologies"],
        "products": ["main products/services"],
        "competitors": ["competitor1", "competitor2"],
        "recent_news": ["recent headline 1", "recent headline 2"],
        "interview_tips": [
            "Mention their mission about...",
            "Show interest in their product..."
        ],
        "questions_to_ask": [
            "Good question for the interviewer",
            "Another insightful question"
        ]
    }}
    """
    
    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        
        result = llm.invoke([
            SystemMessage(content="You are a company research expert. Provide accurate, helpful information. Output only valid JSON."),
            HumanMessage(content=prompt)
        ])
        
        content = result.content.strip()
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        
        parsed = json.loads(content)
        console.success(f"Found info for {company}")
        return parsed
        
    except Exception as e:
        console.error(f"Failed to research company: {e}")
        return {"error": str(e), "company_name": company}


def analyze_company_culture(
    company: str,
    role: str = ""
) -> Dict:
    """
    Analyze company culture based on available data.
    
    Args:
        company: Company name
        role: Target role for context
    
    Returns:
        Culture analysis with work-life balance, values, etc.
    """
    console.step(2, 4, "Analyzing company culture")
    
    api_key = settings.groq_api_key_fallback.get_secret_value() if settings.groq_api_key_fallback else settings.groq_api_key.get_secret_value()
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.4,
        api_key=api_key
    )
    
    prompt = f"""
    Analyze the work culture at {company} for someone interviewing for {role or 'a tech role'}.
    
    Provide realistic insights based on general knowledge.
    
    Return ONLY valid JSON:
    {{
        "culture_type": "Startup/Corporate/Remote-first/etc",
        "work_life_balance": {{
            "rating": "Good/Average/Demanding",
            "notes": "explanation"
        }},
        "growth_opportunities": {{
            "rating": "Excellent/Good/Limited",
            "notes": "explanation"
        }},
        "management_style": "Flat/Hierarchical/Mixed",
        "remote_policy": "Full remote/Hybrid/In-office",
        "diversity_inclusion": "Strong/Growing/Unknown",
        "engineering_culture": {{
            "code_review": true,
            "testing": "Strong/Moderate/Weak",
            "documentation": "Good/Average/Lacking",
            "innovation_time": "20% time/Hackathons/None"
        }},
        "pros": [
            "Pro 1",
            "Pro 2"
        ],
        "cons": [
            "Con 1",
            "Con 2"
        ],
        "best_for": "Type of person who thrives here",
        "glassdoor_style_rating": 3.8
    }}
    """
    
    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        
        result = llm.invoke([
            SystemMessage(content="You are an HR and culture analyst. Be balanced and realistic. Output only valid JSON."),
            HumanMessage(content=prompt)
        ])
        
        content = result.content.strip()
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        
        parsed = json.loads(content)
        console.success(f"Culture analysis complete")
        return parsed
        
    except Exception as e:
        console.error(f"Failed to analyze culture: {e}")
        return {"error": str(e)}


def identify_red_flags(
    company: str,
    job_description: str = ""
) -> Dict:
    """
    Identify potential red flags about the company or job posting.
    
    Args:
        company: Company name
        job_description: Job posting text (optional)
    
    Returns:
        Red flags and concerns to investigate
    """
    console.step(3, 4, "Checking for red flags")
    
    api_key = settings.groq_api_key_fallback.get_secret_value() if settings.groq_api_key_fallback else settings.groq_api_key.get_secret_value()
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=api_key
    )
    
    jd_context = f"\n\nJob Description:\n{job_description[:1500]}" if job_description else ""
    
    prompt = f"""
    Analyze potential red flags for {company}.{jd_context}
    
    Check for common warning signs candidates should investigate.
    
    Return ONLY valid JSON:
    {{
        "company_red_flags": [
            {{
                "flag": "Description of concern",
                "severity": "high|medium|low",
                "how_to_verify": "How to investigate this"
            }}
        ],
        "job_posting_red_flags": [
            {{
                "flag": "Vague salary/Unrealistic expectations/etc",
                "severity": "high|medium|low",
                "what_to_ask": "Question to clarify"
            }}
        ],
        "questions_to_ask_in_interview": [
            "Why is this position open?",
            "What happened to the previous person?",
            "What does success look like in 6 months?"
        ],
        "things_to_research": [
            "Check Glassdoor reviews",
            "LinkedIn employee tenure",
            "Recent funding/layoffs news"
        ],
        "overall_risk_level": "low|medium|high",
        "recommendation": "Proceed with caution / Looks good / Major concerns"
    }}
    """
    
    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        
        result = llm.invoke([
            SystemMessage(content="You are a career counselor helping candidates avoid bad job situations. Be thorough but fair. Output only valid JSON."),
            HumanMessage(content=prompt)
        ])
        
        content = result.content.strip()
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        
        parsed = json.loads(content)
        
        risk = parsed.get("overall_risk_level", "unknown")
        if risk == "low":
            console.success(f"Low risk - looks good!")
        elif risk == "medium":
            console.warning(f"Medium risk - investigate further")
        else:
            console.error(f"High risk - proceed with caution")
        
        return parsed
        
    except Exception as e:
        console.error(f"Failed to check red flags: {e}")
        return {"error": str(e)}


def get_interview_insights(
    company: str,
    role: str
) -> Dict:
    """
    Get interview insights and tips for the specific company.
    
    Args:
        company: Company name
        role: Target role
    
    Returns:
        Interview process insights and preparation tips
    """
    console.step(4, 4, "Getting interview insights")
    
    api_key = settings.groq_api_key_fallback.get_secret_value() if settings.groq_api_key_fallback else settings.groq_api_key.get_secret_value()
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.5,
        api_key=api_key
    )
    
    prompt = f"""
    Provide interview insights for {role} at {company}.
    
    Return ONLY valid JSON:
    {{
        "interview_process": {{
            "typical_rounds": ["Phone Screen", "Technical", "Onsite"],
            "duration": "2-4 weeks typical",
            "difficulty": "Medium/Hard"
        }},
        "common_question_topics": [
            "Topic 1 they often ask about",
            "Topic 2",
            "Topic 3"
        ],
        "technical_focus": [
            "Coding patterns they prefer",
            "System design if senior"
        ],
        "behavioral_themes": [
            "Leadership principles they value",
            "Cultural fit aspects"
        ],
        "tips_from_candidates": [
            "Tip 1 from people who interviewed",
            "Tip 2"
        ],
        "what_they_look_for": [
            "Problem-solving approach",
            "Communication during coding"
        ],
        "resources": [
            {{
                "name": "Glassdoor Interview Reviews",
                "url": "https://glassdoor.com/Interview/{company.replace(' ', '-')}-Interview-Questions"
            }},
            {{
                "name": "LeetCode Company Tag",
                "url": "https://leetcode.com/company/{company.lower().replace(' ', '-')}/"
            }}
        ]
    }}
    """
    
    try:
        from langchain_core.messages import SystemMessage, HumanMessage
        
        result = llm.invoke([
            SystemMessage(content="You are an interview coach with knowledge of tech company hiring. Output only valid JSON."),
            HumanMessage(content=prompt)
        ])
        
        content = result.content.strip()
        if "```" in content:
            content = content.split("```")[1].replace("json", "").strip()
        
        parsed = json.loads(content)
        console.success("Interview insights ready")
        return parsed
        
    except Exception as e:
        console.error(f"Failed to get insights: {e}")
        return {"error": str(e)}


# ============================================
# Company Agent System Prompt
# ============================================

COMPANY_AGENT_SYSTEM_PROMPT = """You are an expert company research analyst helping job candidates prepare for interviews.

## Your Capabilities

### `search_company_info`
Get company overview: industry, size, mission, tech stack, products, competitors.

### `analyze_company_culture`
Analyze work culture: work-life balance, growth, management style, pros/cons.

### `identify_red_flags`
Check for warning signs in the company or job posting.

### `get_interview_insights`
Get specific interview tips, common questions, and what they look for.

## Workflow

1. **Research** - Get basic company information
2. **Culture** - Analyze work culture and fit
3. **Red Flags** - Identify concerns to investigate
4. **Interview Tips** - Provide specific interview insights

## Guidelines

- Be balanced and fair - mention both pros and cons
- Provide actionable insights, not just generic advice
- Always include questions the candidate should ask
- Flag serious concerns clearly but don't be alarmist
"""


class CompanyAgent(BaseAgent):
    """
    DeepAgent-based Company Research Agent.
    
    Researches companies, analyzes culture, identifies red flags,
    and provides interview-specific insights.
    """
    
    def __init__(self):
        super().__init__()
        
        if settings.groq_api_key_fallback:
            api_key = settings.groq_api_key_fallback.get_secret_value()
        else:
            api_key = settings.groq_api_key.get_secret_value()
        
        os.environ["GROQ_API_KEY"] = api_key
        
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.4,
            api_key=api_key
        )
        
        self.agent = create_deep_agent(
            tools=[
                search_company_info,
                analyze_company_culture,
                identify_red_flags,
                get_interview_insights,
            ],
            system_prompt=COMPANY_AGENT_SYSTEM_PROMPT,
            model=llm,
        )
    
    async def run(self, *args, **kwargs) -> Dict:
        """Required abstract method."""
        company = kwargs.get('company', '')
        role = kwargs.get('role', '')
        
        if not company:
            return {"error": "company name is required"}
        
        return await self.research_company(company, role)
    
    async def research_company(
        self,
        company: str,
        role: str = "",
        job_description: str = ""
    ) -> Dict:
        """
        Comprehensive company research.
        
        Args:
            company: Company name
            role: Target role
            job_description: Optional job posting text
            
        Returns:
            Complete research report
        """
        console.subheader(f"🏢 Researching {company}")
        console.info("Gathering company intelligence...")
        
        # Get all information
        info = search_company_info(company, role)
        culture = analyze_company_culture(company, role)
        red_flags = identify_red_flags(company, job_description)
        insights = get_interview_insights(company, role)
        
        return {
            "success": True,
            "company": company,
            "role": role,
            "company_info": info,
            "culture_analysis": culture,
            "red_flags": red_flags,
            "interview_insights": insights
        }
    
    async def quick_check(
        self,
        company: str
    ) -> Dict:
        """Quick company overview without full analysis."""
        console.subheader(f"🏢 Quick Check: {company}")
        
        info = search_company_info(company)
        red_flags = identify_red_flags(company)
        
        return {
            "success": True,
            "company": company,
            "overview": info,
            "risk_level": red_flags.get("overall_risk_level", "unknown"),
            "key_concerns": red_flags.get("company_red_flags", [])[:3]
        }


# Singleton instance
company_agent = CompanyAgent()
