# Agents module - Lazy imports

def get_resume_agent():
    from src.agents.resume_agent import resume_agent
    return resume_agent

def get_cover_letter_agent():
    from src.agents.cover_letter_agent import cover_letter_agent
    return cover_letter_agent

__all__ = [
    "get_resume_agent",
    "get_cover_letter_agent",
]
